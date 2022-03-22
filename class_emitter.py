from PyQt5 import QtCore as qtc


class Emitter(qtc.QObject):
    emitter_signal = qtc.pyqtSignal(int, list)

    # def emit_signal(self, *args):
    #     lst = list(args)
    #     self.emitter_signal.emit(lst)
