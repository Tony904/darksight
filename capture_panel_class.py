from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class CapturePanel(QtWidgets.QFrame):

    def setupUi(self, Frame):
        row, col, space_available = self.__get_row_col(Frame)
        suffix = "_" + str(2 * col + row)

        self.frme_capture_panel = QtWidgets.QFrame(Frame)
        self.frme_capture_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_capture_panel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_capture_panel.setObjectName("frme_capture_panel" + suffix)
        self.layout_hrz_frme_capture_panel = QtWidgets.QHBoxLayout(self.frme_capture_panel)
        self.layout_hrz_frme_capture_panel.setSpacing(0)
        self.layout_hrz_frme_capture_panel.setObjectName("layout_hrz_frme_capture_panel" + suffix)
        self.frme_capture_panel_controls = QtWidgets.QFrame(self.frme_capture_panel)
        self.frme_capture_panel_controls.setMaximumSize(QtCore.QSize(50, 16777215))
        self.frme_capture_panel_controls.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_capture_panel_controls.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_capture_panel_controls.setObjectName("frme_capture_panel_controls" + suffix)
        self.layout_vrt_frme_capture_panel_controls = QtWidgets.QVBoxLayout(self.frme_capture_panel_controls)
        self.layout_vrt_frme_capture_panel_controls.setContentsMargins(0, 0, 0, 0)
        self.layout_vrt_frme_capture_panel_controls.setSpacing(0)
        self.layout_vrt_frme_capture_panel_controls.setObjectName("layout_vrt_frme_capture_panel_controls" + suffix)
        self.frme_zoom_panel = QtWidgets.QFrame(self.frme_capture_panel_controls)
        self.frme_zoom_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_zoom_panel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_zoom_panel.setObjectName("frme_zoom_panel" + suffix)
        self.layout_vrt_frme_zoom_panel = QtWidgets.QVBoxLayout(self.frme_zoom_panel)
        self.layout_vrt_frme_zoom_panel.setContentsMargins(0, 0, 0, 0)
        self.layout_vrt_frme_zoom_panel.setSpacing(0)
        self.layout_vrt_frme_zoom_panel.setObjectName("layout_vrt_frme_zoom_panel" + suffix)
        self.lbl_static_zoom = QtWidgets.QLabel(self.frme_zoom_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_static_zoom.sizePolicy().hasHeightForWidth())
        self.lbl_static_zoom.setSizePolicy(sizePolicy)
        self.lbl_static_zoom.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lbl_static_zoom.setFont(font)
        self.lbl_static_zoom.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.lbl_static_zoom.setObjectName("lbl_static_zoom" + suffix)
        self.layout_vrt_frme_zoom_panel.addWidget(self.lbl_static_zoom)
        self.spbx_dbl_zoom = QtWidgets.QDoubleSpinBox(self.frme_zoom_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spbx_dbl_zoom.sizePolicy().hasHeightForWidth())
        self.spbx_dbl_zoom.setSizePolicy(sizePolicy)
        self.spbx_dbl_zoom.setMaximumSize(QtCore.QSize(1000, 0))
        self.spbx_dbl_zoom.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.spbx_dbl_zoom.setAlignment(QtCore.Qt.AlignCenter)
        self.spbx_dbl_zoom.setDecimals(2)
        self.spbx_dbl_zoom.setMinimum(0.01)
        self.spbx_dbl_zoom.setMaximum(3.0)
        self.spbx_dbl_zoom.setSingleStep(0.1)
        self.spbx_dbl_zoom.setProperty("value", 1.0)
        self.spbx_dbl_zoom.setObjectName("spbx_dbl_zoom" + suffix)
        self.layout_vrt_frme_zoom_panel.addWidget(self.spbx_dbl_zoom)
        self.layout_vrt_frme_capture_panel_controls.addWidget(self.frme_zoom_panel)
        self.frme_freeze_frame_panel = QtWidgets.QFrame(self.frme_capture_panel_controls)
        self.frme_freeze_frame_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_freeze_frame_panel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_freeze_frame_panel.setObjectName("frme_freeze_frame_panel" + suffix)
        self.layout_vert_frme_freeze_frame_panel = QtWidgets.QVBoxLayout(self.frme_freeze_frame_panel)
        self.layout_vert_frme_freeze_frame_panel.setContentsMargins(0, 0, 0, 0)
        self.layout_vert_frme_freeze_frame_panel.setSpacing(0)
        self.layout_vert_frme_freeze_frame_panel.setObjectName("layout_vert_frme_freeze_frame_panel" + suffix)
        self.lbl_static_freeze_frame = QtWidgets.QLabel(self.frme_freeze_frame_panel)
        self.lbl_static_freeze_frame.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_static_freeze_frame.setWordWrap(True)
        self.lbl_static_freeze_frame.setObjectName("lbl_static_freeze_frame" + suffix)
        self.layout_vert_frme_freeze_frame_panel.addWidget(self.lbl_static_freeze_frame)
        self.frme_freeze_frame_checkbox = QtWidgets.QFrame(self.frme_freeze_frame_panel)
        self.frme_freeze_frame_checkbox.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_freeze_frame_checkbox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_freeze_frame_checkbox.setObjectName("frme_freeze_frame_checkbox" + suffix)
        self.layout_hrz_frme_freeze_frame_checkbox = QtWidgets.QHBoxLayout(self.frme_freeze_frame_checkbox)
        self.layout_hrz_frme_freeze_frame_checkbox.setContentsMargins(0, 0, 0, 0)
        self.layout_hrz_frme_freeze_frame_checkbox.setSpacing(0)
        self.layout_hrz_frme_freeze_frame_checkbox.setObjectName("layout_hrz_frme_freeze_frame_checkbox" + suffix)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.layout_hrz_frme_freeze_frame_checkbox.addItem(spacerItem)
        self.chbx_freeze_frame = QtWidgets.QCheckBox(self.frme_freeze_frame_checkbox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.chbx_freeze_frame.sizePolicy().hasHeightForWidth())
        self.chbx_freeze_frame.setSizePolicy(sizePolicy)
        self.chbx_freeze_frame.setMaximumSize(QtCore.QSize(15, 20))
        self.chbx_freeze_frame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chbx_freeze_frame.setText("")
        self.chbx_freeze_frame.setTristate(False)
        self.chbx_freeze_frame.setObjectName("chbx_freeze_frame" + suffix)
        self.layout_hrz_frme_freeze_frame_checkbox.addWidget(self.chbx_freeze_frame)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.layout_hrz_frme_freeze_frame_checkbox.addItem(spacerItem1)
        self.layout_vert_frme_freeze_frame_panel.addWidget(self.frme_freeze_frame_checkbox)
        self.layout_vrt_frme_capture_panel_controls.addWidget(self.frme_freeze_frame_panel)
        spacerItem2 = QtWidgets.QSpacerItem(45, 507, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.layout_vrt_frme_capture_panel_controls.addItem(spacerItem2)
        self.layout_hrz_frme_capture_panel.addWidget(self.frme_capture_panel_controls)
        self.frme_capture_display_panel = QtWidgets.QFrame(self.frme_capture_panel)
        self.frme_capture_display_panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_capture_display_panel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_capture_display_panel.setObjectName("frme_capture_display_panel" + suffix)
        self.layout_grid_frme_capture_display_panel = QtWidgets.QGridLayout(self.frme_capture_display_panel)
        self.layout_grid_frme_capture_display_panel.setContentsMargins(0, 0, 0, 0)
        self.layout_grid_frme_capture_display_panel.setSpacing(0)
        self.layout_grid_frme_capture_display_panel.setObjectName("layout_grid_frme_capture_display_panel" + suffix)
        self.lbl_capture_display_pixmap = QtWidgets.QLabel(self.frme_capture_display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_capture_display_pixmap.sizePolicy().hasHeightForWidth())
        self.lbl_capture_display_pixmap.setSizePolicy(sizePolicy)
        self.lbl_capture_display_pixmap.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lbl_capture_display_pixmap.setFrameShape(QtWidgets.QFrame.Panel)
        self.lbl_capture_display_pixmap.setText("")
        self.lbl_capture_display_pixmap.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.lbl_capture_display_pixmap.setObjectName("lbl_capture_display_pixmap" + suffix)
        self.layout_grid_frme_capture_display_panel.addWidget(self.lbl_capture_display_pixmap, 0, 0, 1, 1)
        self.sbar_vrt_capture_display = QtWidgets.QScrollBar(self.frme_capture_display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbar_vrt_capture_display.sizePolicy().hasHeightForWidth())
        self.sbar_vrt_capture_display.setSizePolicy(sizePolicy)
        self.sbar_vrt_capture_display.setMaximumSize(QtCore.QSize(15, 16777215))
        self.sbar_vrt_capture_display.setOrientation(QtCore.Qt.Vertical)
        self.sbar_vrt_capture_display.setObjectName("sbar_vrt_capture_display" + suffix)
        self.layout_grid_frme_capture_display_panel.addWidget(self.sbar_vrt_capture_display, 0, 1, 1, 1)
        self.sbar_hzt_capture_display = QtWidgets.QScrollBar(self.frme_capture_display_panel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sbar_hzt_capture_display.sizePolicy().hasHeightForWidth())
        self.sbar_hzt_capture_display.setSizePolicy(sizePolicy)
        self.sbar_hzt_capture_display.setMaximumSize(QtCore.QSize(16777215, 15))
        self.sbar_hzt_capture_display.setOrientation(QtCore.Qt.Horizontal)
        self.sbar_hzt_capture_display.setObjectName("sbar_hzt_capture_display" + suffix)
        self.layout_grid_frme_capture_display_panel.addWidget(self.sbar_hzt_capture_display, 1, 0, 1, 1)
        self.layout_hrz_frme_capture_panel.addWidget(self.frme_capture_display_panel)

        if space_available:
            Frame.layout().addWidget(self.frme_capture_panel, row, col, 1, 1)
        else:
            print('Max number of capture display panels reached.')

        self.__set_text()

    def __set_text(self):
        self.lbl_static_zoom.setText("Zoom")
        self.lbl_static_freeze_frame.setText("Freeze Frame")

    @staticmethod
    def __get_row_col(Frame):
        i = Frame.layout().count()
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
