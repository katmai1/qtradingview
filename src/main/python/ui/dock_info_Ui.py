# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dock_info.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dock_info(object):
    def setupUi(self, dock_info):
        dock_info.setObjectName("dock_info")
        dock_info.resize(248, 587)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_exchange = QtWidgets.QLabel(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_exchange.setFont(font)
        self.label_exchange.setAlignment(QtCore.Qt.AlignCenter)
        self.label_exchange.setObjectName("label_exchange")
        self.verticalLayout.addWidget(self.label_exchange)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        dock_info.setWidget(self.dockWidgetContents)

        self.retranslateUi(dock_info)
        QtCore.QMetaObject.connectSlotsByName(dock_info)

    def retranslateUi(self, dock_info):
        _translate = QtCore.QCoreApplication.translate
        dock_info.setWindowTitle(_translate("dock_info", "DockWidget"))
        self.label_exchange.setText(_translate("dock_info", "Exchange"))

