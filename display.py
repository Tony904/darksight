from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from conductor import CapState
from capture import CaptureProperties
import cv2
import numpy as np
import image_utils as imut


class DisplayDrawer(qtc.QObject):
    qimg_completed = qtc.pyqtSignal(qtg.QImage)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ndarray_dtype = np.uint8

    @qtc.pyqtSlot(list, int, int)
    def run(self, caps, w, h):
        print('display_drawer.run() executed.')
        caps = list(caps)
        canvas = np.zeros((h, w, 3), dtype=self.ndarray_dtype)
        uid = 0
        for state in caps:
            max_pw = w // 2
            max_ph = h // 2
            pimg = imut.scale_by_largest_dim(state.frame, max_pw, max_ph, zoom=state.props.zoom)
            # pimg = cv2.resize(ndarr, (0, 0), fx=state.props.zoom, fy=state.props.zoom, interpolation=cv2.INTER_LINEAR)
            ph, pw, _ = pimg.shape
            if state.detections is not None:
                print('state.detectios is not None')
                color = (0, 0, 255)
                for label, confidence, bbox in state.detections:
                    print(str(label) + ": " + str(confidence))
                    left, top, right, bottom = self._relative_to_abs_rect(bbox, pw, ph)
                    cv2.rectangle(pimg, (left, top), (right, bottom), color, 1)
                    cv2.putText(pimg, "{} [{:.0f}]".format(label, float(confidence)), (left, top - 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            else:
                print('state.detections = None')
            pimg = imut.crop_image_centered(pimg, pw, ph, x_offset=state.props.pan[0], y_offset=state.props.pan[1])
            ph, pw, _ = pimg.shape
            if uid == 0:  # top-left
                top, bottom, left, right = 0, ph, 0, pw
                canvas[top:bottom, left:right] = pimg
            elif uid == 1:  # top-right
                top, bottom, left, right = 0, ph, max_pw, max_pw + pw
                canvas[top:bottom, left:right] = pimg
            elif uid == 2:  # bottom-left
                top, bottom, left, right = max_ph, max_ph + ph, 0, pw
                canvas[top:bottom, left:right] = pimg
            elif uid == 3:  # bottom-right
                top, bottom, left, right = max_ph, max_ph + ph, max_pw, max_pw + pw
                canvas[top:bottom, left:right] = pimg
            uid += 1
        data = canvas.data
        cols = canvas.shape[1]
        rows = canvas.shape[0]
        stride = canvas.strides[0]
        display_qimg = qtg.QImage(data, cols, rows, stride, qtg.QImage.Format_RGB888)
        print('Emitting qimg_completed.')
        self.qimg_completed.emit(display_qimg.copy())

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
