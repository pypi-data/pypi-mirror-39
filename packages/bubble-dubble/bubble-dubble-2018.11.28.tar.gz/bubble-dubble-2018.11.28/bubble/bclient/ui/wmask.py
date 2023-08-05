# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/satarsa/projects/python/bubble/bubble/bclient/ui/wmask.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WMask(object):
    def setupUi(self, WMask):
        WMask.setObjectName("WMask")
        WMask.resize(999, 638)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/mask"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WMask.setWindowIcon(icon)
        self.verticalLayout = QtWidgets.QVBoxLayout(WMask)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkInvert = QtWidgets.QCheckBox(WMask)
        self.checkInvert.setObjectName("checkInvert")
        self.horizontalLayout.addWidget(self.checkInvert)
        self.lessCheckbox = QtWidgets.QCheckBox(WMask)
        self.lessCheckbox.setObjectName("lessCheckbox")
        self.horizontalLayout.addWidget(self.lessCheckbox)
        self.lessEdit = QtWidgets.QLineEdit(WMask)
        self.lessEdit.setObjectName("lessEdit")
        self.horizontalLayout.addWidget(self.lessEdit)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.moreCheckbox = QtWidgets.QCheckBox(WMask)
        self.moreCheckbox.setObjectName("moreCheckbox")
        self.horizontalLayout_2.addWidget(self.moreCheckbox)
        self.moreEdit = QtWidgets.QLineEdit(WMask)
        self.moreEdit.setObjectName("moreEdit")
        self.horizontalLayout_2.addWidget(self.moreEdit)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.polyButton = QtWidgets.QPushButton(WMask)
        self.polyButton.setObjectName("polyButton")
        self.horizontalLayout_3.addWidget(self.polyButton)
        self.ellipseButton = QtWidgets.QPushButton(WMask)
        self.ellipseButton.setObjectName("ellipseButton")
        self.horizontalLayout_3.addWidget(self.ellipseButton)
        self.buttonCircle = QtWidgets.QPushButton(WMask)
        self.buttonCircle.setObjectName("buttonCircle")
        self.horizontalLayout_3.addWidget(self.buttonCircle)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.imageView = ImageView(WMask)
        self.imageView.setObjectName("imageView")
        self.verticalLayout.addWidget(self.imageView)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.openImageButton = QtWidgets.QPushButton(WMask)
        self.openImageButton.setObjectName("openImageButton")
        self.horizontalLayout_4.addWidget(self.openImageButton)
        self.applyButton = QtWidgets.QPushButton(WMask)
        self.applyButton.setObjectName("applyButton")
        self.horizontalLayout_4.addWidget(self.applyButton)
        self.saveMaskButton = QtWidgets.QPushButton(WMask)
        self.saveMaskButton.setObjectName("saveMaskButton")
        self.horizontalLayout_4.addWidget(self.saveMaskButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.clearButton = QtWidgets.QPushButton(WMask)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout_4.addWidget(self.clearButton)
        self.closeButton = QtWidgets.QPushButton(WMask)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_4.addWidget(self.closeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(WMask)
        QtCore.QMetaObject.connectSlotsByName(WMask)

    def retranslateUi(self, WMask):
        _translate = QtCore.QCoreApplication.translate
        WMask.setWindowTitle(_translate("WMask", "Mask"))
        self.checkInvert.setText(_translate("WMask", "Invert ROI"))
        self.lessCheckbox.setText(_translate("WMask", "Less than"))
        self.moreCheckbox.setText(_translate("WMask", "More than"))
        self.polyButton.setText(_translate("WMask", "Polygone"))
        self.ellipseButton.setText(_translate("WMask", "Ellipse"))
        self.buttonCircle.setText(_translate("WMask", "Circle"))
        self.openImageButton.setText(_translate("WMask", "Open"))
        self.applyButton.setText(_translate("WMask", "Apply"))
        self.saveMaskButton.setText(_translate("WMask", "Save"))
        self.clearButton.setText(_translate("WMask", "Clear"))
        self.closeButton.setText(_translate("WMask", "Close"))

from pyqtgraph import ImageView
from . import resources_rc
