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

    @qtc.pyqtSlot()
    def run(self, ndarrs, thresh):
        outputs = []  # element = tuple(uid, detections)
        for ndarr in ndarrs:
            detections = None
            if ndarr is not None:
                scaled = imut.scale_by_largest_dim(ndarr, gbs.darknet_w, gbs.darknet_h)
                padded, pad_bottom, pad_right = imut.pad_image_to_square(scaled)
                img = darknet.make_image(gbs.darknet_w, gbs.darknet_h, 3)
                darknet.copy_image_from_bytes(img, padded.tobytes())
                detections = darknet.detect_image(gbs.network, gbs.class_names, img, thresh)
                detections = self._get_relative_unpadded_detections(detections, pad_bottom, pad_right)
                darknet.free_image(img)
            outputs.append(detections)
        self.completed.emit(outputs)

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


class InferenceDrawer(qtc.QObject):
    completed = qtc.pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @qtc.pyqtSlot(tuple)
    def run(self, inference_output):
        inference_output = list(inference_output)
        outputs = []
        for element in inference_output:
            uid, ndarr, detections = element
            dst_h, dst_w, _ = ndarr.shape
            color = (0, 0, 255)
            for label, confidence, bbox in detections:
                print(str(label) + ": " + str(confidence))
                left, top, right, bottom = self._relative_to_abs_rect(bbox, dst_w, dst_h)
                cv2.rectangle(ndarr, (left, top), (right, bottom), color, 1)
                cv2.putText(ndarr, "{} [{:.0f}]".format(label, float(confidence)), (left, top - 5),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            outputs.append((uid, ndarr, detections))
        self.completed.emit(outputs)

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
