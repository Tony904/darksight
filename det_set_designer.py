# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detection_settings_designer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_form_detection_settings(object):
    def setupUi(self, form_detection_settings):
        form_detection_settings.setObjectName("form_detection_settings")
        form_detection_settings.resize(1063, 618)
        self.layout_vrt_form_det_set = QtWidgets.QVBoxLayout(form_detection_settings)
        self.layout_vrt_form_det_set.setObjectName("layout_vrt_form_det_set")
        self.tabs_wdgt_det_set_panels = QtWidgets.QTabWidget(form_detection_settings)
        self.tabs_wdgt_det_set_panels.setObjectName("tabs_wdgt_det_set_panels")
        self.tab_det_set_p0 = QtWidgets.QWidget()
        self.tab_det_set_p0.setObjectName("tab_det_set_p0")
        self.layout_grid_tabs_wdgt_det_set_panels = QtWidgets.QGridLayout(self.tab_det_set_p0)
        self.layout_grid_tabs_wdgt_det_set_panels.setObjectName("layout_grid_tabs_wdgt_det_set_panels")
        self.chbx_enable_dets_p0 = QtWidgets.QCheckBox(self.tab_det_set_p0)
        self.chbx_enable_dets_p0.setObjectName("chbx_enable_dets_p0")
        self.layout_grid_tabs_wdgt_det_set_panels.addWidget(self.chbx_enable_dets_p0, 0, 0, 1, 1)
        self.frme_det_recipe_builder_p0 = QtWidgets.QFrame(self.tab_det_set_p0)
        self.frme_det_recipe_builder_p0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_det_recipe_builder_p0.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_det_recipe_builder_p0.setObjectName("frme_det_recipe_builder_p0")
        self.layout_vrt_frme_recipe_builder_p0 = QtWidgets.QVBoxLayout(self.frme_det_recipe_builder_p0)
        self.layout_vrt_frme_recipe_builder_p0.setObjectName("layout_vrt_frme_recipe_builder_p0")
        self.btn_new_detection_0 = QtWidgets.QPushButton(self.frme_det_recipe_builder_p0)
        self.btn_new_detection_0.setObjectName("btn_new_detection_0")
        self.layout_vrt_frme_recipe_builder_p0.addWidget(self.btn_new_detection_0)
        self.tabs_wdgt_dets_p0 = QtWidgets.QTabWidget(self.frme_det_recipe_builder_p0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabs_wdgt_dets_p0.sizePolicy().hasHeightForWidth())
        self.tabs_wdgt_dets_p0.setSizePolicy(sizePolicy)
        self.tabs_wdgt_dets_p0.setObjectName("tabs_wdgt_dets_p0")
        self.tab_det0_p0 = QtWidgets.QWidget()
        self.tab_det0_p0.setObjectName("tab_det0_p0")
        self.layout_vrt_wtab_det_0 = QtWidgets.QVBoxLayout(self.tab_det0_p0)
        self.layout_vrt_wtab_det_0.setObjectName("layout_vrt_wtab_det_0")
        self.lbl_static_type_det0_p0 = QtWidgets.QLabel(self.tab_det0_p0)
        self.lbl_static_type_det0_p0.setObjectName("lbl_static_type_det0_p0")
        self.layout_vrt_wtab_det_0.addWidget(self.lbl_static_type_det0_p0)
        self.cmbo_det_type_det0_p0 = QtWidgets.QComboBox(self.tab_det0_p0)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbo_det_type_det0_p0.sizePolicy().hasHeightForWidth())
        self.cmbo_det_type_det0_p0.setSizePolicy(sizePolicy)
        self.cmbo_det_type_det0_p0.setMaximumSize(QtCore.QSize(200, 16777215))
        self.cmbo_det_type_det0_p0.setObjectName("cmbo_det_type_det0_p0")
        self.cmbo_det_type_det0_p0.addItem("")
        self.cmbo_det_type_det0_p0.addItem("")
        self.layout_vrt_wtab_det_0.addWidget(self.cmbo_det_type_det0_p0)
        self.stck_det0_p0 = QtWidgets.QStackedWidget(self.tab_det0_p0)
        self.stck_det0_p0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.stck_det0_p0.setObjectName("stck_det0_p0")
        self.stck_page0_det0_p0 = QtWidgets.QWidget()
        self.stck_page0_det0_p0.setObjectName("stck_page0_det0_p0")
        self.btn_define_det_zone_0 = QtWidgets.QPushButton(self.stck_page0_det0_p0)
        self.btn_define_det_zone_0.setGeometry(QtCore.QRect(10, 10, 81, 34))
        self.btn_define_det_zone_0.setObjectName("btn_define_det_zone_0")
        self.ledit_top_page0_det0_p0 = QtWidgets.QLineEdit(self.stck_page0_det0_p0)
        self.ledit_top_page0_det0_p0.setGeometry(QtCore.QRect(80, 50, 71, 20))
        self.ledit_top_page0_det0_p0.setObjectName("ledit_top_page0_det0_p0")
        self.ledit_left_page0_det0_p0 = QtWidgets.QLineEdit(self.stck_page0_det0_p0)
        self.ledit_left_page0_det0_p0.setGeometry(QtCore.QRect(80, 80, 71, 20))
        self.ledit_left_page0_det0_p0.setObjectName("ledit_left_page0_det0_p0")
        self.lbl_static_top_page0_d0_p0 = QtWidgets.QLabel(self.stck_page0_det0_p0)
        self.lbl_static_top_page0_d0_p0.setGeometry(QtCore.QRect(10, 50, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_static_top_page0_d0_p0.setFont(font)
        self.lbl_static_top_page0_d0_p0.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_static_top_page0_d0_p0.setObjectName("lbl_static_top_page0_d0_p0")
        self.lbl_static_left_page0_det0_p0 = QtWidgets.QLabel(self.stck_page0_det0_p0)
        self.lbl_static_left_page0_det0_p0.setGeometry(QtCore.QRect(10, 80, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_static_left_page0_det0_p0.setFont(font)
        self.lbl_static_left_page0_det0_p0.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_static_left_page0_det0_p0.setObjectName("lbl_static_left_page0_det0_p0")
        self.lbl_bottom_page0_det0_p0 = QtWidgets.QLabel(self.stck_page0_det0_p0)
        self.lbl_bottom_page0_det0_p0.setGeometry(QtCore.QRect(10, 110, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_bottom_page0_det0_p0.setFont(font)
        self.lbl_bottom_page0_det0_p0.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_bottom_page0_det0_p0.setObjectName("lbl_bottom_page0_det0_p0")
        self.lbl_static_right_page0_det0_p0 = QtWidgets.QLabel(self.stck_page0_det0_p0)
        self.lbl_static_right_page0_det0_p0.setGeometry(QtCore.QRect(10, 140, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_static_right_page0_det0_p0.setFont(font)
        self.lbl_static_right_page0_det0_p0.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_static_right_page0_det0_p0.setObjectName("lbl_static_right_page0_det0_p0")
        self.ledit_bottom_page0_det0_p0 = QtWidgets.QLineEdit(self.stck_page0_det0_p0)
        self.ledit_bottom_page0_det0_p0.setGeometry(QtCore.QRect(80, 110, 71, 20))
        self.ledit_bottom_page0_det0_p0.setObjectName("ledit_bottom_page0_det0_p0")
        self.ledit_right_page0_det0_p0 = QtWidgets.QLineEdit(self.stck_page0_det0_p0)
        self.ledit_right_page0_det0_p0.setGeometry(QtCore.QRect(80, 140, 71, 20))
        self.ledit_right_page0_det0_p0.setObjectName("ledit_right_page0_det0_p0")
        self.frme_btns_top_page0_det0_p0 = QtWidgets.QFrame(self.stck_page0_det0_p0)
        self.frme_btns_top_page0_det0_p0.setGeometry(QtCore.QRect(160, 50, 16, 20))
        self.frme_btns_top_page0_det0_p0.setAutoFillBackground(False)
        self.frme_btns_top_page0_det0_p0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_btns_top_page0_det0_p0.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_btns_top_page0_det0_p0.setObjectName("frme_btns_top_page0_det0_p0")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frme_btns_top_page0_det0_p0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.btn_top_up_page0_det0_p0 = QtWidgets.QPushButton(self.frme_btns_top_page0_det0_p0)
        self.btn_top_up_page0_det0_p0.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Resources/up_arrow.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_top_up_page0_det0_p0.setIcon(icon)
        self.btn_top_up_page0_det0_p0.setObjectName("btn_top_up_page0_det0_p0")
        self.verticalLayout_3.addWidget(self.btn_top_up_page0_det0_p0)
        self.btn_top_down_page0_det0_p0 = QtWidgets.QPushButton(self.frme_btns_top_page0_det0_p0)
        self.btn_top_down_page0_det0_p0.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Resources/down_arrow.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_top_down_page0_det0_p0.setIcon(icon1)
        self.btn_top_down_page0_det0_p0.setIconSize(QtCore.QSize(16, 16))
        self.btn_top_down_page0_det0_p0.setObjectName("btn_top_down_page0_det0_p0")
        self.verticalLayout_3.addWidget(self.btn_top_down_page0_det0_p0)
        self.stck_det0_p0.addWidget(self.stck_page0_det0_p0)
        self.stck_page1_det0_p0 = QtWidgets.QWidget()
        self.stck_page1_det0_p0.setObjectName("stck_page1_det0_p0")
        self.stck_det0_p0.addWidget(self.stck_page1_det0_p0)
        self.layout_vrt_wtab_det_0.addWidget(self.stck_det0_p0)
        self.tabs_wdgt_dets_p0.addTab(self.tab_det0_p0, "")
        self.tab_det1_p0 = QtWidgets.QWidget()
        self.tab_det1_p0.setObjectName("tab_det1_p0")
        self.tabs_wdgt_dets_p0.addTab(self.tab_det1_p0, "")
        self.layout_vrt_frme_recipe_builder_p0.addWidget(self.tabs_wdgt_dets_p0)
        self.layout_grid_tabs_wdgt_det_set_panels.addWidget(self.frme_det_recipe_builder_p0, 1, 0, 1, 1)
        self.frme_det_set_img_p0 = QtWidgets.QFrame(self.tab_det_set_p0)
        self.frme_det_set_img_p0.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frme_det_set_img_p0.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frme_det_set_img_p0.setObjectName("frme_det_set_img_p0")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frme_det_set_img_p0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_det_set_pixmap_p0 = QtWidgets.QLabel(self.frme_det_set_img_p0)
        self.lbl_det_set_pixmap_p0.setText("")
        self.lbl_det_set_pixmap_p0.setObjectName("lbl_det_set_pixmap_p0")
        self.verticalLayout_2.addWidget(self.lbl_det_set_pixmap_p0)
        self.layout_grid_tabs_wdgt_det_set_panels.addWidget(self.frme_det_set_img_p0, 1, 1, 1, 1)
        self.tabs_wdgt_det_set_panels.addTab(self.tab_det_set_p0, "")
        self.tab_panel_1 = QtWidgets.QWidget()
        self.tab_panel_1.setObjectName("tab_panel_1")
        self.tabs_wdgt_det_set_panels.addTab(self.tab_panel_1, "")
        self.layout_vrt_form_det_set.addWidget(self.tabs_wdgt_det_set_panels)

        self.retranslateUi(form_detection_settings)
        self.tabs_wdgt_det_set_panels.setCurrentIndex(0)
        self.tabs_wdgt_dets_p0.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(form_detection_settings)

    def retranslateUi(self, form_detection_settings):
        _translate = QtCore.QCoreApplication.translate
        form_detection_settings.setWindowTitle(_translate("form_detection_settings", "Form"))
        self.chbx_enable_dets_p0.setText(_translate("form_detection_settings", "Enable Detection"))
        self.btn_new_detection_0.setText(_translate("form_detection_settings", "Create New Detection"))
        self.lbl_static_type_det0_p0.setText(_translate("form_detection_settings", "Type"))
        self.cmbo_det_type_det0_p0.setItemText(0, _translate("form_detection_settings", "Single Character"))
        self.cmbo_det_type_det0_p0.setItemText(1, _translate("form_detection_settings", "String"))
        self.btn_define_det_zone_0.setText(_translate("form_detection_settings", "Define\n"
"Detection Zone"))
        self.lbl_static_top_page0_d0_p0.setText(_translate("form_detection_settings", "Top"))
        self.lbl_static_left_page0_det0_p0.setText(_translate("form_detection_settings", "Left"))
        self.lbl_bottom_page0_det0_p0.setText(_translate("form_detection_settings", "Bottom"))
        self.lbl_static_right_page0_det0_p0.setText(_translate("form_detection_settings", "Right"))
        self.tabs_wdgt_dets_p0.setTabText(self.tabs_wdgt_dets_p0.indexOf(self.tab_det0_p0), _translate("form_detection_settings", "Det 0"))
        self.tabs_wdgt_dets_p0.setTabText(self.tabs_wdgt_dets_p0.indexOf(self.tab_det1_p0), _translate("form_detection_settings", "Det 1"))
        self.tabs_wdgt_det_set_panels.setTabText(self.tabs_wdgt_det_set_panels.indexOf(self.tab_det_set_p0), _translate("form_detection_settings", "Panel 0"))
        self.tabs_wdgt_det_set_panels.setTabText(self.tabs_wdgt_det_set_panels.indexOf(self.tab_panel_1), _translate("form_detection_settings", "Panel 1"))