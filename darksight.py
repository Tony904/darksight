import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import cv2
import numpy as np
import image_utils as imut
import my_utils
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
        qimg = qtg.QImage(img.data, img.shape[1], img.shape[0],
                          img.strides[0], qtg.QImage.Format_RGB888)
        qpix = qtg.QPixmap.fromImage(qimg)
        width = qpix.width()
        height = qpix.height()

        for n in range(self.ui.layout_grid_frme_capture_panels.count()):
            if n == 0:
                display_lbl = self.ui.frme_capture_panels.findChild(qtw.QLabel,
                                                                                "lbl_capture_display_pixmap")
            else:
                display_lbl = self.ui.frme_capture_panels.findChild(qtw.QLabel,
                                                                                "lbl_capture_display_pixmap_" + str(n))
            display_lbl.setPixmap(qpix)

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
        self.focus = 300
        self.thread_active = True

    @qtc.pyqtSlot(int)
    def run(self, cam_index):
        self.thread_active = True
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        # 16MP camera = 4672x3504
        # 8MP 3264x2448
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4672)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3504)
        # cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        cap.set(cv2.CAP_PROP_FOCUS, self.focus)
        focus = self.focus
        while cap.isOpened() & self.thread_active:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                cv2.putText(frame_rgb, "Focus:" + str(focus), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1,
                            cv2.LINE_AA)
                # qimg = qtg.QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0],
                #                  frame_rgb.strides[0], qtg.QImage.Format_RGB888)
                self.frame_captured.emit(frame_rgb)
                if focus != self.focus:
                    focus = self.focus
                    cap.set(cv2.CAP_PROP_FOCUS, focus)
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
