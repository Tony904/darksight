import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import globals as gbs
import darknet
import cv2
import numpy as np
import functools
import image_utils as imut
import my_utils as mut
from capture import CaptureStream, CaptureProperties
from inference import Inference
from display import DisplayDrawer
from conductor import Conductor
from darksight_lev_designer import Ui_form_main_lev
import time


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.mw = MainWindow()
        self.mw.show()


class MainWindow(qtw.QWidget):
    run_capture = qtc.pyqtSignal()
    run_conductor = qtc.pyqtSignal(int, int, float, list)
    display_pixmap_set = qtc.pyqtSignal()
    sg_start_display_loop = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_form_main_lev()
        self.ui.setupUi(self)

        self.caps = []
        self.cap_qthreads = []

        self.display_loop_active = False

        self._init_connect_signals_to_slots()

        self.show()

        self.conductor = Conductor()
        self.conductor_qthread = qtc.QThread()
        self.conductor.moveToThread(self.conductor_qthread)
        self.conductor_qthread.start()
        self.display_drawer = DisplayDrawer()
        self.display_drawer_qthread = qtc.QThread()
        self.display_drawer.moveToThread(self.display_drawer_qthread)
        self.display_drawer_qthread.start()
        self.inference = Inference()
        self.inference_qthread = qtc.QThread()
        self.inference.moveToThread(self.inference_qthread)
        self.inference_qthread.start()

        self._set_det_controls_connections()
        self._set_display_loop_connections()

    def _block_signals(func):
        @functools.wraps(func)
        def wrapper(*args):
            args[0].blockSignals(True)
            func(*args)
            args[0].blockSignals(False)
        return wrapper

    def _set_event_handlers(self):
        self.ui.lbl_main_pixmap.mouseMoveEvent = self.lbl_main_pixmap_mouseMoveEvent_handler
        self.ui.lbl_main_pixmap.mouseReleaseEvent = self.lbl_main_pixmap_mouseReleaseEvent_handler

    def lbl_main_pixmap_mouseMoveEvent_handler(self, e):
        # print(e.pos())
        pass

    def lbl_main_pixmap_mouseReleaseEvent_handler(self, e):
        pass

    def _init_connect_signals_to_slots(self):
        self.ui.btn_start_cap_2.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_2.text(), 0))
        self.ui.btn_start_cap_3.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_3.text(), 1))
        self.ui.btn_start_cap_4.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_4.text(), 2))
        self.ui.btn_start_cap_5.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_5.text(), 3))
        self.ui.btn_stop_cap_2.clicked.connect(lambda s: self.stop_capture(0))
        self.ui.btn_stop_cap_3.clicked.connect(lambda s: self.stop_capture(1))
        self.ui.btn_stop_cap_4.clicked.connect(lambda s: self.stop_capture(2))
        self.ui.btn_stop_cap_5.clicked.connect(lambda s: self.stop_capture(3))

        self.ui.btn_pan_up.clicked.connect(
            lambda s: self.update_active_cap_prop('pan', (0, -self.ui.spbx_pan_inc.value())))
        self.ui.btn_pan_down.clicked.connect(
            lambda s: self.update_active_cap_prop('pan', (0, self.ui.spbx_pan_inc.value())))
        self.ui.btn_pan_left.clicked.connect(
            lambda s: self.update_active_cap_prop('pan', (-self.ui.spbx_pan_inc.value(), 0)))
        self.ui.btn_pan_right.clicked.connect(
            lambda s: self.update_active_cap_prop('pan', (self.ui.spbx_pan_inc.value(), 0)))

        self.ui.tabw_cam_settings.currentChanged.connect(self.cam_tab_changed)
        self.ui.tabw_recipe_builder.currentChanged.connect(self.recipe_builder_tab_changed)

        self.ui.btn_load_darknet.clicked.connect(self.load_darknet)

    def cam_tab_changed(self, i):
        for n in range(len(self.caps)):
            if i == self.caps[n].uid:
                self._load_cap_props_to_ui(i, n)
                return 0
        self.ui.ledit_cam_index.setText('')

    def _load_cap_props_to_ui(self, uid, n):
        self._setText_no_signal(self.ui.ledit_cam_index, self.caps[n].props.c)
        self._setValue_no_signal(self.ui.spbx_cap_focus, self.caps[n].props.focus)
        if self.caps[n].props.autofocus == 1:
            self._setChecked_no_signal(self.ui.chbx_cap_autofocus, True)
        else:
            self._setChecked_no_signal(self.ui.chbx_cap_autofocus, False)
        self._setValue_no_signal(self.ui.spbx_cap_brightness, self.caps[n].props.brightness)
        self._setValue_no_signal(self.ui.spbx_cap_contrast, self.caps[n].props.contrast)
        self._setValue_no_signal(self.ui.spbx_cap_hue, self.caps[n].props.hue)
        self._setValue_no_signal(self.ui.spbx_cap_saturation, self.caps[n].props.saturation)
        self._setValue_no_signal(self.ui.spbx_cap_sharpness, self.caps[n].props.sharpness)
        self._setValue_no_signal(self.ui.spbx_cap_gamma, self.caps[n].props.gamma)
        self._setValue_no_signal(self.ui.spbx_cap_white, self.caps[n].props.white)
        if self.caps[n].props.autowhite == 1:
            self._setChecked_no_signal(self.ui.chbx_cap_autowhite, True)
        else:
            self._setChecked_no_signal(self.ui.chbx_cap_autowhite, False)
        self._setValue_no_signal(self.ui.spbx_cap_backlight, self.caps[n].props.backlight)
        self._setValue_no_signal(self.ui.spbx_cap_gain, self.caps[n].props.gain)
        self._setValue_no_signal(self.ui.spbx_cap_exposure, self.caps[n].props.exposure)
        if self.caps[n].props.autoexposure == 1:
            self._setChecked_no_signal(self.ui.chbx_cap_autoexposure, True)
        else:
            self._setChecked_no_signal(self.ui.chbx_cap_autoexposure, False)
        self._setValue_no_signal(self.ui.spbx_dbl_zoom_img, self.caps[n].props.zoom)
        self._setValue_no_signal(self.ui.spbx_rotate_img, self.caps[n].props.rotate)
        self._setText_no_signal(self.ui.ledit_cap_width, int(self.caps[n].props.width))
        self._setText_no_signal(self.ui.ledit_cap_height, int(self.caps[n].props.height))

    @staticmethod
    @_block_signals
    def _setValue_no_signal(widget, value):
        widget.setValue(value)

    @staticmethod
    @_block_signals
    def _setChecked_no_signal(widget, state):
        widget.setChecked(state)

    @staticmethod
    @_block_signals
    def _setText_no_signal(widget, text):
        widget.setText(str(text))

    @qtc.pyqtSlot(int)
    def recipe_builder_tab_changed(self, i):
        if i == 0:  # tab_recipe_builder is at tab index 0
            self.cam_tab_changed(self.ui.tabw_cam_settings.currentIndex())

    @qtc.pyqtSlot()
    def load_darknet(self):
        cfg_file = self.ui.ledit_cfg_file.text()
        data_file = self.ui.ledit_meta_data_file.text()
        weights_file = self.ui.ledit_weights_file.text()
        batch_size = 1
        gbs.network, gbs.class_names, _ = darknet.load_network(cfg_file, data_file, weights_file, batch_size)
        gbs.darknet_w = darknet.network_width(gbs.network)
        gbs.darknet_h = darknet.network_height(gbs.network)

        self.conductor.inference_enabled = True
        gbs.darknet_loaded = True
        self.ui.ptxt_darknet_output.setPlainText('Darknet loaded.')
        print("Darknet loaded.")
        print('Net Width: ' + str(gbs.darknet_w))
        print('Net Height: ' + str(gbs.darknet_h))

    def _connect_calib_controls_to_cap(self, cap):
        offset = 2
        props = ['backlight', 'brightness', 'contrast', 'exposure', 'focus', 'gain', 'gamma', 'hue', 'saturation',
                 'sharpness', 'white']
        s = '_' + str(cap.uid + offset)
        scar = self.ui.frme_cam_calib.findChild(qtw.QWidget, 'scar_con_cap_props' + s)
        prefix = 'spbx_cap_'
        for p in props:
            # print("prefix + p + s = " + prefix + p + s)
            w = scar.findChild(qtw.QSpinBox, prefix + p + s)
            w.valueChanged.connect(lambda x, i=p: cap.update_prop(i, x))
        print("Completed connecting panel to cap.")

    def _set_det_controls_connections(self):
        # self.ui.chbx_pause.stateChanged.connect(self.active_cap_pause)
        # self.ui.spbx_rotate_cap.valueChanged.connect(self.active_cap_rotate)
        # self.ui.spbx_dbl_zoom_cap.connect(self.active_cap_zoom)

        self.ui.spbx_cap_backlight.valueChanged.connect(lambda x: self.update_active_cap_prop('backlight', x))
        self.ui.spbx_cap_brightness.valueChanged.connect(lambda x: self.update_active_cap_prop('brightness', x))
        self.ui.spbx_cap_contrast.valueChanged.connect(lambda x: self.update_active_cap_prop('contrast', x))
        self.ui.spbx_cap_exposure.valueChanged.connect(lambda x: self.update_active_cap_prop('exposure', x))
        self.ui.spbx_cap_focus.valueChanged.connect(lambda x: self.update_active_cap_prop('focus', x))
        self.ui.spbx_cap_gain.valueChanged.connect(lambda x: self.update_active_cap_prop('gain', x))
        self.ui.spbx_cap_gamma.valueChanged.connect(lambda x: self.update_active_cap_prop('gamma', x))
        self.ui.spbx_cap_hue.valueChanged.connect(lambda x: self.update_active_cap_prop('hue', x))
        self.ui.spbx_cap_saturation.valueChanged.connect(lambda x: self.update_active_cap_prop('satruation', x))
        self.ui.spbx_cap_sharpness.valueChanged.connect(lambda x: self.update_active_cap_prop('sharpness', x))
        self.ui.spbx_cap_white.valueChanged.connect(lambda x: self.update_active_cap_prop('white', x))
        self.ui.spbx_dbl_zoom_img.valueChanged.connect(lambda x: self.update_active_cap_prop('zoom', x))

    def _set_display_loop_connections(self):
        self.sg_start_display_loop.connect(self.start_next_display_cycle)
        self.run_conductor.connect(self.conductor.run)
        self.conductor.sg_run_inference.connect(self.inference.run)
        self.inference.completed.connect(self.conductor.run_drawer)
        self.conductor.sg_run_drawer.connect(self.display_drawer.run)
        self.display_drawer.qimg_completed.connect(self.set_pixmap)
        self.display_pixmap_set.connect(self.start_next_display_cycle)

    def create_capture(self, cstr, uid):
        c = None
        try:
            c = int(cstr)
            valid = True
        except ValueError:
            valid = False
            print("A non-integer was entered for the camera index.")
            print("cstr=" + str(cstr))
        if valid:
            print("Attempting to create CaptureStream. c=" + str(c) + " uid=" + str(uid))
            c_open = True
            for n in range(len(self.caps)):
                if c == self.caps[n].props.c:
                    c_open = False
                    print("Error: Cam index " + str(c) + " already in use.")
                    break
            if c_open:
                print("Creating CaptureStream with uid=" + str(uid) + ", c=" + str(c))
                cap = CaptureStream()
                cap_thread = qtc.QThread()
                cap.moveToThread(cap_thread)
                cap_thread.start()
                self.caps.append(cap)
                self.cap_qthreads.append(cap_thread)

                cap.uid = uid
                cap.props.c = c
                cap.read_failed.connect(self.stop_capture)
                cap.deletion_requested.connect(self.delete_capture)
                self._connect_calib_controls_to_cap(cap)

                self.run_capture.connect(cap.run)
                self.run_capture.emit()
                print('emitted run_capture')
                self.run_capture.disconnect(cap.run)
                if self.display_loop_active is False:
                    self.display_loop_active = True
                    self.sg_start_display_loop.emit()

    def stop_capture(self, uid):
        print("Attempting to stop CaptureStream uid=" + str(uid))
        for n in range(len(self.caps)):
            if uid == self.caps[n].uid:
                self.caps[n].stop()

    @qtc.pyqtSlot(int)
    def delete_capture(self, uid):
        print("Attempting to delete CaptureStream uid=" + str(uid))
        for n in range(len(self.caps)):
            if uid == self.caps[n].uid:
                self.caps[n].read_failed.disconnect()
                del self.caps[n]
                self.cap_qthreads[n].quit()
                self.cap_qthreads[n].wait()
                del self.cap_qthreads[n]
                print("CaptureStream deleted.")
                break

    def update_active_cap_prop(self, prop, x):
        print('Updating active cap prop: ' + str(prop) + ' ' + str(x))
        uid = self.ui.tabw_cam_settings.currentIndex()
        for n in range(len(self.caps)):
            if uid == self.caps[n].uid:
                self.caps[n].update_prop(prop, x)
                break

    @qtc.pyqtSlot(qtg.QImage)
    def set_pixmap(self, qimg):
        if qimg is not None:
            qpix = qtg.QPixmap.fromImage(qimg)
            self.ui.lbl_main_pixmap.setPixmap(qpix)
        else:
            print('qimg = None, therefore no new pixamp set.')
        self.display_pixmap_set.emit()

    @qtc.pyqtSlot()
    def start_next_display_cycle(self):
        if self.display_loop_active:
            w = self.ui.lbl_main_pixmap.width()
            h = self.ui.lbl_main_pixmap.height()
            # t = inference_thresh_input_widget
            if len(self.caps) > 0:
                self.run_conductor.emit(w, h, 0.5, self.caps)
            else:
                self.display_loop_active = False
                print('Cannot start next display cycle. No CaptureStreams exist.')


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
