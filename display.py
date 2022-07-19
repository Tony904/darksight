from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import cv2
import numpy as np
import image_utils as imut


class DisplayDrawer(qtc.QObject):
    qimg_completed = qtc.pyqtSignal(qtg.QImage)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ndarray_dtype = np.uint8

    @qtc.pyqtSlot(list, int, int)
    def run(self, queue, w, h):
        queue = list(queue)
        ndarr = np.zeros((h, w, 3), dtype=self.ndarray_dtype)
        uid = 0
        for cap in queue:
            if cap is not None:
                ndarr, props, detections = cap
                if detections is not None:
                    dst_h, dst_w, _ = ndarr.shape
                    color = (0, 0, 255)
                    for label, confidence, bbox in detections:
                        print(str(label) + ": " + str(confidence))
                        left, top, right, bottom = self._relative_to_abs_rect(bbox, dst_w, dst_h)
                        cv2.rectangle(ndarr, (left, top), (right, bottom), color, 1)
                        cv2.putText(ndarr, "{} [{:.0f}]".format(label, float(confidence)), (left, top - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                max_pw = w // 2
                max_ph = h // 2
                pimg = imut.scale_by_largest_dim(cap[1], max_pw, max_ph)
                pw = pimg.shape[1]
                ph = pimg.shape[0]
                pimg = cv2.resize(pimg, (0, 0), fx=props.zoom, fy=props.zoom, interpolation=cv2.INTER_LINEAR)
                pimg = imut.crop_image_centered(pimg, pw, ph, x_offset=props.pan[0], y_offset=props.pan[1])
                ph, pw, _ = pimg.shape
                if uid == 0:  # top-left
                    top, bottom, left, right = 0, ph, 0, pw
                    ndarr[top:bottom, left:right] = pimg
                elif uid == 1:  # top-right
                    top, bottom, left, right = 0, ph, max_pw, max_pw + pw
                    ndarr[top:bottom, left:right] = pimg
                elif uid == 2:  # bottom-left
                    top, bottom, left, right = max_ph, max_ph + ph, 0, pw
                    ndarr[top:bottom, left:right] = pimg
                elif uid == 3:  # bottom-right
                    top, bottom, left, right = max_ph, max_ph + ph, max_pw, max_pw + pw
                    ndarr[top:bottom, left:right] = pimg
            uid += 1
        data = ndarr.data
        cols = ndarr.shape[1]
        rows = ndarr.shape[0]
        stride = ndarr.strides[0]
        display_qimg = qtg.QImage(data, cols, rows, stride, qtg.QImage.Format_RGB888)
        self.qimg_completed.emit(display_qimg)

    @staticmethod
    def _relative_to_abs_rect(bbox, dst_w, dst_h):
        x, y, w, h = bbox
        abs_x = x * dst_w
        abs_y = y * dst_h
        abs_w = w * dst_w
        abs_h = h * dst_h
        left = int(abs_x - (abs_w / 2))
        top = int(abs_y - (abs_h / 2))
        right = int(abs_x + (abs_w / 2))
        bottom = int(abs_y + (abs_h / 2))
        return left, top, right, bottom
