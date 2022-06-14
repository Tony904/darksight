from PyQt5 import QtCore as qtc
import cv2
import numpy as np


class CaptureStream(qtc.QObject):
    frame_captured = qtc.pyqtSignal(np.ndarray, int, qtc.QObject)
    read_failed = qtc.pyqtSignal(int)
    deletion_requested = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.props = CaptureProperties()
        self.cap_active = False
        self.cap = None
        self.uid = None
        print("New CaptureStream instance created.")

    @qtc.pyqtSlot()
    def run(self):
        print("CaptureStream run() executed. uid=" + str(self.uid))
        self.cap = cv2.VideoCapture(self.props.c, cv2.CAP_DSHOW)
        self.cap_active = True
        while self.cap.isOpened() and self.cap_active:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_captured.emit(frame_rgb, self.uid, self.props)
            else:
                print("Error: Camera read fail. uid=" + str(self.uid) + ", cam index=" + str(self.props.c))
                self.read_failed.emit(self.uid)
                self.cap_active = False
                break
        self.cap.release()
        if not self.cap_active:
            self.deletion_requested.emit(self.uid)

    @qtc.pyqtSlot()
    def update_prop(self, prop, x):
        print("Updating prop: " + prop + " x=" + str(x))
        if prop == 'autofocus':
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, x)
            self.props.autofocus = self.cap.get(cv2.CAP_PROP_AUTOFOCUS)
        elif prop == 'autoexposure':
            self.cap.set(cv2.CAP_PROP_AUTOFOCUS, x)
            self.props.autoexposure = self.cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
        elif prop == 'autowhite':
            self.cap.set(cv2.CAP_PROP_AUTO_WB, x)
            self.props.autowhite = self.cap.get(cv2.CAP_PROP_AUTO_WB)
        elif prop == 'focus':
            self.cap.set(cv2.CAP_PROP_FOCUS, x)
            self.props.focus = self.cap.get(cv2.CAP_PROP_FOCUS)
        elif prop == 'exposure':
            if not self.props.autoexposure:
                self.cap.set(cv2.CAP_PROP_EXPOSURE, x)
                self.props.exposure = self.cap.get(cv2.CAP_PROP_EXPOSURE)
        elif prop == 'backlight':
            self.cap.set(cv2.CAP_PROP_BACKLIGHT, x)
            self.props.backlight = self.cap.get(cv2.CAP_PROP_BACKLIGHT)
        elif prop == 'sharpness':
            self.cap.set(cv2.CAP_PROP_SHARPNESS, x)
            self.props.sharpness = self.cap.get(cv2.CAP_PROP_SHARPNESS)
        elif prop == 'brightness':
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, x)
            self.props.brightness = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
        elif prop == 'contrast':
            self.cap.set(cv2.CAP_PROP_CONTRAST, x)
            self.props.contrast = self.cap.get(cv2.CAP_PROP_CONTRAST)
        elif prop == 'gain':
            self.cap.set(cv2.CAP_PROP_GAIN, x)
            self.props.gain = self.cap.get(cv2.CAP_PROP_GAIN)
        elif prop == 'gamma':
            self.cap.set(cv2.CAP_PROP_GAMMA, x)
            self.props.gamma = self.cap.get(cv2.CAP_PROP_GAMMA)
        elif prop == 'hue':
            self.cap.set(cv2.CAP_PROP_HUE, x)
            self.props.hue = self.cap.get(cv2.CAP_PROP_HUE)
        elif prop == 'saturation':
            self.cap.set(cv2.CAP_PROP_SATURATION, x)
            self.props.saturation = self.cap.get(cv2.CAP_PROP_SATURATION)
        elif prop == 'white':
            if not self.props.autowhite:
                self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, x)
                self.cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, x)
                self.props.white = self.cap.get(cv2.CAP_PROP_WHITE_BALANCE_RED_V)
        elif prop == 'zoom':
            self.props.zoom = x
        elif prop == 'rotate':
            self.props.rotate = x
        elif prop == 'crop':
            self.props.crop = x
        elif prop == 'pan':
            pan_x = x[0] + self.props.pan[0]
            pan_y = x[1] + self.props.pan[1]
            self.props.pan = (pan_x, pan_y)

    def stop(self):
        print("Stopped CaptureStream: " + str(self.uid))
        self.cap_active = False


class CaptureProperties(qtc.QObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.c = -1
        self.width = 5000
        self.height = 4000
        self.focus = 300.
        self.autofocus = 1  # 2 = disabled, 1 = enabled
        self.brightness = 50
        self.contrast = 32
        self.hue = 0
        self.saturation = 64
        self.sharpness = 3
        self.gamma = 100
        self.white = 4600
        self.autowhite = 1
        self.backlight = 1
        self.gain = 0
        self.exposure = -6
        self.autoexposure = 1  # if disabled, must be re-enabled in AMcap software

        self.zoom = 1.
        self.rotate = 0
        self.pan = (0, 0)  # (x, y) offset from center of output view
