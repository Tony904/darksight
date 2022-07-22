from PyQt5 import QtCore as qtc
import numpy as np
import darknet
import image_utils as imut
import globals as gbs
import cv2


class Inference(qtc.QObject):
    completed = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @qtc.pyqtSlot(list, float)
    def run(self, caps, thresh):
        print('Running inference. Tresh = ' + str(thresh))
        print('length of caps[] = ' + str(len(caps)))
        for state in caps:
            detections = None
            frame = state.frame.copy()
            if frame is not None:
                scaled = imut.scale_by_largest_dim(frame, gbs.darknet_w, gbs.darknet_h)
                padded, pad_bottom, pad_right = imut.pad_image_to_square(scaled)
                img = darknet.make_image(gbs.darknet_w, gbs.darknet_h, 3)
                darknet.copy_image_from_bytes(img, padded.tobytes())
                detections = darknet.detect_image(gbs.network, gbs.class_names, img, thresh=thresh)
                detections = self._get_relative_unpadded_detections(detections, pad_bottom, pad_right)
                darknet.free_image(img)
            state.detections = detections
            print('length of detections[] = ' + str(len(detections)))
        # self.completed.emit(caps)
        self.completed.emit()
        print('Inference complete.')

    @staticmethod
    def _get_relative_unpadded_detections(detections, pad_bottom, pad_right):
        adjusted_detections = []
        unpadded_w = gbs.darknet_w - pad_right
        unpadded_h = gbs.darknet_h - pad_bottom
        for label, confidence, bbox in detections:
            x, y, w, h = bbox  # note: bbox coordinates are absolute coordinates, not relative
            rel_x = float(x / unpadded_w)
            rel_y = float(y / unpadded_h)
            rel_w = float(w / unpadded_w)
            rel_h = float(h / unpadded_h)
            adjusted_bbox = (rel_x, rel_y, rel_w, rel_h)
            adjusted_detection = (label, confidence, adjusted_bbox)
            adjusted_detections.append(adjusted_detection)
        return adjusted_detections
