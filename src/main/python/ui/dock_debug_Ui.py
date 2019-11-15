# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dock_debug.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DockDebug(object):
    def setupUi(self, DockDebug):
        DockDebug.setObjectName("DockDebug")
        DockDebug.resize(400, 300)
        DockDebug.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        DockDebug.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.edit_logger = QtWidgets.QTextBrowser(self.dockWidgetContents)
        self.edit_logger.setStyleSheet("background-color: rgb(222, 222, 222);")
        self.edit_logger.setAutoFormatting(QtWidgets.QTextEdit.AutoAll)
        self.edit_logger.setAcceptRichText(False)
        self.edit_logger.setObjectName("edit_logger")
        self.verticalLayout.addWidget(self.edit_logger)
        self.btn_clear = QtWidgets.QPushButton(self.dockWidgetContents)
        self.btn_clear.setAutoDefault(True)
        self.btn_clear.setObjectName("btn_clear")
        self.verticalLayout.addWidget(self.btn_clear)
        DockDebug.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockDebug)
        self.btn_clear.released.connect(self.edit_logger.clear)
        QtCore.QMetaObject.connectSlotsByName(DockDebug)

    def retranslateUi(self, DockDebug):
        _translate = QtCore.QCoreApplication.translate
        DockDebug.setWindowTitle(_translate("DockDebug", "Dep&urar"))
        self.btn_clear.setText(_translate("DockDebug", "Limpiar"))
