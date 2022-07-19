from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import cv2
import numpy as np
import image_utils as imut


class Conductor(qtc.QObject):
    run_drawer = qtc.pyqtSignal(list, int, int)
    run_inference = qtc.pyqtSignal(list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = [None, None, None, None]  # index = uid /// element = (ndarray, CaptureProperties, detections)
        self.window_w = None
        self.window_h = None
        self.inference_enabled = False

    @qtc.pyqtSlot()
    def run(self):
        if self.inference_enabled:
            ndarrs = []
            for uid in self.queue:
                if uid is not None:
                    ndarrs.append(uid[0])
                else:
                    ndarrs.append(None)
            self.run_inference.emit(ndarrs)
        else:
            self.run_drawer.emit(self.queue, self.window_w, self.window_h)

    @qtc.pyqtSlot(int, np.ndarray, qtc.QObject)
    def update_queue_from_cap_stream(self, uid, ndarr, props):
        self._update_queue((uid, ndarr, props, None))

    @qtc.pyqtSlot(list)
    def update_queue_from_inference(self, batch_detections):
        uid = 0
        for detections in batch_detections:
            self._update_queue(uid, self.queue[uid][1], self.queue[uid][2], detections)
            uid += 1
        self.run_drawer.emit(self.queue, self.window_w, self.window_h)

    def _update_queue(self, tpl):
        uid, ndarr, props, detections = tpl
        if ndarr is not None:
            t = (ndarr, props, detections)
            self.queue[uid] = t
        else:
            self.queue[uid] = None

    @qtc.pyqtSlot(int, int)
    def update_params(self, w, h):
        self.window_w = w
        self.window_h = h

