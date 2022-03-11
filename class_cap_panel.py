import sys
import argparse
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from PyQt5 import QtWidgets as qtw
import cv2
import numpy as np
import functools
import my_utils as mut


class CapturePanel(qtw.QFrame):
    camera_capture_requested = qtc.pyqtSignal(int)

    def _if_cap_active(func):
        @functools.wraps(func)
        def wrapper(*args):
            if args[0].capture_active:
                return func(*args)
        return wrapper

    def _if_cap_not_active(func):
        @functools.wraps(func)
        def wrapper(*args):
            if not args[0].capture_active:
                return func(*args)
        return wrapper

    def setupUi(self, qframe):
        row, col, space_available = self._get_row_col(qframe)
        suffix = "_" + str(2 * col + row)

        self.frme_cap_panel_0 = qtw.QFrame(qframe)
        self.frme_cap_panel_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_panel_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_panel_0.setLineWidth(1)
        self.frme_cap_panel_0.setObjectName("frme_cap_panel" + suffix)
        self.layout_hrz_frme_cap_panel_0 = qtw.QHBoxLayout(self.frme_cap_panel_0)
        self.layout_hrz_frme_cap_panel_0.setContentsMargins(0, 0, 0, 0)
        self.layout_hrz_frme_cap_panel_0.setSpacing(0)
        self.layout_hrz_frme_cap_panel_0.setObjectName("layout_hrz_frme_cap_panel" + suffix)
        self.frme_cap_controls_0 = qtw.QFrame(self.frme_cap_panel_0)
        self.frme_cap_controls_0.setMaximumSize(qtc.QSize(80, 16777215))
        self.frme_cap_controls_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_controls_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_controls_0.setObjectName("frme_cap_controls" + suffix)
        self.layout_vrt_frme_cap_controls_0 = qtw.QVBoxLayout(self.frme_cap_controls_0)
        self.layout_vrt_frme_cap_controls_0.setContentsMargins(0, 0, 0, 0)
        self.layout_vrt_frme_cap_controls_0.setSpacing(0)
        self.layout_vrt_frme_cap_controls_0.setObjectName("layout_vrt_frme_cap_controls" + suffix)
        self.frme_zoom_0 = qtw.QFrame(self.frme_cap_controls_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_zoom_0.sizePolicy().hasHeightForWidth())
        self.frme_zoom_0.setSizePolicy(sizePolicy)
        self.frme_zoom_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_zoom_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_zoom_0.setObjectName("frme_zoom" + suffix)
        self.layout_hrz_frme_zoom_0 = qtw.QHBoxLayout(self.frme_zoom_0)
        self.layout_hrz_frme_zoom_0.setContentsMargins(3, 3, 0, 3)
        self.layout_hrz_frme_zoom_0.setSpacing(3)
        self.layout_hrz_frme_zoom_0.setObjectName("layout_hrz_frme_zoom" + suffix)
        self.lbl_static_zoom_0 = qtw.QLabel(self.frme_zoom_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_zoom_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_zoom_0.setSizePolicy(sizePolicy)
        self.lbl_static_zoom_0.setMaximumSize(qtc.QSize(16777215, 20))
        self.lbl_static_zoom_0.setAlignment(qtc.Qt.AlignLeading | qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        self.lbl_static_zoom_0.setObjectName("lbl_static_zoom" + suffix)
        self.layout_hrz_frme_zoom_0.addWidget(self.lbl_static_zoom_0)
        self.spbx_dbl_zoom_0 = qtw.QDoubleSpinBox(self.frme_zoom_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_dbl_zoom_0.sizePolicy().hasHeightForWidth())
        self.spbx_dbl_zoom_0.setSizePolicy(sizePolicy)
        self.spbx_dbl_zoom_0.setMaximumSize(qtc.QSize(1000, 20))
        self.spbx_dbl_zoom_0.setDecimals(2)
        self.spbx_dbl_zoom_0.setMinimum(0.01)
        self.spbx_dbl_zoom_0.setMaximum(3.0)
        self.spbx_dbl_zoom_0.setSingleStep(0.1)
        self.spbx_dbl_zoom_0.setProperty("value", 1.0)
        self.spbx_dbl_zoom_0.setObjectName("spbx_dbl_zoom" + suffix)
        self.layout_hrz_frme_zoom_0.addWidget(self.spbx_dbl_zoom_0)
        self.layout_vrt_frme_cap_controls_0.addWidget(self.frme_zoom_0)
        self.frme_pause_0 = qtw.QFrame(self.frme_cap_controls_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_pause_0.sizePolicy().hasHeightForWidth())
        self.frme_pause_0.setSizePolicy(sizePolicy)
        self.frme_pause_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_pause_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_pause_0.setObjectName("frme_pause" + suffix)
        self.layout_hrz_frme_pause_0 = qtw.QHBoxLayout(self.frme_pause_0)
        self.layout_hrz_frme_pause_0.setContentsMargins(0, 3, 0, 3)
        self.layout_hrz_frme_pause_0.setSpacing(0)
        self.layout_hrz_frme_pause_0.setObjectName("layout_hrz_frme_pause" + suffix)
        spacerItem = qtw.QSpacerItem(40, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.layout_hrz_frme_pause_0.addItem(spacerItem)
        self.chbx_pause_0 = qtw.QCheckBox(self.frme_pause_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chbx_pause_0.sizePolicy().hasHeightForWidth())
        self.chbx_pause_0.setSizePolicy(sizePolicy)
        self.chbx_pause_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.chbx_pause_0.setTristate(False)
        self.chbx_pause_0.setObjectName("chbx_pause" + suffix)
        self.layout_hrz_frme_pause_0.addWidget(self.chbx_pause_0)
        spacerItem1 = qtw.QSpacerItem(38, 20, qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.layout_hrz_frme_pause_0.addItem(spacerItem1)
        self.layout_vrt_frme_cap_controls_0.addWidget(self.frme_pause_0)
        self.frme_rotate_image_0 = qtw.QFrame(self.frme_cap_controls_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_rotate_image_0.sizePolicy().hasHeightForWidth())
        self.frme_rotate_image_0.setSizePolicy(sizePolicy)
        self.frme_rotate_image_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_rotate_image_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_rotate_image_0.setObjectName("frme_rotate_image" + suffix)
        self.layout_vrt_frme_rotate_image_0 = qtw.QVBoxLayout(self.frme_rotate_image_0)
        self.layout_vrt_frme_rotate_image_0.setContentsMargins(0, 3, 0, 3)
        self.layout_vrt_frme_rotate_image_0.setSpacing(0)
        self.layout_vrt_frme_rotate_image_0.setObjectName("layout_vrt_frme_rotate_image" + suffix)
        self.lbl_static_rotate_0 = qtw.QLabel(self.frme_rotate_image_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_rotate_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_rotate_0.setSizePolicy(sizePolicy)
        self.lbl_static_rotate_0.setAlignment(qtc.Qt.AlignCenter)
        self.lbl_static_rotate_0.setObjectName("lbl_static_rotate" + suffix)
        self.layout_vrt_frme_rotate_image_0.addWidget(self.lbl_static_rotate_0)
        self.spbx_rotate_image_0 = qtw.QSpinBox(self.frme_rotate_image_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_rotate_image_0.sizePolicy().hasHeightForWidth())
        self.spbx_rotate_image_0.setSizePolicy(sizePolicy)
        self.spbx_rotate_image_0.setMaximum(270)
        self.spbx_rotate_image_0.setSingleStep(90)
        self.spbx_rotate_image_0.setProperty("value", 0)
        self.spbx_rotate_image_0.setObjectName("spbx_rotate_image" + suffix)
        self.layout_vrt_frme_rotate_image_0.addWidget(self.spbx_rotate_image_0)
        self.layout_vrt_frme_cap_controls_0.addWidget(self.frme_rotate_image_0)
        self.scar_cap_props_0 = qtw.QScrollArea(self.frme_cap_controls_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scar_cap_props_0.sizePolicy().hasHeightForWidth())
        self.scar_cap_props_0.setSizePolicy(sizePolicy)
        self.scar_cap_props_0.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.scar_cap_props_0.setSizeAdjustPolicy(qtw.QAbstractScrollArea.AdjustIgnored)
        self.scar_cap_props_0.setWidgetResizable(True)
        self.scar_cap_props_0.setObjectName("scar_cap_props" + suffix)
        self.scar_con_cap_props_0 = qtw.QWidget()
        self.scar_con_cap_props_0.setGeometry(qtc.QRect(0, 0, 59, 425))
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scar_con_cap_props_0.sizePolicy().hasHeightForWidth())
        self.scar_con_cap_props_0.setSizePolicy(sizePolicy)
        self.scar_con_cap_props_0.setObjectName("scar_con_cap_props" + suffix)
        self.layout_vrt_scar_con_cap_props_0 = qtw.QVBoxLayout(self.scar_con_cap_props_0)
        self.layout_vrt_scar_con_cap_props_0.setContentsMargins(0, 0, 0, 0)
        self.layout_vrt_scar_con_cap_props_0.setSpacing(0)
        self.layout_vrt_scar_con_cap_props_0.setObjectName("layout_vrt_scar_con_cap_props" + suffix)
        self.frme_cap_focus_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_focus_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_focus_0.setSizePolicy(sizePolicy)
        self.frme_cap_focus_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_focus_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_focus_0.setObjectName("frme_cap_focus" + suffix)
        self.layout_vrt_frme_cap_brightness_1 = qtw.QVBoxLayout(self.frme_cap_focus_0)
        self.layout_vrt_frme_cap_brightness_1.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_brightness_1.setSpacing(0)
        self.layout_vrt_frme_cap_brightness_1.setObjectName("layout_vrt_frme_cap_brightness_1")
        self.lbl_static_focus_0 = qtw.QLabel(self.frme_cap_focus_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_focus_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_focus_0.setSizePolicy(sizePolicy)
        self.lbl_static_focus_0.setObjectName("lbl_static_focus" + suffix)
        self.layout_vrt_frme_cap_brightness_1.addWidget(self.lbl_static_focus_0)
        self.spbx_cap_focus_0 = qtw.QSpinBox(self.frme_cap_focus_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_focus_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_focus_0.setSizePolicy(sizePolicy)
        self.spbx_cap_focus_0.setAlignment(qtc.Qt.AlignLeading | qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        self.spbx_cap_focus_0.setMinimum(0)
        self.spbx_cap_focus_0.setMaximum(1100)
        self.spbx_cap_focus_0.setProperty("value", 550)
        self.spbx_cap_focus_0.setObjectName("spbx_cap_focus" + suffix)
        self.layout_vrt_frme_cap_brightness_1.addWidget(self.spbx_cap_focus_0)
        self.chbx_cap_autofocus_0 = qtw.QCheckBox(self.frme_cap_focus_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chbx_cap_autofocus_0.sizePolicy().hasHeightForWidth())
        self.chbx_cap_autofocus_0.setSizePolicy(sizePolicy)
        self.chbx_cap_autofocus_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.chbx_cap_autofocus_0.setObjectName("chbx_cap_autofocus" + suffix)
        self.layout_vrt_frme_cap_brightness_1.addWidget(self.chbx_cap_autofocus_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_focus_0)
        self.frme_cap_exposure_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_exposure_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_exposure_0.setSizePolicy(sizePolicy)
        self.frme_cap_exposure_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_exposure_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_exposure_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_exposure_0.setObjectName("frme_cap_exposure" + suffix)
        self.layout_vrt_frme_cap_exposure_0 = qtw.QVBoxLayout(self.frme_cap_exposure_0)
        self.layout_vrt_frme_cap_exposure_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_exposure_0.setSpacing(0)
        self.layout_vrt_frme_cap_exposure_0.setObjectName("layout_vrt_frme_cap_exposure" + suffix)
        self.lbl_static_exposure_0 = qtw.QLabel(self.frme_cap_exposure_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_exposure_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_exposure_0.setSizePolicy(sizePolicy)
        self.lbl_static_exposure_0.setObjectName("lbl_static_exposure" + suffix)
        self.layout_vrt_frme_cap_exposure_0.addWidget(self.lbl_static_exposure_0)
        self.spbx_cap_exposure_0 = qtw.QSpinBox(self.frme_cap_exposure_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_exposure_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_exposure_0.setSizePolicy(sizePolicy)
        self.spbx_cap_exposure_0.setMinimum(-20)
        self.spbx_cap_exposure_0.setMaximum(20)
        self.spbx_cap_exposure_0.setProperty("value", -6)
        self.spbx_cap_exposure_0.setObjectName("spbx_cap_exposure" + suffix)
        self.layout_vrt_frme_cap_exposure_0.addWidget(self.spbx_cap_exposure_0)
        self.chbx_cap_autoexposure_0 = qtw.QCheckBox(self.frme_cap_exposure_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chbx_cap_autoexposure_0.sizePolicy().hasHeightForWidth())
        self.chbx_cap_autoexposure_0.setSizePolicy(sizePolicy)
        self.chbx_cap_autoexposure_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.chbx_cap_autoexposure_0.setChecked(True)
        self.chbx_cap_autoexposure_0.setObjectName("chbx_cap_autoexposure" + suffix)
        self.layout_vrt_frme_cap_exposure_0.addWidget(self.chbx_cap_autoexposure_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_exposure_0)
        self.frme_cap_backlight_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_backlight_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_backlight_0.setSizePolicy(sizePolicy)
        self.frme_cap_backlight_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_backlight_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_backlight_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_backlight_0.setObjectName("frme_cap_backlight" + suffix)
        self.layout_vrt_frme_cap_backlight_0 = qtw.QVBoxLayout(self.frme_cap_backlight_0)
        self.layout_vrt_frme_cap_backlight_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_backlight_0.setSpacing(0)
        self.layout_vrt_frme_cap_backlight_0.setObjectName("layout_vrt_frme_cap_backlight" + suffix)
        self.lbl_static_backlight_0 = qtw.QLabel(self.frme_cap_backlight_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_backlight_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_backlight_0.setSizePolicy(sizePolicy)
        self.lbl_static_backlight_0.setObjectName("lbl_static_backlight" + suffix)
        self.layout_vrt_frme_cap_backlight_0.addWidget(self.lbl_static_backlight_0)
        self.spbx_cap_backlight_0 = qtw.QSpinBox(self.frme_cap_backlight_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_backlight_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_backlight_0.setSizePolicy(sizePolicy)
        self.spbx_cap_backlight_0.setMinimum(-10)
        self.spbx_cap_backlight_0.setMaximum(10)
        self.spbx_cap_backlight_0.setProperty("value", 1)
        self.spbx_cap_backlight_0.setObjectName("spbx_cap_backlight" + suffix)
        self.layout_vrt_frme_cap_backlight_0.addWidget(self.spbx_cap_backlight_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_backlight_0)
        self.frme_cap_sharpness_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_sharpness_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_sharpness_0.setSizePolicy(sizePolicy)
        self.frme_cap_sharpness_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_sharpness_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_sharpness_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_sharpness_0.setObjectName("frme_cap_sharpness" + suffix)
        self.layout_vrt_frme_cap_sharpness_0 = qtw.QVBoxLayout(self.frme_cap_sharpness_0)
        self.layout_vrt_frme_cap_sharpness_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_sharpness_0.setSpacing(0)
        self.layout_vrt_frme_cap_sharpness_0.setObjectName("layout_vrt_frme_cap_sharpness" + suffix)
        self.lbl_static_sharpness_0 = qtw.QLabel(self.frme_cap_sharpness_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_sharpness_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_sharpness_0.setSizePolicy(sizePolicy)
        self.lbl_static_sharpness_0.setObjectName("lbl_static_sharpness" + suffix)
        self.layout_vrt_frme_cap_sharpness_0.addWidget(self.lbl_static_sharpness_0)
        self.spbx_cap_sharpness_0 = qtw.QSpinBox(self.frme_cap_sharpness_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_sharpness_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_sharpness_0.setSizePolicy(sizePolicy)
        self.spbx_cap_sharpness_0.setMinimum(-100)
        self.spbx_cap_sharpness_0.setMaximum(100)
        self.spbx_cap_sharpness_0.setProperty("value", 3)
        self.spbx_cap_sharpness_0.setObjectName("spbx_cap_sharpness" + suffix)
        self.layout_vrt_frme_cap_sharpness_0.addWidget(self.spbx_cap_sharpness_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_sharpness_0)
        self.frme_cap_gamma_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_gamma_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_gamma_0.setSizePolicy(sizePolicy)
        self.frme_cap_gamma_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_gamma_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_gamma_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_gamma_0.setObjectName("frme_cap_gamma" + suffix)
        self.layout_vrt_frme_cap_gamma_0 = qtw.QVBoxLayout(self.frme_cap_gamma_0)
        self.layout_vrt_frme_cap_gamma_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_gamma_0.setSpacing(0)
        self.layout_vrt_frme_cap_gamma_0.setObjectName("layout_vrt_frme_cap_gamma" + suffix)
        self.lbl_static_gamma_0 = qtw.QLabel(self.frme_cap_gamma_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_gamma_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_gamma_0.setSizePolicy(sizePolicy)
        self.lbl_static_gamma_0.setObjectName("lbl_static_gamma" + suffix)
        self.layout_vrt_frme_cap_gamma_0.addWidget(self.lbl_static_gamma_0)
        self.spbx_cap_gamma_0 = qtw.QSpinBox(self.frme_cap_gamma_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_gamma_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_gamma_0.setSizePolicy(sizePolicy)
        self.spbx_cap_gamma_0.setMaximum(1000)
        self.spbx_cap_gamma_0.setProperty("value", 100)
        self.spbx_cap_gamma_0.setObjectName("spbx_cap_gamma" + suffix)
        self.layout_vrt_frme_cap_gamma_0.addWidget(self.spbx_cap_gamma_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_gamma_0)
        self.frme_cap_gain_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_gain_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_gain_0.setSizePolicy(sizePolicy)
        self.frme_cap_gain_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_gain_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_gain_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_gain_0.setObjectName("frme_cap_gain" + suffix)
        self.layout_vrt_frme_cap_gain_0 = qtw.QVBoxLayout(self.frme_cap_gain_0)
        self.layout_vrt_frme_cap_gain_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_gain_0.setSpacing(0)
        self.layout_vrt_frme_cap_gain_0.setObjectName("layout_vrt_frme_cap_gain" + suffix)
        self.lbl_static_gain_0 = qtw.QLabel(self.frme_cap_gain_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_gain_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_gain_0.setSizePolicy(sizePolicy)
        self.lbl_static_gain_0.setObjectName("lbl_static_gain" + suffix)
        self.layout_vrt_frme_cap_gain_0.addWidget(self.lbl_static_gain_0)
        self.spbx_cap_gain_0 = qtw.QSpinBox(self.frme_cap_gain_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_gain_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_gain_0.setSizePolicy(sizePolicy)
        self.spbx_cap_gain_0.setMaximum(1000)
        self.spbx_cap_gain_0.setProperty("value", 0)
        self.spbx_cap_gain_0.setObjectName("spbx_cap_gain" + suffix)
        self.layout_vrt_frme_cap_gain_0.addWidget(self.spbx_cap_gain_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_gain_0)
        self.frme_cap_contrast_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_contrast_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_contrast_0.setSizePolicy(sizePolicy)
        self.frme_cap_contrast_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_contrast_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_contrast_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_contrast_0.setObjectName("frme_cap_contrast" + suffix)
        self.layout_vrt_frme_cap_contrast_0 = qtw.QVBoxLayout(self.frme_cap_contrast_0)
        self.layout_vrt_frme_cap_contrast_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_contrast_0.setSpacing(0)
        self.layout_vrt_frme_cap_contrast_0.setObjectName("layout_vrt_frme_cap_contrast" + suffix)
        self.lbl_static_contrast_0 = qtw.QLabel(self.frme_cap_contrast_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_contrast_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_contrast_0.setSizePolicy(sizePolicy)
        self.lbl_static_contrast_0.setObjectName("lbl_static_contrast" + suffix)
        self.layout_vrt_frme_cap_contrast_0.addWidget(self.lbl_static_contrast_0)
        self.spbx_cap_contrast_0 = qtw.QSpinBox(self.frme_cap_contrast_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_contrast_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_contrast_0.setSizePolicy(sizePolicy)
        self.spbx_cap_contrast_0.setMinimum(-100)
        self.spbx_cap_contrast_0.setMaximum(100)
        self.spbx_cap_contrast_0.setProperty("value", 32)
        self.spbx_cap_contrast_0.setObjectName("spbx_cap_contrast" + suffix)
        self.layout_vrt_frme_cap_contrast_0.addWidget(self.spbx_cap_contrast_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_contrast_0)
        self.frme_cap_saturation_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_saturation_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_saturation_0.setSizePolicy(sizePolicy)
        self.frme_cap_saturation_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_saturation_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_saturation_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_saturation_0.setObjectName("frme_cap_saturation" + suffix)
        self.layout_vrt_frme_cap_saturation_0 = qtw.QVBoxLayout(self.frme_cap_saturation_0)
        self.layout_vrt_frme_cap_saturation_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_saturation_0.setSpacing(0)
        self.layout_vrt_frme_cap_saturation_0.setObjectName("layout_vrt_frme_cap_saturation" + suffix)
        self.lbl_static_saturation_0 = qtw.QLabel(self.frme_cap_saturation_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_saturation_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_saturation_0.setSizePolicy(sizePolicy)
        self.lbl_static_saturation_0.setObjectName("lbl_static_saturation" + suffix)
        self.layout_vrt_frme_cap_saturation_0.addWidget(self.lbl_static_saturation_0)
        self.spbx_cap_saturation_0 = qtw.QSpinBox(self.frme_cap_saturation_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_saturation_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_saturation_0.setSizePolicy(sizePolicy)
        self.spbx_cap_saturation_0.setMinimum(-200)
        self.spbx_cap_saturation_0.setMaximum(200)
        self.spbx_cap_saturation_0.setProperty("value", 64)
        self.spbx_cap_saturation_0.setObjectName("spbx_cap_saturation" + suffix)
        self.layout_vrt_frme_cap_saturation_0.addWidget(self.spbx_cap_saturation_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_saturation_0)
        self.frme_cap_brightness_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_brightness_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_brightness_0.setSizePolicy(sizePolicy)
        self.frme_cap_brightness_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_brightness_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_brightness_0.setObjectName("frme_cap_brightness" + suffix)
        self.layout_vrt_frme_cap_brightness_0 = qtw.QVBoxLayout(self.frme_cap_brightness_0)
        self.layout_vrt_frme_cap_brightness_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_brightness_0.setSpacing(0)
        self.layout_vrt_frme_cap_brightness_0.setObjectName("layout_vrt_frme_cap_brightness" + suffix)
        self.lbl_static_brightness_0 = qtw.QLabel(self.frme_cap_brightness_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_brightness_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_brightness_0.setSizePolicy(sizePolicy)
        self.lbl_static_brightness_0.setObjectName("lbl_static_brightness" + suffix)
        self.layout_vrt_frme_cap_brightness_0.addWidget(self.lbl_static_brightness_0)
        self.spbx_cap_brightness_0 = qtw.QSpinBox(self.frme_cap_brightness_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_brightness_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_brightness_0.setSizePolicy(sizePolicy)
        self.spbx_cap_brightness_0.setAlignment(qtc.Qt.AlignLeading | qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        self.spbx_cap_brightness_0.setMinimum(-100)
        self.spbx_cap_brightness_0.setMaximum(100)
        self.spbx_cap_brightness_0.setProperty("value", 0)
        self.spbx_cap_brightness_0.setObjectName("spbx_cap_brightness" + suffix)
        self.layout_vrt_frme_cap_brightness_0.addWidget(self.spbx_cap_brightness_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_brightness_0)
        self.frme_cap_hue_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_hue_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_hue_0.setSizePolicy(sizePolicy)
        self.frme_cap_hue_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_hue_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_hue_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_hue_0.setObjectName("frme_cap_hue" + suffix)
        self.layout_vrt_frme_cap_hue_0 = qtw.QVBoxLayout(self.frme_cap_hue_0)
        self.layout_vrt_frme_cap_hue_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_hue_0.setSpacing(0)
        self.layout_vrt_frme_cap_hue_0.setObjectName("layout_vrt_frme_cap_hue" + suffix)
        self.lbl_static_hue_0 = qtw.QLabel(self.frme_cap_hue_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_hue_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_hue_0.setSizePolicy(sizePolicy)
        self.lbl_static_hue_0.setObjectName("lbl_static_hue" + suffix)
        self.layout_vrt_frme_cap_hue_0.addWidget(self.lbl_static_hue_0)
        self.spbx_cap_hue_0 = qtw.QSpinBox(self.frme_cap_hue_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_hue_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_hue_0.setSizePolicy(sizePolicy)
        self.spbx_cap_hue_0.setMinimum(-100)
        self.spbx_cap_hue_0.setMaximum(100)
        self.spbx_cap_hue_0.setProperty("value", 0)
        self.spbx_cap_hue_0.setObjectName("spbx_cap_hue" + suffix)
        self.layout_vrt_frme_cap_hue_0.addWidget(self.spbx_cap_hue_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_hue_0)
        self.frme_cap_white_0 = qtw.QFrame(self.scar_con_cap_props_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_white_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_white_0.setSizePolicy(sizePolicy)
        self.frme_cap_white_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.frme_cap_white_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_white_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_white_0.setObjectName("frme_cap_white" + suffix)
        self.layout_vrt_frme_cap_white_0 = qtw.QVBoxLayout(self.frme_cap_white_0)
        self.layout_vrt_frme_cap_white_0.setContentsMargins(3, 0, 3, 0)
        self.layout_vrt_frme_cap_white_0.setSpacing(0)
        self.layout_vrt_frme_cap_white_0.setObjectName("layout_vrt_frme_cap_white" + suffix)
        self.lbl_static_white_0 = qtw.QLabel(self.frme_cap_white_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_white_0.sizePolicy().hasHeightForWidth())
        self.lbl_static_white_0.setSizePolicy(sizePolicy)
        self.lbl_static_white_0.setObjectName("lbl_static_white" + suffix)
        self.layout_vrt_frme_cap_white_0.addWidget(self.lbl_static_white_0)
        self.spbx_cap_white_0 = qtw.QSpinBox(self.frme_cap_white_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_cap_white_0.sizePolicy().hasHeightForWidth())
        self.spbx_cap_white_0.setSizePolicy(sizePolicy)
        self.spbx_cap_white_0.setMaximum(10000)
        self.spbx_cap_white_0.setSingleStep(10)
        self.spbx_cap_white_0.setProperty("value", 4600)
        self.spbx_cap_white_0.setObjectName("spbx_cap_white" + suffix)
        self.layout_vrt_frme_cap_white_0.addWidget(self.spbx_cap_white_0)
        self.chbx_cap_autowhite_0 = qtw.QCheckBox(self.frme_cap_white_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Ignored, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chbx_cap_autowhite_0.sizePolicy().hasHeightForWidth())
        self.chbx_cap_autowhite_0.setSizePolicy(sizePolicy)
        self.chbx_cap_autowhite_0.setLayoutDirection(qtc.Qt.LeftToRight)
        self.chbx_cap_autowhite_0.setChecked(True)
        self.chbx_cap_autowhite_0.setObjectName("chbx_cap_autowhite" + suffix)
        self.layout_vrt_frme_cap_white_0.addWidget(self.chbx_cap_autowhite_0)
        self.layout_vrt_scar_con_cap_props_0.addWidget(self.frme_cap_white_0)
        self.scar_cap_props_0.setWidget(self.scar_con_cap_props_0)
        self.layout_vrt_frme_cap_controls_0.addWidget(self.scar_cap_props_0)
        self.frme_cap_resolution_0 = qtw.QFrame(self.frme_cap_controls_0)
        self.frme_cap_resolution_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_resolution_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_resolution_0.setObjectName("frme_cap_resolution" + suffix)
        self.layout_grid_frme_cap_res_0 = qtw.QGridLayout(self.frme_cap_resolution_0)
        self.layout_grid_frme_cap_res_0.setContentsMargins(3, 0, 3, 1)
        self.layout_grid_frme_cap_res_0.setSpacing(0)
        self.layout_grid_frme_cap_res_0.setObjectName("layout_grid_frme_cap_res" + suffix)
        self.lbl_static_resolution_0 = qtw.QLabel(self.frme_cap_resolution_0)
        self.lbl_static_resolution_0.setAlignment(qtc.Qt.AlignLeading | qtc.Qt.AlignLeft | qtc.Qt.AlignVCenter)
        self.lbl_static_resolution_0.setObjectName("lbl_static_resolution" + suffix)
        self.layout_grid_frme_cap_res_0.addWidget(self.lbl_static_resolution_0, 0, 1, 1, 1)
        self.lbl_static_w_resolution_0 = qtw.QLabel(self.frme_cap_resolution_0)
        self.lbl_static_w_resolution_0.setAlignment(qtc.Qt.AlignCenter)
        self.lbl_static_w_resolution_0.setObjectName("lbl_static_w_resolution" + suffix)
        self.layout_grid_frme_cap_res_0.addWidget(self.lbl_static_w_resolution_0, 1, 0, 1, 1)
        self.ledit_cap_width_0 = qtw.QLineEdit(self.frme_cap_resolution_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ledit_cap_width_0.sizePolicy().hasHeightForWidth())
        self.ledit_cap_width_0.setSizePolicy(sizePolicy)
        self.ledit_cap_width_0.setReadOnly(True)
        self.ledit_cap_width_0.setObjectName("ledit_cap_width" + suffix)
        self.layout_grid_frme_cap_res_0.addWidget(self.ledit_cap_width_0, 1, 1, 1, 1)
        self.lbl_static_h_resolution_0 = qtw.QLabel(self.frme_cap_resolution_0)
        self.lbl_static_h_resolution_0.setAlignment(qtc.Qt.AlignCenter)
        self.lbl_static_h_resolution_0.setObjectName("lbl_static_h_resolution" + suffix)
        self.layout_grid_frme_cap_res_0.addWidget(self.lbl_static_h_resolution_0, 2, 0, 1, 1)
        self.ledit_cap_height_0 = qtw.QLineEdit(self.frme_cap_resolution_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ledit_cap_height_0.sizePolicy().hasHeightForWidth())
        self.ledit_cap_height_0.setSizePolicy(sizePolicy)
        self.ledit_cap_height_0.setReadOnly(True)
        self.ledit_cap_height_0.setObjectName("ledit_cap_height" + suffix)
        self.layout_grid_frme_cap_res_0.addWidget(self.ledit_cap_height_0, 2, 1, 1, 1)
        self.lbl_static_c_resolution_0 = qtw.QLabel(self.frme_cap_resolution_0)
        self.lbl_static_c_resolution_0.setAlignment(qtc.Qt.AlignCenter)
        self.lbl_static_c_resolution_0.setObjectName("lbl_static_c_resolution" + suffix)
        self.layout_grid_frme_cap_res_0.addWidget(self.lbl_static_c_resolution_0, 3, 0, 1, 1)
        self.ledit_cap_channels_0 = qtw.QLineEdit(self.frme_cap_resolution_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ledit_cap_channels_0.sizePolicy().hasHeightForWidth())
        self.ledit_cap_channels_0.setSizePolicy(sizePolicy)
        self.ledit_cap_channels_0.setText("")
        self.ledit_cap_channels_0.setReadOnly(True)
        self.ledit_cap_channels_0.setObjectName("ledit_cap_channels" + suffix)
        self.layout_grid_frme_cap_res_0.addWidget(self.ledit_cap_channels_0, 3, 1, 1, 1)
        self.layout_vrt_frme_cap_controls_0.addWidget(self.frme_cap_resolution_0)
        self.frme_cam_index_0 = qtw.QFrame(self.frme_cap_controls_0)
        self.frme_cam_index_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cam_index_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cam_index_0.setObjectName("frme_cam_index" + suffix)
        self.layout_hrz_cam_index_0 = qtw.QHBoxLayout(self.frme_cam_index_0)
        self.layout_hrz_cam_index_0.setContentsMargins(1, 0, 0, 0)
        self.layout_hrz_cam_index_0.setSpacing(0)
        self.layout_hrz_cam_index_0.setObjectName("layout_hrz_cam_index" + suffix)
        self.lbl_static_cam_index_0 = qtw.QLabel(self.frme_cam_index_0)
        self.lbl_static_cam_index_0.setObjectName("lbl_static_cam_index" + suffix)
        self.layout_hrz_cam_index_0.addWidget(self.lbl_static_cam_index_0)
        self.ledit_cam_index_0 = qtw.QLineEdit(self.frme_cam_index_0)
        self.ledit_cam_index_0.setMaximumSize(qtc.QSize(20, 16777215))
        self.ledit_cam_index_0.setObjectName("ledit_cam_index" + suffix)
        self.layout_hrz_cam_index_0.addWidget(self.ledit_cam_index_0)
        self.layout_vrt_frme_cap_controls_0.addWidget(self.frme_cam_index_0)

        self.frme_start_stop_cap_0 = qtw.QFrame(self.frme_cap_controls_0)
        self.frme_start_stop_cap_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_start_stop_cap_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_start_stop_cap_0.setObjectName("frme_start_stop_cap" + suffix)
        self.layout_hrz_frme_start_stop_cap_0 = qtw.QHBoxLayout(self.frme_start_stop_cap_0)
        self.layout_hrz_frme_start_stop_cap_0.setContentsMargins(0, 0, 0, 0)
        self.layout_hrz_frme_start_stop_cap_0.setSpacing(0)
        self.layout_hrz_frme_start_stop_cap_0.setObjectName("layout_hrz_frme_start_stop_cap" + suffix)
        self.btn_start_cap_0 = qtw.QPushButton(self.frme_start_stop_cap_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_start_cap_0.sizePolicy().hasHeightForWidth())
        self.btn_start_cap_0.setSizePolicy(sizePolicy)
        self.btn_start_cap_0.setObjectName("btn_start_cap" + suffix)
        self.layout_hrz_frme_start_stop_cap_0.addWidget(self.btn_start_cap_0)
        self.btn_stop_cap_0 = qtw.QPushButton(self.frme_start_stop_cap_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_stop_cap_0.sizePolicy().hasHeightForWidth())
        self.btn_stop_cap_0.setSizePolicy(sizePolicy)
        self.btn_stop_cap_0.setObjectName("btn_stop_cap" + suffix)
        self.layout_hrz_frme_start_stop_cap_0.addWidget(self.btn_stop_cap_0)
        self.layout_vrt_frme_cap_controls_0.addWidget(self.frme_start_stop_cap_0)

        self.layout_hrz_frme_cap_panel_0.addWidget(self.frme_cap_controls_0)
        self.frme_cap_display_0 = qtw.QFrame(self.frme_cap_panel_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frme_cap_display_0.sizePolicy().hasHeightForWidth())
        self.frme_cap_display_0.setSizePolicy(sizePolicy)
        self.frme_cap_display_0.setFrameShape(qtw.QFrame.StyledPanel)
        self.frme_cap_display_0.setFrameShadow(qtw.QFrame.Plain)
        self.frme_cap_display_0.setObjectName("frme_cap_display" + suffix)
        self.layout_grid_frme_cap_display_0 = qtw.QGridLayout(self.frme_cap_display_0)
        self.layout_grid_frme_cap_display_0.setContentsMargins(0, 0, 0, 0)
        self.layout_grid_frme_cap_display_0.setSpacing(0)
        self.layout_grid_frme_cap_display_0.setObjectName("layout_grid_frme_cap_display" + suffix)
        self.lbl_cap_display_pixmap_0 = qtw.QLabel(self.frme_cap_display_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_cap_display_pixmap_0.sizePolicy().hasHeightForWidth())
        self.lbl_cap_display_pixmap_0.setSizePolicy(sizePolicy)
        self.lbl_cap_display_pixmap_0.setContextMenuPolicy(qtc.Qt.DefaultContextMenu)
        self.lbl_cap_display_pixmap_0.setFrameShape(qtw.QFrame.Panel)
        self.lbl_cap_display_pixmap_0.setText("")
        self.lbl_cap_display_pixmap_0.setAlignment(qtc.Qt.AlignLeading | qtc.Qt.AlignLeft | qtc.Qt.AlignTop)
        self.lbl_cap_display_pixmap_0.setObjectName("lbl_cap_display_pixmap" + suffix)
        self.layout_grid_frme_cap_display_0.addWidget(self.lbl_cap_display_pixmap_0, 0, 0, 1, 1)
        self.sbar_vrt_cap_display_0 = qtw.QScrollBar(self.frme_cap_display_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Fixed, qtw.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbar_vrt_cap_display_0.sizePolicy().hasHeightForWidth())
        self.sbar_vrt_cap_display_0.setSizePolicy(sizePolicy)
        self.sbar_vrt_cap_display_0.setMaximumSize(qtc.QSize(15, 16777215))
        self.sbar_vrt_cap_display_0.setOrientation(qtc.Qt.Vertical)
        self.sbar_vrt_cap_display_0.setObjectName("sbar_vrt_cap_display" + suffix)
        self.layout_grid_frme_cap_display_0.addWidget(self.sbar_vrt_cap_display_0, 0, 1, 1, 1)
        self.sbar_hrz_cap_display_0 = qtw.QScrollBar(self.frme_cap_display_0)
        sizePolicy = qtw.QSizePolicy(qtw.QSizePolicy.Preferred, qtw.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbar_hrz_cap_display_0.sizePolicy().hasHeightForWidth())
        self.sbar_hrz_cap_display_0.setSizePolicy(sizePolicy)
        self.sbar_hrz_cap_display_0.setMaximumSize(qtc.QSize(16777215, 15))
        self.sbar_hrz_cap_display_0.setOrientation(qtc.Qt.Horizontal)
        self.sbar_hrz_cap_display_0.setObjectName("sbar_hrz_cap_display" + suffix)
        self.layout_grid_frme_cap_display_0.addWidget(self.sbar_hrz_cap_display_0, 1, 0, 1, 1)
        self.layout_hrz_frme_cap_panel_0.addWidget(self.frme_cap_display_0)

        blank_img = np.zeros((500, 500, 1), np.int)
        blank_qimg = qtg.QImage(blank_img.data, blank_img.shape[1], blank_img.shape[0], blank_img.strides[0],
                                qtg.QImage.Format_RGB888)
        blank_qpix = qtg.QPixmap.fromImage(blank_qimg)
        self.lbl_cap_display_pixmap_0.setPixmap(blank_qpix)

        self._set_text()

        self.capture_active = False
        self._create_capture_stream()
        self._connect_signals_to_slots()

        if space_available:
            qframe.layout().addWidget(self.frme_cap_panel_0, row, col, 1, 1)
        else:
            print('Max number of capture display panels reached.')

        print("cap_panel setup complete")


    @qtc.pyqtSlot(np.ndarray)
    def _display_capture(self, img):
        h, w, c = img.shape
        self.ledit_cap_width_0.setText(str(w))
        self.ledit_cap_height_0.setText(str(h))
        self.ledit_cap_channels_0.setText(str(c))
        chbx_pause = self.chbx_pause_0
        if not chbx_pause.isChecked():
            lbl_display = self.lbl_cap_display_pixmap_0
            sbar_hrz = self.sbar_hrz_cap_display_0
            sbar_vrt = self.sbar_vrt_cap_display_0
            dbsp_zoom = self.spbx_dbl_zoom_0
            spbx_rotate = self.spbx_rotate_image_0

            window_w = lbl_display.width()
            window_h = lbl_display.height()
            zoom = dbsp_zoom.value()  # float

            temp_window_w = int(window_w / zoom)
            temp_window_h = int(window_h / zoom)

            new_sbar_max = max(0, w - temp_window_w)
            sbar_max = sbar_hrz.maximum()
            sbar_max_no_zero = max(1, sbar_max)
            sbar_hrz_percent = sbar_hrz.value() / sbar_max_no_zero  # float
            if new_sbar_max != sbar_max:
                sbar_hrz.setMaximum(new_sbar_max)
                sbar_hrz.setValue(int(new_sbar_max * sbar_hrz_percent))

            new_sbar_max = max(0, h - temp_window_h)
            sbar_max = sbar_vrt.maximum()
            sbar_max_no_zero = max(1, sbar_max)
            sbar_vrt_percent = sbar_vrt.value() / sbar_max_no_zero  # float
            if new_sbar_max != sbar_max:
                sbar_vrt.setMaximum(new_sbar_max)
                sbar_vrt.setValue(int(new_sbar_max * sbar_vrt_percent))

            sbar_hrz_val = sbar_hrz.value()
            sbar_vrt_val = sbar_vrt.value()
            x1, = mut.min_max_clamp(0, w - temp_window_w, sbar_hrz_val)
            x2 = min(w, x1 + temp_window_w)
            y1, = mut.min_max_clamp(0, h - temp_window_h, sbar_vrt_val)
            y2 = min(h, y1 + temp_window_h)

            degrees = spbx_rotate.value()
            if degrees:
                view_w = x2 - x1
                view_h = y2 - y1
                view_cx = x1 + view_w // 2
                view_cy = y1 + view_h // 2
                if degrees == 90 or degrees == 270:
                    x1, = mut.min_max_clamp(0, w, view_cx - view_h // 2)
                    x2 = min(w, x1 + view_h)
                    y1, = mut.min_max_clamp(0, h, view_cy - view_w // 2)
                    y2 = min(h, y1 + view_w)
                    view = img[y1:y2, x1:x2].copy()
                    if degrees == 90:
                        view = cv2.rotate(view, cv2.ROTATE_90_CLOCKWISE)
                    else:
                        view = cv2.rotate(view, cv2.ROTATE_90_COUNTERCLOCKWISE)
                else:  # degrees == 180
                    view = img[y1:y2, x1:x2].copy()
                    view = cv2.rotate(view, cv2.ROTATE_180)
            else:
                view = img[y1:y2, x1:x2].copy()

            qimg = qtg.QImage(view.data, view.shape[1], view.shape[0], view.strides[0], qtg.QImage.Format_RGB888)
            qimg = qimg.scaled(window_w, window_h, qtc.Qt.KeepAspectRatio)
            qpix = qtg.QPixmap.fromImage(qimg)
            lbl_display.setPixmap(qpix)

    def _create_capture_stream(self):
        self.cap_stream = CaptureStream()
        self.cap_thread = qtc.QThread()
        self.cap_stream.moveToThread(self.cap_thread)
        self.cap_thread.start()
        print("capture stream created.")
        self.camera_capture_requested.connect(self.cap_stream.run)
        self.cap_stream.frame_captured.connect(self._display_capture)

    def _set_text(self):
        self.lbl_static_zoom_0.setText("Zoom")
        self.chbx_pause_0.setText("Pause")
        self.lbl_static_rotate_0.setText("Rotate (90)")
        self.lbl_static_focus_0.setText("Focus")
        self.chbx_cap_autofocus_0.setText("Auto")
        self.lbl_static_exposure_0.setText("Exposure")
        self.chbx_cap_autoexposure_0.setText("Auto")
        self.lbl_static_backlight_0.setText("Backlight")
        self.lbl_static_sharpness_0.setText("Sharpness")
        self.lbl_static_gamma_0.setText("Gamma")
        self.lbl_static_gain_0.setText("Gain")
        self.lbl_static_contrast_0.setText("Contrast")
        self.lbl_static_saturation_0.setText("Saturation")
        self.lbl_static_brightness_0.setText("Brightness")
        self.lbl_static_hue_0.setText("Hue")
        self.lbl_static_white_0.setText("White Bal.")
        self.chbx_cap_autowhite_0.setText("Auto")
        self.lbl_static_resolution_0.setText("Resolution")
        self.lbl_static_w_resolution_0.setText("W")
        self.ledit_cap_width_0.setText("5000")
        self.lbl_static_h_resolution_0.setText("H")
        self.ledit_cap_height_0.setText("4000")
        self.lbl_static_c_resolution_0.setText("C")
        self.lbl_static_cam_index_0.setText("Cam Index")
        self.btn_start_cap_0.setText("Start")
        self.btn_stop_cap_0.setText("Stop")

    def _connect_signals_to_slots(self):
        self.btn_start_cap_0.clicked.connect(self._send_capture_request)
        self.btn_stop_cap_0.clicked.connect(self._stop_capture)
        self.spbx_cap_focus_0.valueChanged.connect(self._send_focus_update_request)
        self.spbx_cap_backlight_0.valueChanged.connect(self._send_backlight_update_request)
        self.spbx_cap_brightness_0.valueChanged.connect(self._send_brightness_update_request)
        self.spbx_cap_contrast_0.valueChanged.connect(self._send_contrast_update_request)
        self.spbx_cap_exposure_0.valueChanged.connect(self._send_exposure_update_request)
        self.spbx_cap_gain_0.valueChanged.connect(self._send_gain_update_request)
        self.spbx_cap_gamma_0.valueChanged.connect(self._send_gamma_update_request)
        self.spbx_cap_hue_0.valueChanged.connect(self._send_hue_update_request)
        self.spbx_cap_saturation_0.valueChanged.connect(self._send_saturation_update_request)
        self.spbx_cap_sharpness_0.valueChanged.connect(self._send_sharpness_update_request)
        self.spbx_cap_white_0.valueChanged.connect(self._send_white_update_request)

        self.chbx_cap_autoexposure_0.stateChanged.connect(self._send_auto_exposure_update_request)
        self.chbx_cap_autofocus_0.stateChanged.connect(self._send_auto_focus_update_request)
        self.chbx_cap_autowhite_0.stateChanged.connect(self._send_auto_white_update_request)

    @_if_cap_active
    def _send_auto_focus_update_request(self, newval):
        self.cap_stream.update_auto_focus(newval)

    @_if_cap_active
    def _send_auto_exposure_update_request(self, newval):
        self.cap_stream.update_auto_exposure(newval)

    @_if_cap_active
    def _send_auto_white_update_request(self, newval):
        self.cap_stream.update_auto_white_balance(newval)

    @_if_cap_active
    def _send_focus_update_request(self, newval):
        self.cap_stream.update_focus(newval)

    @_if_cap_active
    def _send_backlight_update_request(self, newval):
        self.cap_stream.update_backlight_comp(newval)

    @_if_cap_active
    def _send_brightness_update_request(self, newval):
        self.cap_stream.update_brightness(newval)

    @_if_cap_active
    def _send_contrast_update_request(self, newval):
        self.cap_stream.update_contrast(newval)

    @_if_cap_active
    def _send_exposure_update_request(self, newval):
        self.cap_stream.update_exposure(newval)

    @_if_cap_active
    def _send_gain_update_request(self, newval):
        self.cap_stream.update_gain(newval)

    @_if_cap_active
    def _send_gamma_update_request(self, newval):
        self.cap_stream.update_gamma(newval)

    @_if_cap_active
    def _send_hue_update_request(self, newval):
        self.cap_stream.update_hue(newval)

    @_if_cap_active
    def _send_saturation_update_request(self, newval):
        self.cap_stream.update_saturation(newval)

    @_if_cap_active
    def _send_sharpness_update_request(self, newval):
        self.cap_stream.update_sharpness(newval)

    @_if_cap_active
    def _send_white_update_request(self, newval):
        self.cap_stream.update_white_balance(newval)

    @qtc.pyqtSlot()
    @_if_cap_not_active
    def _send_capture_request(self):
        self.capture_active = True
        # camera_index = int(self.ledit_cam_index_0.text())
        camera_index = 1
        self._send_auto_focus_update_request(int(self.chbx_cap_autofocus_0.isChecked()))
        self._send_auto_exposure_update_request(int(self.chbx_cap_autoexposure_0.isChecked()))
        self._send_auto_white_update_request(int(self.chbx_cap_autowhite_0.isChecked()))
        self._send_focus_update_request(self.spbx_cap_focus_0.value())
        self._send_brightness_update_request(self.spbx_cap_brightness_0.value())
        self._send_contrast_update_request(self.spbx_cap_contrast_0.value())
        self._send_hue_update_request(self.spbx_cap_hue_0.value())
        self._send_saturation_update_request(self.spbx_cap_saturation_0.value())
        self._send_sharpness_update_request(self.spbx_cap_sharpness_0.value())
        self._send_gamma_update_request(self.spbx_cap_gamma_0.value())
        self._send_white_update_request(self.spbx_cap_white_0.value())
        self._send_backlight_update_request(self.spbx_cap_backlight_0.value())
        self._send_gain_update_request(self.spbx_cap_gain_0.value())
        self._send_exposure_update_request(self.spbx_cap_exposure_0.value())
        print("emitting camera_capture_requested signal.")
        self.camera_capture_requested.emit(camera_index)

    @qtc.pyqtSlot()
    @_if_cap_active
    def _stop_capture(self):
        self.capture_active = False
        self.cap_stream.stop()

    @staticmethod
    def _get_row_col(qframe):
        i = qframe.layout().count()
        space_available = True
        if i == 0:
            row = 0
            col = 0
        elif i == 1:
            row = 1
            col = 0
        elif i == 2:
            row = 0
            col = 1
        elif i == 3:
            row = 1
            col = 1
        else:
            row = 2
            col = 2
            space_available = False
        return row, col, space_available


class CaptureStream(qtc.QObject):
    frame_captured = qtc.pyqtSignal(np.ndarray)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.thread_active = False
        self.width = 5000
        self.height = 4000
        self.focus = 300.
        self.auto_focus = 0
        self.brightness = 0
        self.contrast = 32
        self.hue = 0
        self.saturation = 64
        self.sharpness = 3
        self.gamma = 100
        self.white_balance = 4600
        self.auto_white_balance = 1
        self.backlight_comp = 1
        self.gain = 0
        self.exposure = -6
        self.auto_exposure = 1  # if disabled, must be re-enabled in AMcap software

    @qtc.pyqtSlot(int)
    def run(self, cam_index):
        print("capture stream run()")
        self.thread_active = True
        cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
        # 16MP camera = 4672x3504
        # 8MP 3264x2448
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        focus = self.focus
        auto_focus = self.auto_focus
        brightness = self.brightness
        contrast = self.contrast
        hue = self.hue
        saturation = self.saturation
        sharpness = self.sharpness
        gamma = self.gamma
        white_balance = self.white_balance
        auto_white_balance = self.auto_white_balance
        backlight_comp = self.backlight_comp
        gain = self.gain
        exposure = self.exposure
        auto_exposure = self.auto_exposure

        # cap.set(cv2.CAP_PROP_AUTOFOCUS, auto_focus)
        if not auto_focus:
            cap.set(cv2.CAP_PROP_FOCUS, focus)
        cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
        cap.set(cv2.CAP_PROP_CONTRAST, contrast)
        cap.set(cv2.CAP_PROP_HUE, hue)
        cap.set(cv2.CAP_PROP_SATURATION, saturation)
        cap.set(cv2.CAP_PROP_GAMMA, gamma)
        cap.set(cv2.CAP_PROP_AUTO_WB, auto_white_balance)
        if not auto_white_balance:
            cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, white_balance)
            cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, white_balance)
        cap.set(cv2.CAP_PROP_BACKLIGHT, backlight_comp)
        cap.set(cv2.CAP_PROP_GAIN, gain)
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)
        if not auto_exposure:
            cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
        count = 0
        while cap.isOpened() and self.thread_active:
            ret, frame = cap.read()
            count = count + 1
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_captured.emit(frame_rgb)
                if not auto_focus == self.auto_focus:
                    auto_focus = self.auto_focus
                    cap.set(cv2.CAP_PROP_AUTOFOCUS, auto_focus)
                    print("Auto-focus set to: " + str(auto_focus))
                    print("Auto-focus is: " + str(cap.get(cv2.CAP_PROP_AUTOFOCUS)))
                elif abs(focus - self.focus) >= 1:
                    focus = self.focus
                    if not auto_focus:
                        cap.set(cv2.CAP_PROP_FOCUS, focus)
                        print("Focus set to: " + str(focus))
                        print("Focus is: " + str(cap.get(cv2.CAP_PROP_FOCUS)))
                elif not auto_white_balance == self.auto_white_balance:
                    auto_white_balance = self.auto_white_balance
                    cap.set(cv2.CAP_PROP_AUTO_WB, auto_white_balance)
                elif abs(white_balance - self.white_balance) >= 1:
                    white_balance = self.white_balance
                    if not auto_white_balance:
                        cap.set(cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, self.white_balance)
                        cap.set(cv2.CAP_PROP_WHITE_BALANCE_RED_V, self.white_balance)
                elif not auto_exposure == self.auto_exposure:
                    auto_exposure = self.auto_exposure
                    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)
                elif abs(exposure - self.exposure) >= 1:
                    exposure = self.exposure
                    if not auto_exposure:
                        cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
                        print("Exposure set to: " + str(exposure))
                        print("Exposure is: " + str(cap.get(cv2.CAP_PROP_EXPOSURE)))
                    else:
                        print("auto exposure = 1. no change.")
                elif abs(gain - self.gain) >= 1:
                    gain = self.gain
                    cap.set(cv2.CAP_PROP_GAIN, gain)
                    print("Gain set to: " + str(gain))
                    print("Gain is: " + str(cap.get(cv2.CAP_PROP_GAIN)))
                elif abs(gamma - self.gamma) >= 1:
                    gamma = self.gamma
                    cap.set(cv2.CAP_PROP_GAMMA, gamma)
                    print("Gamma set to: " + str(gamma))
                    print("Gamma is: " + str(cap.get(cv2.CAP_PROP_GAMMA)))
                elif abs(brightness - self.brightness) >= 1:
                    brightness = self.brightness
                    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
                    print("Brightness set to: " + str(brightness))
                    print("Brightness is: " + str(cap.get(cv2.CAP_PROP_BRIGHTNESS)))
                elif abs(contrast - self.contrast) >= 1:
                    contrast = self.contrast
                    cap.set(cv2.CAP_PROP_CONTRAST, contrast)
                    print("Contrast set to: " + str(contrast))
                    print("Contrast is: " + str(cap.get(cv2.CAP_PROP_CONTRAST)))
                elif abs(sharpness - self.sharpness) >= 1:
                    sharpness = self.sharpness
                    cap.set(cv2.CAP_PROP_SHARPNESS, sharpness)
                    print("Sharpness set to: " + str(sharpness))
                    print("Sharpness is: " + str(cap.get(cv2.CAP_PROP_SHARPNESS)))
                elif abs(saturation - self.saturation) >= 1:
                    saturation = self.saturation
                    cap.set(cv2.CAP_PROP_SATURATION, saturation)
                    print("Saturation set to: " + str(saturation))
                    print("Saturation is: " + str(cap.get(cv2.CAP_PROP_SATURATION)))
                elif abs(hue - self.hue) >= 1:
                    hue = self.hue
                    cap.set(cv2.CAP_PROP_HUE, hue)
                    print("Hue set to: " + str(hue))
                    print("Hue is: " + str(cap.get(cv2.CAP_PROP_HUE)))
                elif abs(backlight_comp - self.backlight_comp) >= 1:
                    backlight_comp = self.backlight_comp
                    cap.set(cv2.CAP_PROP_BACKLIGHT, backlight_comp)
                    print("Backlight comp set to: " + str(backlight_comp))
                    print("Backlight comp is: " + str(cap.get(cv2.CAP_PROP_BACKLIGHT)))
            else:
                self.stop()
                print("Capture read unsuccessful. Cam index: " + str(cam_index))

        cap.release()
        print("Capture stopped. Cam index: " + str(cam_index))

    def stop(self):
        self.thread_active = False

    def update_focus(self, focus):
        self.focus = focus

    def update_auto_focus(self, auto):
        self.auto_focus = auto

    def update_brightness(self, brightness):
        self.brightness = brightness

    def update_contrast(self, contrast):
        self.contrast = contrast

    def update_hue(self, hue):
        self.hue = hue

    def update_saturation(self, saturation):
        self.saturation = saturation

    def update_sharpness(self, sharpness):
        self.sharpness = sharpness

    def update_gamma(self, gamma):
        self.gamma = gamma

    def update_white_balance(self, white_balance):
        self.white_balance = white_balance

    def update_auto_white_balance(self, auto):
        self.auto_white_balance = auto

    def update_backlight_comp(self, backlight_comp):
        self.backlight_comp = backlight_comp

    def update_gain(self, gain):
        self.gain = gain

    def update_exposure(self, exposure):
        self.exposure = exposure

    def update_auto_exposure(self, auto):
        self.auto_exposure = auto
