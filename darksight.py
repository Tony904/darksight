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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_FormMain()
        self.ui.setupUi(self)

        self.ui.btn_add_capture_panel.clicked.connect(self._add_capture_panel)
        self.ui.btn_remove_capture_panel.clicked.connect(self._remove_capture_panel)

        self.showMaximized()

    @qtc.pyqtSlot()
    def _add_capture_panel(self):
        self.capture_panel = CapturePanel()
        self.capture_panel.setupUi(self.ui.frme_cap_panels)
        i = self.ui.layout_grid_frme_cap_panels.count()
        obj_name = self.ui.layout_grid_frme_cap_panels.itemAt(i - 1).widget().objectName()
        print("Added capture panel: " + obj_name)

    @qtc.pyqtSlot()
    def _remove_capture_panel(self):
        i = self.ui.layout_grid_frme_cap_panels.count()
        widget = self.ui.layout_grid_frme_cap_panels.itemAt(i - 1).widget()
        if i > 0:
            print("Removing capture panel: " + widget.objectName())
            self.ui.layout_grid_frme_cap_panels.removeWidget(widget)
            widget.deleteLater()
        else:
            print("Cannot delete last frame." + " (count = " + str(i) + ")")
        print('Panels: ')
        for n in range(self.ui.layout_grid_frme_cap_panels.count()):
            print(str(self.ui.layout_grid_frme_cap_panels.itemAt(n).widget().objectName()))


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
