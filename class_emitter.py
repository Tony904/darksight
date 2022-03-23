from PyQt5 import QtCore as qtc


class Emitter(qtc.QObject):
    emitter_signal = qtc.pyqtSignal(tuple)
