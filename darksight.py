import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
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

        # create main window
        self.mw = MainWindow()
        self.mw.show()


class MainWindow(qtw.QWidget):
    camera_capture_requested = qtc.pyqtSignal(int)
    focus_value_changed = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_FormMain()
        self.ui.setupUi(self)

        self.capture_active = False

        self.ui.btn_add_capture_panel.clicked.connect(self.__add_capture_panel)
        self.ui.btn_remove_capture_panel.clicked.connect(self.__remove_capture_panel)

        self.ui.spbx_cap_focus_0.valueChanged.connect(self.__send_focus_update_request)
        self.ui.spbx_cap_backlight_0.valueChanged.connect(self.__send_backlight_update_request)
        self.ui.spbx_cap_brightness_0.valueChanged.connect(self.__send_brightness_update_request)
        self.ui.spbx_cap_contrast_0.valueChanged.connect(self.__send_contrast_update_request)
        self.ui.spbx_cap_exposure_0.valueChanged.connect(self.__send_exposure_update_request)
        self.ui.spbx_cap_gain_0.valueChanged.connect(self.__send_gain_update_request)
        self.ui.spbx_cap_gamma_0.valueChanged.connect(self.__send_gamma_update_request)
        self.ui.spbx_cap_hue_0.valueChanged.connect(self.__send_hue_update_request)
        self.ui.spbx_cap_saturation_0.valueChanged.connect(self.__send_saturation_update_request)
        self.ui.spbx_cap_sharpness_0.valueChanged.connect(self.__send_sharpness_update_request)
        self.ui.spbx_cap_white_0.valueChanged.connect(self.__send_white_update_request)

        self.ui.chbx_cap_autoexposure_0.stateChanged.connect(self.__send_auto_exposure_update_request)
        self.ui.chbx_cap_autofocus_0.stateChanged.connect(self.__send_auto_focus_update_request)
        self.ui.chbx_cap_autowhite_0.stateChanged.connect(self.__send_auto_white_update_request)

        self.ui.btn_start_capture.clicked.connect(self.__send_capture_request)
        self.ui.btn_stop_capture.clicked.connect(self.__stop_capture)

        self.cap_feed = CaptureFeed()
        self.cap_thread = qtc.QThread()
        self.cap_feed.moveToThread(self.cap_thread)
        self.cap_thread.start()

        self.camera_capture_requested.connect(self.cap_feed.run)
        self.cap_feed.frame_captured.connect(self.__display_capture)

        self.showMaximized()

    def __if_cap_active(func):
        @functools.wraps(func)
        def wrapper(*args):
            if args[0].capture_active:
                return func(*args)
        return wrapper

    def __if_cap_not_active(func):
        @functools.wraps(func)
        def wrapper(*args):
            if not args[0].capture_active:
                return func(*args)
        return wrapper

    @__if_cap_active
    def __send_auto_focus_update_request(self):
        auto = int(self.ui.chbx_cap_autofocus_0.isChecked())
        self.cap_feed.update_auto_focus(auto)

    @__if_cap_active
    def __send_auto_exposure_update_request(self):
        auto = int(self.ui.chbx_cap_autoexposure_0.isChecked())
        self.cap_feed.update_auto_exposure(auto)

    @__if_cap_active
    def __send_auto_white_update_request(self):
        auto = int(self.ui.chbx_cap_autowhite_0.isChecked())
        self.cap_feed.update_auto_white_balance(auto)

    @__if_cap_active
    def __send_focus_update_request(self):
        focus = self.ui.spbx_cap_focus_0.value()
        self.cap_feed.update_focus(focus)

    @__if_cap_active
    def __send_backlight_update_request(self):
        backlight = self.ui.spbx_cap_backlight_0.value()
        self.cap_feed.update_backlight_comp(backlight)

    @__if_cap_active
    def __send_brightness_update_request(self):
        brightness = self.ui.spbx_cap_brightness_0.value()
        self.cap_feed.update_brightness(brightness)

    @__if_cap_active
    def __send_contrast_update_request(self):
        contrast = self.ui.spbx_cap_contrast_0.value()
        self.cap_feed.update_contrast(contrast)

    @__if_cap_active
    def __send_exposure_update_request(self):
        exposure = self.ui.spbx_cap_exposure_0.value()
        self.cap_feed.update_exposure(exposure)

    @__if_cap_active
    def __send_gain_update_request(self):
        gain = self.ui.spbx_cap_gain_0.value()
        self.cap_feed.update_gain(gain)

    @__if_cap_active
    def __send_gamma_update_request(self):
        gamma = self.ui.spbx_cap_gamma_0.value()
        self.cap_feed.update_gamma(gamma)

    @__if_cap_active
    def __send_hue_update_request(self):
        hue = self.ui.spbx_cap_hue_0.value()
        self.cap_feed.update_hue(hue)

    @__if_cap_active
    def __send_saturation_update_request(self):
        saturation = self.ui.spbx_cap_saturation_0.value()
        self.cap_feed.update_saturation(saturation)

    @__if_cap_active
    def __send_sharpness_update_request(self):
        sharpness = self.ui.spbx_cap_sharpness_0.value()
        self.cap_feed.update_sharpness(sharpness)

    @__if_cap_active
    def __send_white_update_request(self):
        white = self.ui.spbx_cap_white_0.value()
        self.cap_feed.update_white_balance(white)

    @qtc.pyqtSlot()
    @__if_cap_not_active
    def __send_capture_request(self):
        self.capture_active = True
        camera_index = 1
        self.__send_auto_focus_update_request()
        self.__send_auto_exposure_update_request()
        self.__send_auto_white_update_request()
        self.__send_focus_update_request()
        self.__send_brightness_update_request()
        self.__send_contrast_update_request()
        self.__send_hue_update_request()
        self.__send_saturation_update_request()
        self.__send_sharpness_update_request()
        self.__send_gamma_update_request()
        self.__send_white_update_request()
        self.__send_backlight_update_request()
        self.__send_gain_update_request()
        self.__send_exposure_update_request()
        self.camera_capture_requested.emit(camera_index)

    @qtc.pyqtSlot()
    @__if_cap_active
    def __stop_capture(self):
        self.capture_active = False
        self.cap_feed.stop()

    @qtc.pyqtSlot(np.ndarray)
    def __display_capture(self, img):
        h, w, c = img.shape
        self.ui.ledit_cap_width_0.setText(str(w))
        self.ui.ledit_cap_height_0.setText(str(h))
        self.ui.ledit_cap_channels_0.setText(str(c))
        for n in range(self.ui.layout_grid_frme_cap_panels.count()):
            s = str(n)
            chbx_pause = self.ui.frme_cap_panels.findChild(qtw.QCheckBox, "chbx_pause_" + s)
            if not chbx_pause.isChecked():
                lbl_display = self.ui.frme_cap_panels.findChild(qtw.QLabel, "lbl_cap_display_pixmap_" + s)
                sbar_hrz = self.ui.frme_cap_panels.findChild(qtw.QScrollBar, "sbar_hrz_cap_display_" + s)
                sbar_vrt = self.ui.frme_cap_panels.findChild(qtw.QScrollBar, "sbar_vrt_cap_display_" + s)
                dbsp_zoom = self.ui.frme_cap_panels.findChild(qtw.QDoubleSpinBox, "spbx_dbl_zoom_" + s)
                spbx_rotate = self.ui.frme_cap_panels.findChild(qtw.QSpinBox, "spbx_rotate_image_" + s)

                window_w = lbl_display.width()
                window_h = lbl_display.height()
                zoom = dbsp_zoom.value()  # float

                temp_window_w = int(window_w / zoom)
                temp_window_h = int(window_h / zoom)

                new_sbar_max = max(0, w - temp_window_w)
                sbar_max = sbar_hrz.maximum()
                sbar_max_no_zero = max(1, sbar_max)
                sbar_hrz_percent = sbar_hrz.value() / sbar_max_no_zero  # float
                if new_sbar_max != sbar_max:
                    sbar_hrz.setMaximum(new_sbar_max)
                    sbar_hrz.setValue(int(new_sbar_max * sbar_hrz_percent))

                new_sbar_max = max(0, h - temp_window_h)
                sbar_max = sbar_vrt.maximum()
                sbar_max_no_zero = max(1, sbar_max)
                sbar_vrt_percent = sbar_vrt.value() / sbar_max_no_zero  # float
                if new_sbar_max != sbar_max:
                    sbar_vrt.setMaximum(new_sbar_max)
                    sbar_vrt.setValue(int(new_sbar_max * sbar_vrt_percent))

                sbar_hrz_val = sbar_hrz.value()
                sbar_vrt_val = sbar_vrt.value()
                x1, = mut.min_max_clamp(0, w - temp_window_w, sbar_hrz_val)
                x2 = min(w, x1 + temp_window_w)
                y1, = mut.min_max_clamp(0, h - temp_window_h, sbar_vrt_val)
                y2 = min(h, y1 + temp_window_h)

                degrees = spbx_rotate.value()
                if degrees:
                    view_w = x2 - x1
                    view_h = y2 - y1
                    view_cx = x1 + view_w // 2
                    view_cy = y1 + view_h // 2
                    if degrees == 90 or degrees == 270:
                        x1, = mut.min_max_clamp(0, w, view_cx - view_h // 2)
                        x2 = min(w, x1 + view_h)
                        y1, = mut.min_max_clamp(0, h, view_cy - view_w // 2)
                        y2 = min(h, y1 + view_w)
                        view = img[y1:y2, x1:x2].copy()
                        if degrees == 90:
                            view = cv2.rotate(view, cv2.ROTATE_90_CLOCKWISE)
                        else:
                            view = cv2.rotate(view, cv2.ROTATE_90_COUNTERCLOCKWISE)
                    else:  # degrees == 180
                        view = img[y1:y2, x1:x2].copy()
                        view = cv2.rotate(view, cv2.ROTATE_180)
                else:
                    view = img[y1:y2, x1:x2].copy()

                qimg = qtg.QImage(view.data, view.shape[1], view.shape[0], view.strides[0], qtg.QImage.Format_RGB888)
                qimg = qimg.scaled(window_w, window_h, qtc.Qt.KeepAspectRatio)
                qpix = qtg.QPixmap.fromImage(qimg)
                lbl_display.setPixmap(qpix)

    @qtc.pyqtSlot()
    def __add_capture_panel(self):
        capture_panel = CapturePanel()
        capture_panel.setupUi(self.ui.frme_cap_panels)
        i = self.ui.layout_grid_frme_cap_panels.count()
        obj_name = self.ui.layout_grid_frme_cap_panels.itemAt(i - 1).widget().objectName()
        print("Added capture panel: " + obj_name)

    @qtc.pyqtSlot()
    def __remove_capture_panel(self):
        i = self.ui.layout_grid_frme_cap_panels.count()
        widget = self.ui.layout_grid_frme_cap_panels.itemAt(i - 1).widget()
        if i > 1:
            print("Removing capture panel: " + widget.objectName())
            self.ui.layout_grid_frme_cap_panels.removeWidget(widget)
            widget.deleteLater()
        else:
            print("Cannot delete last frame." + " (count = " + str(i) + ")")
        print('Panels: ')
        for n in range(self.ui.layout_grid_frme_cap_panels.count()):
            print(str(self.ui.layout_grid_frme_cap_panels.itemAt(n).widget().objectName()))


class CaptureFeed(qtc.QObject):
    frame_captured = qtc.pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 5000
        self.height = 4000
        self.focus = 300.
        self.auto_focus = 0
        self.brightness = 0
        self.contrast = 32
        self.hue = 0
        self.saturation = 64
        self.sharpness = 3
        self.gamma = 100
        self.white_balance = 4600
        self.auto_white_balance = 1
        self.backlight_comp = 1
        self.gain = 0
        self.exposure = -6
        self.auto_exposure = 1  # if disabled, must be re-enabled in AMcap software

    @qtc.pyqtSlot(int)
    def run(self, cam_index):
        self.thread_active = True
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        # 16MP camera = 4672x3504
        # 8MP 3264x2448
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        focus = self.focus
        auto_focus = self.auto_focus
        brightness = self.brightness
        contrast = self.contrast
        hue = self.hue
        saturation = self.saturation
        sharpness = self.sharpness
        gamma = self.gamma
        white_balance = self.white_balance
        auto_white_balance = self.auto_white_balance
        backlight_comp = self.backlight_comp
        gain = self.gain
        exposure = self.exposure
        auto_exposure = self.auto_exposure

        # cap.set(cv2.CAP_PROP_AUTOFOCUS, auto_focus)
        if not auto_focus:
            cap.set(cv2.CAP_PROP_FOCUS, focus)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        cap.set(cv2.CAP_PROP_HUE, hue)
        cap.set(cv2.CAP_PROP_SATURATION, saturation)
        cap.set(cv2.CAP_PROP_GAMMA, gamma)
        cap.set(cv2.CAP_PROP_AUTO_WB, auto_white_balance)
        if not auto_white_balance:
            cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, white_balance)
            cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, white_balance)
        cap.set(cv2.CAP_PROP_BACKLIGHT, backlight_comp)
        cap.set(cv2.CAP_PROP_GAIN, gain)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)
        if not auto_exposure:
            cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        count = 0
        while cap.isOpened() and self.thread_active:
            ret, frame = cap.read()
            count = count + 1
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_captured.emit(frame_rgb)
                if not auto_focus == self.auto_focus:
                    auto_focus = self.auto_focus
                    cap.set(cv2.CAP_PROP_AUTOFOCUS, auto_focus)
                    print("Auto-focus set to: " + str(auto_focus))
                    print("Auto-focus is: " + str(cap.get(cv2.CAP_PROP_AUTOFOCUS)))
                elif abs(focus - self.focus) >= 1:
                    focus = self.focus
                    if not auto_focus:
                        cap.set(cv2.CAP_PROP_FOCUS, focus)
                        print("Focus set to: " + str(focus))
                        print("Focus is: " + str(cap.get(cv2.CAP_PROP_FOCUS)))
                elif not auto_white_balance == self.auto_white_balance:
                    auto_white_balance = self.auto_white_balance
                    cap.set(cv2.CAP_PROP_AUTO_WB, auto_white_balance)
                elif abs(white_balance - self.white_balance) >= 1:
                    white_balance = self.white_balance
                    if not auto_white_balance:
                        cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, self.white_balance)
                        cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, self.white_balance)
                elif not auto_exposure == self.auto_exposure:
                    auto_exposure = self.auto_exposure
                    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)
                elif abs(exposure - self.exposure) >= 1:
                    exposure = self.exposure
                    if not auto_exposure:
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
                elif abs(backlight_comp - self.backlight_comp) >= 1:
                    backlight_comp = self.backlight_comp
                    cap.set(cv2.CAP_PROP_BACKLIGHT, backlight_comp)
                    print("Backlight comp set to: " + str(backlight_comp))
                    print("Backlight comp is: " + str(cap.get(cv2.CAP_PROP_BACKLIGHT)))
            else:
                self.stop()
                print("Capture read unsuccessful. Cam index: " + str(cam_index))

        cap.release()
        print("Capture stopped. Cam index: " + str(cam_index))

    def stop(self):
        self.thread_active = False

    def update_focus(self, focus):
        self.focus = focus

    def update_auto_focus(self, auto):
        self.auto_focus = auto

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

    def update_white_balance(self, white_balance):
        self.white_balance = white_balance

    def update_auto_white_balance(self, auto):
        self.auto_white_balance = auto

    def update_backlight_comp(self, backlight_comp):
        self.backlight_comp = backlight_comp

    def update_gain(self, gain):
        self.gain = gain

    def update_exposure(self, exposure):
        self.exposure = exposure

    def update_auto_exposure(self, auto):
        self.auto_exposure = auto


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
