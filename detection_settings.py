from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import globals as glb


class DetectionSettings(qtw.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def setupUi(self, panel):
        self.panel = panel
        
