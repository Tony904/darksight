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
from class_inference_manager import InferenceManager
from class_emitter import Emitter
from class_inference import Inference
from class_detections_drawer import DetectionsDrawer
from darksight_lev_designer import Ui_form_main_lev


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.mw = MainWindow()
        self.mw.show()


class MainWindow(qtw.QWidget):
    run_capture = qtc.pyqtSignal()
    initiate_inference = qtc.pyqtSignal()
    send_img_to_manager = qtc.pyqtSignal(int, np.ndarray, Emitter)
    send_det_to_manager = qtc.pyqtSignal(int, list)
    send_inf_state_to_manager = qtc.pyqtSignal(bool)
    send_draw_state_to_manager = qtc.pyqtSignal(bool)
    display_pixmap_set = qtc.pyqtSignal()
    # send_window_size_to_display_manager = qtc.pyqtSignal(int, int)
    # send_uid_order_to_display_manager = qtc.pyqtSignal(list)
    display_params_emitted = qtc.pyqtSignal(int, int, list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_form_main_lev()
        self.ui.setupUi(self)

        self.caps = []
        self.cap_qthreads = []
        self.det_drawers = []
        self.drawer_qthreads = []
        self.emitters = []

        self._init_connect_signals_to_slots()

        self.show()

        self.display_manager = DisplayManager()
        self.display_manager_qthread = qtc.QThread()
        self.display_manager.moveToThread(self.display_manager_qthread)
        self.display_manager_qthread.start()
        self.display_drawer = DisplayDrawer()
        self.display_drawer_qthread = qtc.QThread()
        self.display_drawer.moveToThread(self.display_drawer_qthread)
        self.display_drawer_qthread.start()

        self._set_det_controls_connections()
        self._set_display_loop_connections()
        self._start_display_loop()

    def _init_connect_signals_to_slots(self):
        self.ui.btn_start_cap_2.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_2.text(), 0))
        self.ui.btn_start_cap_3.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_3.text(), 1))
        self.ui.btn_start_cap_4.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_4.text(), 2))
        self.ui.btn_start_cap_5.clicked.connect(lambda s: self.create_capture(self.ui.ledit_cam_index_5.text(), 3))
        self.ui.btn_stop_cap_2.clicked.connect(lambda s: self.stop_capture(0))
        self.ui.btn_stop_cap_3.clicked.connect(lambda s: self.stop_capture(1))
        self.ui.btn_stop_cap_4.clicked.connect(lambda s: self.stop_capture(2))
        self.ui.btn_stop_cap_5.clicked.connect(lambda s: self.stop_capture(3))

    def _load_darknet(self):
        cfg_file = self.ui.ledit_cfg_file
        data_file = self.ui.ledit_meta_data_file
        weights_file = self.ui.ledit_weights_file
        batch_size = 1
        gbs.network, gbs.class_names, _ = darknet.load_network(cfg_file, data_file, weights_file, batch_size)
        gbs.darknet_w = darknet.network_width(gbs.network)
        gbs.darknet_h = darknet.network_height(gbs.network)

        for n in range(len(self.caps)):
            drawer = DetectionsDrawer()
            drawer_qthread = qtc.QThread()
            drawer.moveToThread(drawer_qthread)
            drawer_qthread.start()
            emitter = Emitter()
            emitter.emitter_signal.connect(drawer.run)
            drawer.detections_drawn.connect(self.display_handler)
            self.emitters.append(emitter)
            self.det_drawers.append(drawer)
            self.drawer_qthreads.append(drawer_qthread)

        self.inference = Inference()
        self.inference_qthread = qtc.QThread()
        self.inference.moveToThread(self.inference_qthread)
        self.inference_qthread.start()

        self.infer_manager = InferenceManager()
        self.infer_manager.run_inference.connect(self.inference.run)
        self.infer_manager.emit_inference_packages.connect(self.inference.update_packages)
        self.infer_manager.inference_initiation_requested.connect(self.inference.initiate)
        self.inference.inference_packages_update_requested.connect(self.infer_manager.send_inference_packages)
        self.inference.inference_packages_updated.connect(self.infer_manager.request_inference_start)
        self.inference.inference_complete.connect(self.infer_manager.inference_completed)

        self.send_inf_package_to_manager.connect(self.infer_manager.update_inference_queue)

        self.initiate_inference.connect(self.inference.initiate)
        self.initiate_inference.emit()
        gbs.darknet_loaded = True
        print("Darknet loaded.")

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

    def _set_display_loop_connections(self):
        self.display_pixmap_set.connect(self.display_manager.request_display_params)
        self.display_manager.display_params_update_requested.connect(self.send_display_params)
        self.display_params_emitted.connect(self.display_manager.set_display_params)
        self.display_manager.display_drawer_update_emitted.connect(self.display_drawer.apply_update)
        self.display_drawer.updated.connect(self.display_drawer.run)
        self.display_drawer.qimg_completed.connect(self.set_pixmap)

        # self.send_window_size_to_display_manager.connect(self.display_manager.update_window_size)
        # self.send_uid_order_to_display_manager.connect(self.display_manager.update_uid_order)

    def _start_display_loop(self):
        self.set_pixmap(None)

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
                cap.frame_captured.connect(self.display_manager.update_queue)
                cap.read_failed.connect(self.stop_capture)
                cap.read_failed.connect(self.display_manager.clear_queue_index)
                cap.deletion_requested.connect(self.delete_capture)
                self._connect_calib_controls_to_cap(cap)

                self.run_capture.connect(cap.run)
                self.run_capture.emit()
                self.run_capture.disconnect(cap.run)

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
                self.caps[n].frame_captured.disconnect(self.display_manager.update_queue)
                del self.caps[n]
                self.cap_qthreads[n].quit()
                self.cap_qthreads[n].wait()
                del self.cap_qthreads[n]
                print("CaptureStream deleted.")
                break

    def update_active_cap_prop(self, prop, x):
        i = self.ui.tabw_cam_settings.currentIndex()
        self.caps[i].update_prop(prop, x)

    def set_pixmap(self, qimg):
        if qimg is not None:
            qpix = qtg.QPixmap.fromImage(qimg)
            self.ui.lbl_main_pixmap.setPixmap(qpix)
        self.display_pixmap_set.emit()

    @qtc.pyqtSlot()
    def send_display_params(self):
        w = self.ui.lbl_main_pixmap.width()
        h = self.ui.lbl_main_pixmap.height()
        # self.send_window_size_to_display_manager.emit(w, h)
        uid_order = [0, 1, 2, 3]
        # self.send_uid_order_to_display_manager.emit(uid_order)
        self.display_params_emitted.emit(w, h, uid_order)


