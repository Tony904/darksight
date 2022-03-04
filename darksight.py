import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import cv2
import numpy as np
import image_utils as imut
import my_utils as mut
from capture_panel_class import CapturePanel
from darksight_designer import Ui_FormMain


class MainApp(qtw.QApplication):

    def __init__(self, argv):
        super().__init__(argv)

        # create main window
        self.mw = MainWindow()
        self.mw.show()

def if_cap_active(func):
    def wrapper(widget):
        if widget.capture_active:
            func(widget)
    return wrapper

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

        self.ui.sbar_vrt_camera_focus_0.valueChanged.connect(self.__send_focus_update_request)
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

        self.ui.btn_start_capture.clicked.connect(self.__send_capture_request)
        self.ui.btn_stop_capture.clicked.connect(self.__stop_capture)

        self.cap_feed = CaptureFeed()
        self.cap_thread = qtc.QThread()
        self.cap_feed.moveToThread(self.cap_thread)
        self.cap_thread.start()

        self.camera_capture_requested.connect(self.cap_feed.run)
        self.cap_feed.frame_captured.connect(self.__display_capture)

        self.showMaximized()

    @qtc.pyqtSlot()
    @if_cap_active
    def __send_focus_update_request(self):
        focus = self.ui.sbar_vrt_camera_focus_0.value()
        self.ui.lbl_camera_focus_value_0.setText(str(focus))
        if self.capture_active:
            self.cap_feed.update_focus(focus)

    def __send_backlight_update_request(self):
        backlight = self.ui.spbx_cap_backlight_0.value()
        if self.capture_active:
            self.cap_feed.update_backlight_comp(backlight)

    def __send_brightness_update_request(self):
        brightness = self.ui.spbx_cap_brightness_0.value()
        pass

    def __send_contrast_update_request(self):
        pass

    def __send_exposure_update_request(self):
        pass

    def __send_gain_update_request(self):
        pass

    def __send_gamma_update_request(self):
        pass

    def __send_hue_update_request(self):
        pass

    def __send_saturation_update_request(self):
        pass

    def __send_sharpness_update_request(self):
        pass

    def __send_white_update_request(self):
        pass

    @qtc.pyqtSlot()
    def __send_capture_request(self):
        if not self.capture_active:
            self.capture_active = True
            camera_index = 1
            self.camera_capture_requested.emit(camera_index)

    @qtc.pyqtSlot()
    @if_cap_active
    def __stop_capture(self):
        self.capture_active = False
        self.cap_feed.stop()

    @qtc.pyqtSlot(np.ndarray)
    def __display_capture(self, img):
        h, w, c = img.shape
        self.ui.ledit_camera_resolution.setText("W: " + str(w) + ", H: " + str(h) + ", C: " + str(c))
        for n in range(self.ui.layout_grid_frme_capture_panels.count()):
            s = str(n)
            chbx_freeze = self.ui.frme_capture_panels.findChild(qtw.QCheckBox, "chbx_freeze_frame_" + s)
            if not chbx_freeze.isChecked():
                lbl_display = self.ui.frme_capture_panels.findChild(qtw.QLabel, "lbl_capture_display_pixmap_" + s)
                sbar_hrz = self.ui.frme_capture_panels.findChild(qtw.QScrollBar, "sbar_hzt_capture_display_" + s)
                sbar_vrt = self.ui.frme_capture_panels.findChild(qtw.QScrollBar, "sbar_vrt_capture_display_" + s)
                dbsp_zoom = self.ui.frme_capture_panels.findChild(qtw.QDoubleSpinBox, "spbx_dbl_zoom_" + s)
                spbx_rotate = self.ui.frme_capture_panels.findChild(qtw.QSpinBox, "spbx_rotate_image_" + s)

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
        capture_panel.setupUi(self.ui.frme_capture_panels)
        i = self.ui.layout_grid_frme_capture_panels.count()
        obj_name = self.ui.layout_grid_frme_capture_panels.itemAt(i - 1).widget().objectName()
        print("Added capture panel: " + obj_name)

    @qtc.pyqtSlot()
    def __remove_capture_panel(self):
        i = self.ui.layout_grid_frme_capture_panels.count()
        widget = self.ui.layout_grid_frme_capture_panels.itemAt(i - 1).widget()
        if i > 1:
            print("Removing capture panel: " + widget.objectName())
            self.ui.layout_grid_frme_capture_panels.removeWidget(widget)
            widget.deleteLater()
        else:
            print("Cannot delete last frame." + " (count = " + str(i) + ")")
        print('Panels: ')
        for n in range(self.ui.layout_grid_frme_capture_panels.count()):
            print(str(self.ui.layout_grid_frme_capture_panels.itemAt(n).widget().objectName()))



