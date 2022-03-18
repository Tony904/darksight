import sys
import time

from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import darknet
import cv2
import numpy as np
import functools
import image_utils as imut
import my_utils as mut
from class_cap_panel import CapturePanel
from darksight_designer import Ui_FormMain


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        self.mw = MainWindow()
        self.mw.show()


class MainWindow(qtw.QWidget):
    run_stream = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_FormMain()
        self.ui.setupUi(self)
        self.panels = []
        self.streams = []
        self.qthreads = []

        self.ui.btn_add_capture_panel.clicked.connect(self._add_capture_panel)
        self.ui.btn_remove_capture_panel.clicked.connect(self._remove_capture_panel)

        self.showMaximized()

    def load_darknet(self):
        cfg_file = "D:/yolo_v4/darknet/build/darknet/x64/cfg/yolov4-csp.cfg"
        data_file = "D:/yolo_v4/darknet/build/darknet/x64/data/obj.data"
        weights_file = "D:/yolo_v4/darknet/build/darknet/x64/training_backup/yolov4-csp_last.weights"
        batch_size = 1
        global network, class_names, class_colors, darknet_w, darknet_h
        network, class_names, class_colors = darknet.load_network(cfg_file, data_file, weights_file, batch_size)
        darknet_w = darknet.network_width(network)
        darknet_h = darknet.network_height(network)

        self.inference = Inference()
        self.inference_qthread = qtc.QThread()
        self.inference.moveToThread(self.inference_qthread)
        self.inference_qthread.start()
        self.inference.predicted.connect(self.relay_detections)
        self.draw_detections = DrawDetections()
        self.draw_detections_qthread = qtc.QThread()
        self.draw_detections.moveToThread(self.draw_detections_qthread)
        self.draw_detections_qthread.start()
        self.draw_detections.detections_drawn.connect(self.relay_predicted_image)

    def relay_detections(self, detections):
        self.draw_detections.update_detections(detections)

    def relay_input_image(self, img):
        self.inference.update_image(img)

    def relay_predicted_image(self, img):
        pass

    def _if_cap_active(func):
        @functools.wraps(func)
        def wrapper(*args):
            if args[0].panels[args[1]].s > -1:
                return func(*args)
        return wrapper

    @qtc.pyqtSlot()
    def _add_capture_panel(self):
        panel = CapturePanel()
        panel.setupUi(self.ui.frme_cap_panels)
        panel.capture_requested.connect(self.setup_capture)
        panel.stop_capture_requested.connect(self.stop_stream)
        panel.update_autowhite_requested.connect(self._update_autowhite)
        panel.update_autofocus_requested.connect(self._update_autofocus)
        panel.update_autoexposure_requested.connect(self._update_autoexposure)
        panel.update_white_requested.connect(self._update_white)
        panel.update_focus_requested.connect(self._update_focus)
        panel.update_exposure_requested.connect(self._update_exposure)
        panel.update_backlight_requested.connect(self._update_backlight)
        panel.update_brightness_requested.connect(self._update_brightness)
        panel.update_contrast_requested.connect(self._update_contrast)
        panel.update_gain_requested.connect(self._update_gain)
        panel.update_gamma_requested.connect(self._update_gamma)
        panel.update_hue_requested.connect(self._update_hue)
        panel.update_saturation_requested.connect(self._update_saturation)
        panel.update_sharpness_requested.connect(self._update_sharpness)

        self.panels.append(panel)

        i = self.ui.layout_grid_frme_cap_panels.count()
        obj_name = self.ui.layout_grid_frme_cap_panels.itemAt(i - 1).widget().objectName()
        print("Added capture panel: " + obj_name)

    @qtc.pyqtSlot(int, int)
    def setup_capture(self, p, c):
        print("Setting up capture. p=" + str(p) + " c=" + str(c))
        if self.panels[p].s > -1:
            self.stop_stream(p)
        c_open = True
        s = -1
        for n in range(len(self.streams)):
            if c == self.streams[n].c:
                c_open = False
                s = n
                break
        if c_open:
            cap_stream = CaptureStream()
            cap_thread = qtc.QThread()
            cap_stream.moveToThread(cap_thread)
            cap_thread.start()
            self.streams.append(cap_stream)
            self.qthreads.append(cap_thread)
            cap_stream.frame_captured.connect(self.panels[p].display_capture)
            cap_stream.connected_panels.append(p)
            self.panels[p].c = c
            self.panels[p].s = len(self.streams) - 1
            self.run_stream.connect(cap_stream.run)
            self.run_stream.emit(c)
            self.run_stream.disconnect(cap_stream.run)
        else:
            self.streams[s].frame_captured.connect(self.panels[p].display_capture)
            self.streams[s].connected_panels.append(p)
            self.panels[p].c = c
            self.panels[p].s = s

    @_if_cap_active
    def stop_stream(self, p):
        s = self.panels[p].s
        self.streams[s].frame_captured.disconnect(self.panels[p].display_capture)
        self.panels[p].c = -1
        self.panels[p].s = -1
        self.streams[s].connected_panels.remove(p)
        if not len(self.streams[s].connected_panels):
            self.streams[s].stop()
            del self.streams[s]
            self.qthreads[s].quit()
            del self.qthreads[s]

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_autofocus(self, p, x):
        self.streams[self.panels[p].s].update_autofocus(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_autoexposure(self, p, x):
        self.streams[self.panels[p].s].update_autoexposure(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_autowhite(self, p, x):
        self.streams[self.panels[p].s].update_autowhite(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_focus(self, p, x):
        self.streams[self.panels[p].s].update_focus(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_brightness(self, p, x):
        self.streams[self.panels[p].s].update_brightness(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_contrast(self, p, x):
        self.streams[self.panels[p].s].update_contrast(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_hue(self, p, x):
        self.streams[self.panels[p].s].update_hue(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_saturation(self, p, x):
        self.streams[self.panels[p].s].update_saturation(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_sharpness(self, p, x):
        self.streams[self.panels[p].s].update_sharpness(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_gamma(self, p, x):
        self.streams[self.panels[p].s].update_gamma(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_white(self, p, x):
        self.streams[self.panels[p].s].update_white(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_backlight(self, p, x):
        self.streams[self.panels[p].s].update_backlight(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_gain(self, p, x):
        self.streams[self.panels[p].s].update_gain(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _update_exposure(self, p, x):
        self.streams[self.panels[p].s].update_exposure(x)

    @qtc.pyqtSlot(int, int)
    @_if_cap_active
    def _remove_capture_panel(self):
        i = self.ui.layout_grid_frme_cap_panels.count()
        if i > 0:
            widget = self.ui.layout_grid_frme_cap_panels.itemAt(i - 1).widget()
            print("Removing capture panel: " + widget.objectName())
            if len(self.panels):
                self.panels.pop()
            self.ui.layout_grid_frme_cap_panels.removeWidget(widget)
            widget.deleteLater()
        else:
            print("Cannot delete last frame." + " (count = " + str(i) + ")")
        print('Panels: ')
        for n in range(self.ui.layout_grid_frme_cap_panels.count()):
            print(str(self.ui.layout_grid_frme_cap_panels.itemAt(n).widget().objectName()))


class CaptureStream(qtc.QObject):
    frame_captured = qtc.pyqtSignal(np.ndarray, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = -1
        self.connected_panels = []
        self.cap_active = False
        self.width = 5000
        self.height = 4000
        self.focus = 300.
        self.autofocus = 0
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

        self.darknet_img = None

    @qtc.pyqtSlot(int)
    def run(self, cam_index):
        self.c = cam_index
        self.cap_active = True
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        # 16MP camera = 4672x3504
        # 8MP 3264x2448
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        focus = self.focus
        autofocus = self.autofocus
        brightness = self.brightness
        contrast = self.contrast
        hue = self.hue
        saturation = self.saturation
        sharpness = self.sharpness
        gamma = self.gamma
        white = self.white
        autowhite = self.autowhite
        backlight = self.backlight
        gain = self.gain
        exposure = self.exposure
        autoexposure = self.autoexposure

        cap.set(cv2.CAP_PROP_AUTOFOCUS, autofocus)
        if not autofocus:
            cap.set(cv2.CAP_PROP_FOCUS, focus)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        cap.set(cv2.CAP_PROP_HUE, hue)
        cap.set(cv2.CAP_PROP_SATURATION, saturation)
        cap.set(cv2.CAP_PROP_GAMMA, gamma)
        cap.set(cv2.CAP_PROP_AUTO_WB, autowhite)
        if not autowhite:
            cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, white)
            cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, white)
        cap.set(cv2.CAP_PROP_BACKLIGHT, backlight)
        cap.set(cv2.CAP_PROP_GAIN, gain)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, autoexposure)
        if not autoexposure:
            cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        while cap.isOpened() and self.cap_active:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_captured.emit(frame_rgb, cam_index)
                if not autofocus == self.autofocus:
                    autofocus = self.autofocus
                    cap.set(cv2.CAP_PROP_AUTOFOCUS, autofocus)
                    print("Auto-focus set to: " + str(autofocus))
                    print("Auto-focus is: " + str(cap.get(cv2.CAP_PROP_AUTOFOCUS)))
                elif abs(focus - self.focus) >= 1:
                    focus = self.focus
                    if not autofocus:
                        cap.set(cv2.CAP_PROP_FOCUS, focus)
                        print("Focus set to: " + str(focus))
                        print("Focus is: " + str(cap.get(cv2.CAP_PROP_FOCUS)))
                elif not autowhite == self.autowhite:
                    autowhite = self.autowhite
                    cap.set(cv2.CAP_PROP_AUTO_WB, autowhite)
                elif abs(white - self.white) >= 1:
                    white = self.white
                    if not autowhite:
                        cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, white)
                        cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, white)
                elif not autoexposure == self.autoexposure:
                    autoexposure = self.autoexposure
                    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, autoexposure)
                elif abs(exposure - self.exposure) >= 1:
                    exposure = self.exposure
                    if not autoexposure:
                        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
                        print("Exposure set to: " + str(exposure))
                        print("Exposure is: " + str(cap.get(cv2.CAP_PROP_EXPOSURE)))
                    else:
                        print("auto exposure = 1. no change.")
                elif abs(gain - self.gain) >= 1:
                    gain = self.gain
                    cap.set(cv2.CAP_PROP_GAIN, gain)
                    print("Gain set to: " + str(gain))
                    print("Gain is: " + str(cap.get(cv2.CAP_PROP_GAIN)))
                elif abs(gamma - self.gamma) >= 1:
                    gamma = self.gamma
                    cap.set(cv2.CAP_PROP_GAMMA, gamma)
                    print("Gamma set to: " + str(gamma))
                    print("Gamma is: " + str(cap.get(cv2.CAP_PROP_GAMMA)))
                elif abs(brightness - self.brightness) >= 1:
                    brightness = self.brightness
                    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
                    print("Brightness set to: " + str(brightness))
                    print("Brightness is: " + str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
                elif abs(contrast - self.contrast) >= 1:
                    contrast = self.contrast
                    cap.set(cv2.CAP_PROP_CONTRAST, contrast)
                    print("Contrast set to: " + str(contrast))
                    print("Contrast is: " + str(cap.get(cv2.CAP_PROP_CONTRAST)))
                elif abs(sharpness - self.sharpness) >= 1:
                    sharpness = self.sharpness
                    cap.set(cv2.CAP_PROP_SHARPNESS, sharpness)
                    print("Sharpness set to: " + str(sharpness))
                    print("Sharpness is: " + str(cap.get(cv2.CAP_PROP_SHARPNESS)))
                elif abs(saturation - self.saturation) >= 1:
                    saturation = self.saturation
                    cap.set(cv2.CAP_PROP_SATURATION, saturation)
                    print("Saturation set to: " + str(saturation))
                    print("Saturation is: " + str(cap.get(cv2.CAP_PROP_SATURATION)))
                elif abs(hue - self.hue) >= 1:
                    hue = self.hue
                    cap.set(cv2.CAP_PROP_HUE, hue)
                    print("Hue set to: " + str(hue))
                    print("Hue is: " + str(cap.get(cv2.CAP_PROP_HUE)))
                elif abs(backlight - self.backlight) >= 1:
                    backlight = self.backlight
                    cap.set(cv2.CAP_PROP_BACKLIGHT, backlight)
                    print("Backlight comp set to: " + str(backlight))
                    print("Backlight comp is: " + str(cap.get(cv2.CAP_PROP_BACKLIGHT)))
            else:
                self.stop()
                print("Capture read unsuccessful. Cam index: " + str(cam_index))

        cap.release()
        print("Capture stopped. Cam index: " + str(cam_index))

    def stop(self):
        self.cap_active = False

    def update_focus(self, focus):
        self.focus = focus

    def update_autofocus(self, auto):
        self.autofocus = auto

    def update_brightness(self, brightness):
        self.brightness = brightness

    def update_contrast(self, contrast):
        self.contrast = contrast

    def update_hue(self, hue):
        self.hue = hue

    def update_saturation(self, saturation):
        self.saturation = saturation

    def update_sharpness(self, sharpness):
        self.sharpness = sharpness

    def update_gamma(self, gamma):
        self.gamma = gamma

    def update_white(self, white):
        self.white = white

    def update_autowhite(self, auto):
        self.autowhite = auto

    def update_backlight(self, backlight):
        self.backlight = backlight

    def update_gain(self, gain):
        self.gain = gain

    def update_exposure(self, exposure):
        self.exposure = exposure

    def update_autoexposure(self, auto):
        self.autoexposure = auto


class Inference(qtc.QObject):
    predicted = qtc.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.darknet_image = None
        self.thresh = 0.5
        self.active = False

    def run(self):
        self.active = True
        while self.active:
            img = self.darknet_image.copy()
            detections = darknet.detect_image(network, class_names, img, self.thresh)
            self.predicted.emit(detections)
            darknet.free_image(img)

    def update_image(self, img):
        self.darknet_image = img

    def update_thresh(self, thresh):
        self.thresh = thresh


class DrawDetections(qtc.QObject):
    detections_drawn = qtc.pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.img = None
        self.detections = []
        self.thresh = 0.5
        self.active = False

    def run(self):
        self.active = True
        while self.active:
            if self.img:
                img = self.img.copy()
                detections = self.detections.copy()
                for label, confidence, bbox in detections:
                    print("label: " + str(label) + " confidence: " + str(confidence) + " bbox: " + str(bbox))
                    # draw bboxes on img
                self.detections_drawn.emit(img)

    def update_image(self, img):
        self.img = img.copy()

    def update_detections(self, detections):
        self.detections = detections.copy()


if __name__ == "__main__":
    app = MainApp(sys.argv)
    network = None
    class_names = None
    class_colors = None
    darknet_w = None
    darknet_h = None
    sys.exit(app.exec_())
