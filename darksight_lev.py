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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_form_main_lev()
        self.ui.setupUi(self)

        self.caps = []
        self.cap_qthreads = []
        self.drawers = []
        self.drawer_qthreads = []
        self.emitters = []

        self._init_connect_signals_to_slots()
        self.pixmap_ndarr = None

        self.showMaximized()

    def _init_connect_signals_to_slots(self):
        self.ui.btn_start_cap_2.clicked.connect(
            lambda state: self.create_capture(self.ui.ledit_cam_index_2.text(), 0))
        self.ui.btn_start_cap_3.clicked.connect(
            lambda state: self.create_capture(self.ui.ledit_cam_index_3.text(), 1))
        self.ui.btn_start_cap_4.clicked.connect(
            lambda state: self.create_capture(self.ui.ledit_cam_index_4.text(), 2))
        self.ui.btn_start_cap_5.clicked.connect(
            lambda state: self.create_capture(self.ui.ledit_cam_index_5.text(), 3))
        print("Successfully connected _init_ signals and slots.")

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
            self.drawers.append(drawer)
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

    def create_capture(self, cstr, uid):
        c = None
        print("ledit_cam_index_2.text() = " + self.ui.ledit_cam_index_2.text())
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
                cap.frame_captured.connect(self.display_handler)

                self.run_capture.connect(cap.run)
                self.run_capture.emit()
                self.run_capture.disconnect(cap.run)

    def stop_capture(self, uid):
        print("Attempting to stop CaptureStream uid=" + str(uid))
        for n in range(len(self.caps)):
            if uid == self.caps[n].uid:
                self.caps[n].stop()
                self.caps[n].frame_captured.disconnect(self.display_handler)
                del self.caps[n]
                self.cap_qthreads[n].quit()
                del self.cap_qthreads[n]

    def display_handler(self, ndarr, uid):
        pix_w = self.ui.lbl_main_pixmap.height()
        pix_h = self.ui.lbl_main_pixmap.width()
        w = pix_w // 2
        h = pix_h // 2
        img = cv2.resize(ndarr, (w, h), interpolation=cv2.INTER_LINEAR)
        if self.pixmap_ndarr is None:
            self.pixmap_ndarr = np.zeros((pix_h, pix_w, 3), dtype=ndarr.dtype)
        else:
            self.pixmap_ndarr = cv2.resize(self.pixmap_ndarr, (pix_w, pix_h), interpolation=cv2.INTER_LINEAR)
        if 0 <= uid <= 3:
            top, bottom, left, right = None, None, None, None
            if uid == 0:
                top, bottom, left, right = 0, h, 0, w
                self.pixmap_ndarr[top:bottom, left:right] = img.copy()
            elif uid == 1:
                top, bottom, left, right = 0, h, w, pix_w
                self.pixmap_ndarr[top:bottom, left:right] = img.copy()
            elif uid == 2:
                top, bottom, left, right = h, pix_h, 0, w
                self.pixmap_ndarr[top:bottom, left:right] = img.copy()
            elif uid == 3:
                top, bottom, left, right = h, pix_h, w, pix_w
                self.pixmap_ndarr[top:bottom, left:right] = img.copy()
            qimg = qtg.QImage(self.pixmap_ndarr.data, self.pixmap_ndarr.shape[1], self.pixmap_ndarr.shape[0],
                              self.pixmap_ndarr.strides[0], qtg.QImage.Format_RGB888)
            qpix = qtg.QPixmap.fromImage(qimg)
            self.ui.lbl_main_pixmap.setPixmap(qpix)
        else:
            print("Unexpected uid value.")


class CaptureStream(qtc.QObject):
    frame_captured = qtc.pyqtSignal(np.ndarray, int)

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
                self.frame_captured.emit(frame_rgb, self.uid)
        self.cap.release()

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