class DisplayDrawer(qtc.QObject):
    updated = qtc.pyqtSignal()
    qimg_completed = qtc.pyqtSignal(qtg.QImage)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parts = []  # part=(ndarray, uid, CaptureProperties)
        self.window_w = None
        self.window_h = None
        self.uid_order = []  # element=int

        self.ndarray_dtype = np.uint8
        self.display_ndarray = None
        self.display_qimg = None

    @qtc.pyqtSlot()
    def run(self):
        for part in self.parts:
            if part is not None:
                uid = part[1]
                wd2 = self.window_w // 2
                hd2 = self.window_h // 2
                resized = imut.scale_by_largest_dim(part[0], wd2, hd2)
                pw = resized.shape[1]
                ph = resized.shape[0]
                if uid == self.uid_order[0]:
                    # put part in top left
                    top, bottom, left, right = 0, ph, 0, pw
                    self.display_ndarray[top:bottom, left:right] = resized
                elif uid == self.uid_order[1]:
                    # put part in top right
                    top, bottom, left, right = 0, ph, wd2, wd2 + pw
                    self.display_ndarray[top:bottom, left:right] = resized
                elif uid == self.uid_order[2]:
                    # put part in bottom left
                    top, bottom, left, right = hd2, hd2 + ph, 0, pw
                    self.display_ndarray[top:bottom, left:right] = resized
                elif uid == self.uid_order[3]:
                    # put part in bottom right
                    top, bottom, left, right = hd2, hd2 + ph, pw, self.window_w
                    self.display_ndarray[top:bottom, left:right] = resized
        data = self.display_ndarray.data
        cols = self.display_ndarray.shape[1]
        rows = self.display_ndarray.shape[0]
        stride = self.display_ndarray.strides[0]
        self.display_qimg = qtg.QImage(data, cols, rows, stride, qtg.QImage.Format_RGB888)
        self.qimg_completed.emit(self.display_qimg)

    @qtc.pyqtSlot(list, int, int, list)
    def apply_update(self, parts, window_w, window_h, uid_order):
        self.parts = list(parts)
        self.window_w = window_w
        self.window_h = window_h
        self.display_ndarray = np.zeros((window_h, window_w, 3), dtype=self.ndarray_dtype)
        self.uid_order = list(uid_order)
        self.updated.emit()


class DisplayManager(qtc.QObject):
    display_drawer_update_emitted = qtc.pyqtSignal(list, int, int, list)
    display_params_update_requested = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = [None, None, None, None]  # element=(ndarray, uid, CaptureProperties)
        self.window_w = None
        self.window_h = None
        self.uid_order = [0, 1, 2, 3]  # top-left, top-right, bottom-left, bottom-right

    @qtc.pyqtSlot(np.ndarray, int, qtc.QObject)
    def update_queue(self, ndarr, uid, props):
        tpl = (ndarr, uid, props)
        self.queue[uid] = tpl

    @qtc.pyqtSlot(int)
    def clear_queue_index(self, uid):
        self.queue[uid] = None
        print("Queue index cleared: uid=" + str(uid))

    # @qtc.pyqtSlot(int, int)
    # def update_window_size(self, window_w, window_h):
    #     self.window_w = window_w
    #     self.window_h = window_h
    #
    # @qtc.pyqtSlot(list)
    # def update_uid_order(self, uid_order):
    #     self.uid_order = list(uid_order)

    @qtc.pyqtSlot(int, int, list)
    def set_display_params(self, w, h, uid_order):
        self.window_w = w
        self.window_h = h
        self.uid_order = list(uid_order)

        self._send_display_params_to_drawer()

    @qtc.pyqtSlot()
    def request_display_params(self):
        self.display_params_update_requested.emit()

    def _send_display_params_to_drawer(self):
        self.display_drawer_update_emitted.emit(self.queue, self.window_w, self.window_h, self.uid_order)


