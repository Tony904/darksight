from PyQt5 import QtCore as qtc
from capture import CaptureStream


class Conductor(qtc.QObject):
    sg_run_drawer = qtc.pyqtSignal(list, int, int)
    sg_run_inference = qtc.pyqtSignal(list, float)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caps = []
        self.canvas_w = 0
        self.canvas_h = 0
        self.inference_enabled = False

    @qtc.pyqtSlot(int, int, float, list)
    def run(self, w, h, inference_thresh, caps):
        self.canvas_w = w
        self.canvas_h = h
        self.caps = []
        for cap in caps:
            self.caps.append(CapState(cap))
        if self.inference_enabled:
            self.sg_run_inference.emit(self.caps, inference_thresh)
        else:
            self.run_drawer()

    @qtc.pyqtSlot()
    def run_drawer(self):
        self.sg_run_drawer.emit(self.caps, self.canvas_w, self.canvas_h)


class CapState(qtc.QObject):
    def __init__(self, cap, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = cap.uid
        self.frame = cap.frame.copy()
        self.props = cap.props.copy()
        self.detections = None
