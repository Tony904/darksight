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


class MainWindow(qtw.QWidget):
    camera_capture_requested = qtc.pyqtSignal(int)
    focus_value_changed = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_FormMain()
        self.ui.setupUi(self)

        # self.ui.frme_camera_focus_panel.findChild(qtw.QLabel, "lbl_static_focus").setText("hi")

        self.ui.btn_add_capture_panel.clicked.connect(self.__add_capture_panel)
        self.ui.btn_remove_capture_panel.clicked.connect(self.__remove_capture_panel)

        self.ui.btn_start_capture.clicked.connect(self.__send_capture_request)
        self.ui.sbar_vrt_camera_focus.valueChanged.connect(self.__update_focus_label)

        self.cap_feed = CaptureFeed()
        self.cap_thread = qtc.QThread()
        self.cap_feed.moveToThread(self.cap_thread)
        self.cap_thread.start()

        self.cap_feed.frame_captured.connect(self.__display_capture)
        self.camera_capture_requested.connect(self.cap_feed.run)
        self.ui.btn_stop_capture.clicked.connect(self.__stop_capture)

        self.showMaximized()

    @qtc.pyqtSlot()
    def __stop_capture(self):
        self.ui.sbar_vrt_camera_focus.valueChanged.disconnect(self.__send_focus_update_request)
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

                x1, = mut.min_max_clamp(0, w - temp_window_w, sbar_hrz.value())
                x2 = min(w, x1 + temp_window_w)
                y1, = mut.min_max_clamp(0, h - temp_window_h, sbar_vrt.value())
                y2 = min(h, y1 + temp_window_h)

                view = img[y1:y2, x1:x2].copy()
                qimg = qtg.QImage(view.data, view.shape[1], view.shape[0], view.strides[0], qtg.QImage.Format_RGB888)
                qimg = qimg.scaledToWidth(window_w)  # aspect ratio is preserved
                qpix = qtg.QPixmap.fromImage(qimg)
                lbl_display.setPixmap(qpix)

        # if not self.ui.chbx_freeze_frame.isChecked():
        #     scale = self.ui.spbx_dbl_zoom.value()
        #     w, _ = my_utils.scaled_image_dimensions(width, height, scale)
        #     qpix1 = qpix.scaledToWidth(w)
        #     self.ui.lbl_capture_display_pixmap.setPixmap(qpix1)

    @qtc.pyqtSlot()
    def __send_focus_update_request(self):
        focus = self.ui.sbar_vrt_camera_focus.value()
        self.cap_feed.update_focus(focus)

    @qtc.pyqtSlot()
    def __send_capture_request(self):
        self.ui.sbar_vrt_camera_focus.valueChanged.connect(self.__send_focus_update_request)
        camera_index = 1
        self.camera_capture_requested.emit(camera_index)

    @qtc.pyqtSlot()
    def __update_focus_label(self):
        focus = self.ui.sbar_vrt_camera_focus.value()
        self.ui.lbl_camera_focus_value.setText(str(focus))

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
        self.focus = float(300.0)
        self.thread_active = True

    @qtc.pyqtSlot(int)
    def run(self, cam_index):
        self.thread_active = True
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        # 16MP camera = 4672x3504
        # 8MP 3264x2448
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 5000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 4000)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)  # 0 = autofocus off, 1 = autofocus on
        cap.set(cv2.CAP_PROP_FOCUS, self.focus)
        while cap.isOpened() & self.thread_active:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                true_focus = cap.get(cv2.CAP_PROP_FOCUS)
                cv2.putText(frame_rgb, "Focus:" + str(true_focus), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA)
                self.frame_captured.emit(frame_rgb)
                if abs(true_focus - self.focus) >= 1:
                    cap.set(cv2.CAP_PROP_FOCUS, self.focus)
            else:
                self.stop()

        cap.release()

    def stop(self):
        self.thread_active = False

    def update_focus(self, focus):
        self.focus = focus


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