class CaptureStream(qtc.QObject):
    frame_captured = qtc.pyqtSignal(np.ndarray, int, qtc.QObject)
    read_failed = qtc.pyqtSignal(int)
    deletion_requested = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props = CaptureProperties()
        self.cap_active = False
        self.cap = None
        self.uid = None
        print("New CaptureStream instance created.")

    @qtc.pyqtSlot()
    def run(self):
        print("CaptureStream run() executed. uid=" + str(self.uid))
        self.cap = cv2.VideoCapture(self.props.c, cv2.CAP_DSHOW)
        self.cap_active = True
        while self.cap.isOpened() and self.cap_active:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_captured.emit(frame_rgb, self.uid, self.props)
            else:
                print("Error: Camera read fail. uid=" + str(self.uid) + ", cam index=" + str(self.props.c))
                self.read_failed.emit(self.uid)
                self.cap_active = False
                break
        self.cap.release()
        if not self.cap_active:
            self.deletion_requested.emit(self.uid)

    @qtc.pyqtSlot()
    def update_prop(self, prop, x):
        print("Updating prop: " + prop + " x=" + str(x))
        if prop == 'autofocus':
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, x)
            self.props.autofocus = self.cap.get(cv2.CAP_PROP_AUTOFOCUS)
        elif prop == 'autoexposure':
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, x)
            self.props.autoexposure = self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
        elif prop == 'autowhite':
            self.cap.set(cv2.CAP_PROP_AUTO_WB, x)
            self.props.autowhite = self.cap.get(cv2.CAP_PROP_AUTO_WB)
        elif prop == 'focus':
            self.cap.set(cv2.CAP_PROP_FOCUS, x)
            self.props.focus = self.cap.get(cv2.CAP_PROP_FOCUS)
        elif prop == 'exposure':
            if not self.props.autoexposure:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, x)
                self.props.exposure = self.cap.get(cv2.CAP_PROP_EXPOSURE)
        elif prop == 'backlight':
            self.cap.set(cv2.CAP_PROP_BACKLIGHT, x)
            self.props.backlight = self.cap.get(cv2.CAP_PROP_BACKLIGHT)
        elif prop == 'sharpness':
            self.cap.set(cv2.CAP_PROP_SHARPNESS, x)
            self.props.sharpness = self.cap.get(cv2.CAP_PROP_SHARPNESS)
        elif prop == 'brightness':
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, x)
            self.props.brightness = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        elif prop == 'contrast':
            self.cap.set(cv2.CAP_PROP_CONTRAST, x)
            self.props.contrast = self.cap.get(cv2.CAP_PROP_CONTRAST)
        elif prop == 'gain':
            self.cap.set(cv2.CAP_PROP_GAIN, x)
            self.props.gain = self.cap.get(cv2.CAP_PROP_GAIN)
        elif prop == 'gamma':
            self.cap.set(cv2.CAP_PROP_GAMMA, x)
            self.props.gamma = self.cap.get(cv2.CAP_PROP_GAMMA)
        elif prop == 'hue':
            self.cap.set(cv2.CAP_PROP_HUE, x)
            self.props.hue = self.cap.get(cv2.CAP_PROP_HUE)
        elif prop == 'saturation':
            self.cap.set(cv2.CAP_PROP_SATURATION, x)
            self.props.saturation = self.cap.get(cv2.CAP_PROP_SATURATION)
        elif prop == 'white':
            if not self.props.autowhite:
                self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, x)
                self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, x)
                self.props.white = self.cap.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V)
        elif prop == 'zoom':
            self.props.zoom = x
        elif prop == 'rotate':
            self.props.rotate = x
        elif prop == 'crop':
            self.props.crop = x
        elif prop == 'pan':
            self.props.pan = x

    def stop(self):
        print("Stopped CaptureStream: " + str(self.uid))
        self.cap_active = False


class CaptureProperties(qtc.QObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = -1
        self.width = 5000
        self.height = 4000
        self.focus = 300.
        self.autofocus = 1  # 2 = disabled, 1 = enabled
        self.brightness = 0
        self.contrast = 32
        self.hue = 0
        self.saturation = 64
        self.sharpness = 3
        self.gamma = 100
        self.white = 4600
        self.autowhite = 1
        self.backlight = 1
        self.gain = 0
        self.exposure = -6
        self.autoexposure = 1  # if disabled, must be re-enabled in AMcap software

        self.zoom = 1.
        self.rotate = 0
        self.pan = (0, 0)  # (row, col) center of output view


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
