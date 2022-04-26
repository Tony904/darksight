from PyQt5 import QtCore as qtc
import cv2
import numpy as np


class DetectionsDrawer(qtc.QObject):
    detections_drawn = qtc.pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dst_h = None
        self.dst_w = None

    @qtc.pyqtSlot(tuple)
    def run(self, inference_output):
        uid, ndarr, detections = inference_output
        self.dst_h, self.dst_w, _ = ndarr.shape
        color = (0, 0, 255)
        for label, confidence, bbox in detections:
            print(str(label) + ": " + str(confidence))
            left, top, right, bottom = self._relative_to_abs_rect(bbox)
            cv2.rectangle(ndarr, (left, top), (right, bottom), color, 1)
            cv2.putText(ndarr, "{} [{:.0f}]".format(label, float(confidence)), (left, top - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        self.detections_drawn.emit(ndarr)

    def _relative_to_abs_rect(self, bbox):
        x, y, w, h = bbox
        abs_x = x * self.dst_w
        abs_y = y * self.dst_h
        abs_w = w * self.dst_w
        abs_h = h * self.dst_h
        left = int(abs_x - (abs_w / 2))
        top = int(abs_y - (abs_h / 2))
        right = int(abs_x + (abs_w / 2))
        bottom = int(abs_y + (abs_h / 2))
        return left, top, right, bottom
