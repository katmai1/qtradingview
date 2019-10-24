# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dock_debug.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockDebug(object):
    def setupUi(self, DockDebug):
        DockDebug.setObjectName("DockDebug")
        DockDebug.resize(400, 300)
        DockDebug.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dockWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.edit_logger = QtWidgets.QTextBrowser(self.dockWidgetContents)
        self.edit_logger.setStyleSheet("background-color: rgb(222, 222, 222);")
        self.edit_logger.setObjectName("edit_logger")
        self.horizontalLayout.addWidget(self.edit_logger)
        DockDebug.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockDebug)
        QtCore.QMetaObject.connectSlotsByName(DockDebug)

    def retranslateUi(self, DockDebug):
        _translate = QtCore.QCoreApplication.translate
        DockDebug.setWindowTitle(_translate("DockDebug", "Debug (F10)"))
        self.edit_logger.setHtml(_translate("DockDebug", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; font-weight:600; text-decoration: underline;\">QTradingView</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