class CaptureFeed(qtc.QObject):
    frame_captured = qtc.pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 5000
        self.height = 4000
        self.focus = 300.
        self.auto_focus = False
        self.brightness = 1
        self.auto_brightness = False
        self.contrast = 1
        self.auto_contrast = False
        self.hue = 1
        self.auto_hue = False
        self.saturation = 1
        self.auto_saturation = False
        self.sharpness = 1
        self.auto_sharpness = False
        self.gamma = 1
        self.auto_gamma = False
        self.white_balance = 1
        self.auto_white_balance = True
        self.backlight_comp = 0
        self.auto_backlight_comp = False
        self.gain = 1
        self.auto_gain = False
        self.exposure = 1
        self.auto_exposure = True

        self.thread_active = True

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

        cap.set(cv2.CAP_PROP_AUTOFOCUS, auto_focus)
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

        while cap.isOpened() & self.thread_active:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_captured.emit(frame_rgb)
                if not auto_focus == self.auto_focus:
                    auto_focus = self.auto_focus
                    cap.set(cv2.CAP_PROP_AUTOFOCUS, auto_focus)
                elif abs(focus - self.focus) >= 1:
                    focus = self.focus
                    if not auto_focus:
                        cap.set(cv2.CAP_PROP_FOCUS, focus)
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
                elif abs(gain - self.gain) >= 1:
                    gain = self.gain
                    cap.set(cv2.CAP_PROP_GAIN, gain)
                elif abs(gamma - self.gamma) >= 1:
                    gamma = self.gamma
                    cap.set(cv2.CAP_PROP_GAMMA, self.gamma)
                elif abs(brightness - self.brightness) >= 1:
                    brightness = self.brightness
                    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
                elif abs(contrast - self.contrast) >= 1:
                    contrast = self.contrast
                    cap.set(cv2.CAP_PROP_CONTRAST, contrast)
                elif abs(sharpness - self.sharpness) >= 1:
                    sharpness = self.sharpness
                    cap.set(cv2.CAP_PROP_SHARPNESS, self.sharpness)
                elif abs(saturation - self.saturation) >= 1:
                    saturation = self.saturation
                    cap.set(cv2.CAP_PROP_SATURATION, self.saturation)
                elif abs(hue - self.hue) >= 1:
                    hue = self.hue
                    cap.set(cv2.CAP_PROP_HUE, self.hue)
                elif abs(backlight_comp - self.backlight_comp) >= 1:
                    backlight_comp = self.backlight_comp
                    cap.set(cv2.CAP_PROP_BACKLIGHT, backlight_comp)
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

    def update_auto_brightness(self, auto):
        self.auto_brightness = auto

    def update_contrast(self, contrast):
        self.contrast = contrast

    def update_auto_contrast(self, auto):
        self.auto_contrast = auto

    def update_hue(self, hue):
        self.hue = hue

    def update_auto_hue(self, auto):
        self.auto_hue = auto

    def update_saturation(self, saturation):
        self.saturation = saturation

    def update_auto_saturation(self, auto):
        self.auto_saturation = auto

    def update_sharpness(self, sharpness):
        self.sharpness = sharpness

    def update_auto_sharpness(self, auto):
        self.auto_sharpness = auto

    def update_gamma(self, gamma):
        self.gamma = gamma

    def update_auto_gamma(self, auto):
        self.auto_gamma = auto

    def update_white_balance(self, white_balance):
        self.white_balance = white_balance

    def update_auto_white_balance(self, auto):
        self.auto_white_balance = auto

    def update_backlight_comp(self, backlight_comp):
        self.backlight_comp = backlight_comp

    def update_auto_backlight_comp(self, auto):
        self.auto_backlight_comp = auto

    def update_gain(self, gain):
        self.gain = gain

    def update_auto_gain(self, auto):
        self.auto_gain = auto

    def update_exposure(self, exposure):
        self.exposure = exposure

    def update_auto_exposure(self, auto):
        self.auto_exposure = auto


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
