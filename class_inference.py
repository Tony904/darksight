from PyQt5 import QtCore as qtc
import darknet
import image_utils as imut
import globals as gbs


class Inference(qtc.QObject):
    inference_complete = qtc.pyqtSignal()
    inference_packages_updated = qtc.pyqtSignal()
    inference_packages_update_requested = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.packages = []  # package = tuple(uid, ndarr, emitter)
        self.thresh = 0.5

    @qtc.pyqtSlot()
    def run(self):
        for uid, ndarr, emitter in self.packages:
            scaled = imut.scale_by_largest_dim(ndarr, gbs.darknet_w, gbs.darknet_h)
            padded, pad_bottom, pad_right = imut.pad_image_to_square(scaled)
            img = darknet.make_image(gbs.darknet_w, gbs.darknet_h, 3)
            darknet.copy_image_from_bytes(img, padded.tobytes())
            detections = darknet.detect_image(gbs.network, gbs.class_names, img, self.thresh)
            detections = self._get_relative_unpadded_detections(detections, pad_bottom, pad_right)
            emitter.emitter_signal.emit((uid, ndarr, detections))
            darknet.free_image(img)
        self.inference_complete.emit()

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

    @qtc.pyqtSlot()
    def initiate(self):
        self.inference_packages_update_requested.emit()

    @qtc.pyqtSlot(list)
    def update_packages(self, lst):
        self.packages = list(lst)
        self.inference_packages_updated.emit()

    def update_thresh(self, x):
        self.thresh = x
