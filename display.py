from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import cv2
import numpy as np
import image_utils as imut


class DisplayManager(qtc.QObject):
    display_params_update_requested = qtc.pyqtSignal()
    run_drawer = qtc.pyqtSignal(list, int, int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = [None, None, None, None]  # element = (ndarray, uid, CaptureProperties)
        self.window_w = None
        self.window_h = None

    @qtc.pyqtSlot(np.ndarray, int, qtc.QObject)
    def update_queue(self, uid, ndarr, props):
        if ndarr is not None:
            tpl = (uid, ndarr, props)
            self.queue[uid] = tpl
        else:
            self.queue[uid] = None
            print("DisplayerManager queue index cleared: uid=" + str(uid))

    @qtc.pyqtSlot(int, int, list)
    def update_params(self, w, h):
        self.window_w = w
        self.window_h = h

    @qtc.pyqtSlot()
    def request_display_params(self):
        self.display_params_update_requested.emit()


class DisplayDrawer(qtc.QObject):
    qimg_completed = qtc.pyqtSignal(qtg.QImage)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.caps = []  # element = (ndarray, uid, CaptureProperties)
        self.ndarray_dtype = np.uint8

    @qtc.pyqtSlot(list, int, int)
    def run(self, queue, w, h):
        queue = list(queue)
        ndarr = np.zeros((h, w, 3), dtype=self.ndarray_dtype)
        for cap in queue:
            if cap is not None:
                uid = cap[0]
                max_pw = w // 2
                max_ph = h // 2
                pimg = imut.scale_by_largest_dim(cap[1], max_pw, max_ph)
                pw = pimg.shape[1]
                ph = pimg.shape[0]
                pimg = cv2.resize(pimg, (0, 0), fx=cap[2].zoom, fy=cap[2].zoom, interpolation=cv2.INTER_LINEAR)
                pimg = imut.crop_image_centered(pimg, pw, ph, x_offset=cap[2].pan[0], y_offset=cap[2].pan[1])
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
        data = ndarr.data
        cols = ndarr.shape[1]
        rows = ndarr.shape[0]
        stride = ndarr.strides[0]
        display_qimg = qtg.QImage(data, cols, rows, stride, qtg.QImage.Format_RGB888)
        self.qimg_completed.emit(display_qimg)
