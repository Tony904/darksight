from PyQt5 import QtCore as qtc
import numpy as np
from class_emitter import Emitter


class InferenceManager(qtc.QObject):
    run_inference = qtc.pyqtSignal()
    emit_inference_list = qtc.pyqtSignal(list)
    inference_initiation_requested = qtc.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inference_queue = []
        self.inference_active = False

    @qtc.pyqtSlot(int, np.ndarray, Emitter)
    def update_inference_queue(self, p, img_ndarr, emitter):
        new_entry = True
        for i in range(len(self.inference_queue)):
            if self.inference_queue[i][0] == p:
                print("Updating img queue in panel: " + str(p))
                new_entry = False
                tpl = (self.inference_queue[i][0], img_ndarr.copy(), self.inference_queue[i][2])
                self.inference_queue[i] = tpl
                break
        if new_entry:
            print("Adding new entry into inference_queue. p=" + str(p))
            self.inference_queue.append((p, img_ndarr.copy(), emitter))

    @qtc.pyqtSlot()
    def send_inference_list(self):
        if not self.inference_active:
            self.emit_inference_list.emit(self.inference_queue)
            print("Inference Manager emitted: emit_inference_list")
        else:
            print("Inference list request denied. self.inference_active=True")

    @qtc.pyqtSlot()
    def request_inference_start(self):
        self.inference_active = True
        self.run_inference.emit()
        print("Inference Manager emitted: run_inference")

    @qtc.pyqtSlot()
    def inference_completed(self):
        self.inference_active = False
        self.inference_initiation_requested.emit()
