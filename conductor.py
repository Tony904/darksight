from PyQt5 import QtCore as qtc
from capture import CaptureStream


class Conductor(qtc.QObject):
    run_drawer = qtc.pyqtSignal(list, int, int)
    run_inference = qtc.pyqtSignal(list, float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caps = []
        self.canvas_w = 0
        self.canvas_h = 0
        self.inference_enabled = False
        self.inference_thresh = 0.5

    @qtc.pyqtSlot(int, int, float, list)
    def run(self, w, h, inference_thresh, caps):
        self.canvas_w = w
        self.canvas_h = h
        self.inference_thresh = inference_thresh
        self.caps = []
        for cap in caps:
            self.caps.append(CapState(cap))
        if self.inference_enabled:
            self.run_inference.emit(self.caps)
        else:
            self.run_drawer()

    @qtc.pyqtSlot()
    def run_drawer(self):
        self.run_drawer.emit(self.caps, self.w, self.h)


class CapState(qtc.QObject):
    def __init__(self, cap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = cap.uid
        self.frame = cap.frame.copy()
        self.props = cap.props.copy()
        self.detections = None
