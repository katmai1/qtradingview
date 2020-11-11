# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/q/dev/qtradingview/qtradingview/ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(673, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/base/logo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMainWindow::separator{width: 4px}")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks|QtWidgets.QMainWindow.ForceTabbedDocks)
        MainWindow.setProperty("currentExchange", "")
        MainWindow.setProperty("currentMarket", "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webview = QtWebEngineWidgets.QWebEngineView(self.centralwidget)
        self.webview.setObjectName("webview")
        self.horizontalLayout.addWidget(self.webview)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tradingbar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tradingbar.sizePolicy().hasHeightForWidth())
        self.tradingbar.setSizePolicy(sizePolicy)
        self.tradingbar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tradingbar.setOrientation(QtCore.Qt.Horizontal)
        self.tradingbar.setIconSize(QtCore.QSize(24, 24))
        self.tradingbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.tradingbar.setObjectName("tradingbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tradingbar)
        self.appbar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appbar.sizePolicy().hasHeightForWidth())
        self.appbar.setSizePolicy(sizePolicy)
        self.appbar.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.appbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.appbar.setObjectName("appbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.appbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 673, 20))
        self.menuBar.setDefaultUp(False)
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menuBar)
        self.menuView.setObjectName("menuView")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/settings"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon1)
        self.actionSettings.setObjectName("actionSettings")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/actions/exit"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon2)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setIcon(icon)
        self.actionAbout.setObjectName("actionAbout")
        self.actionMarkets = QtWidgets.QAction(MainWindow)
        self.actionMarkets.setCheckable(True)
        self.actionMarkets.setChecked(True)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/actions/markets"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionMarkets.setIcon(icon3)
        self.actionMarkets.setObjectName("actionMarkets")
        self.actionAlarms = QtWidgets.QAction(MainWindow)
        self.actionAlarms.setCheckable(True)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/actions/alarms"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAlarms.setIcon(icon4)
        self.actionAlarms.setObjectName("actionAlarms")
        self.actionFull_Screen = QtWidgets.QAction(MainWindow)
        self.actionFull_Screen.setCheckable(True)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/actions/screen"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionFull_Screen.setIcon(icon5)
        self.actionFull_Screen.setObjectName("actionFull_Screen")
        self.actionDebug = QtWidgets.QAction(MainWindow)
        self.actionDebug.setCheckable(True)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/actions/debug"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDebug.setIcon(icon6)
        self.actionDebug.setObjectName("actionDebug")
        self.actionToolbar = QtWidgets.QAction(MainWindow)
        self.actionToolbar.setCheckable(True)
        self.actionToolbar.setChecked(True)
        self.actionToolbar.setObjectName("actionToolbar")
        self.actionPortfolio = QtWidgets.QAction(MainWindow)
        self.actionPortfolio.setCheckable(True)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/actions/portfolio"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPortfolio.setIcon(icon7)
        self.actionPortfolio.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionPortfolio.setObjectName("actionPortfolio")
        self.tradingbar.addAction(self.actionMarkets)
        self.tradingbar.addAction(self.actionAlarms)
        self.tradingbar.addAction(self.actionPortfolio)
        self.appbar.addAction(self.actionQuit)
        self.appbar.addAction(self.actionSettings)
        self.appbar.addSeparator()
        self.appbar.addAction(self.actionDebug)
        self.appbar.addSeparator()
        self.appbar.addAction(self.actionFull_Screen)
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuView.addAction(self.actionToolbar)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionMarkets)
        self.menuView.addAction(self.actionAlarms)
        self.menuView.addAction(self.actionPortfolio)
        self.menuView.addAction(self.actionDebug)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionFull_Screen)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.actionToolbar.toggled['bool'].connect(self.appbar.setVisible)
        self.actionToolbar.toggled['bool'].connect(self.tradingbar.setVisible)
        self.actionQuit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QTradingview"))
        self.tradingbar.setWindowTitle(_translate("MainWindow", "TradingBar"))
        self.appbar.setWindowTitle(_translate("MainWindow", "AppBar"))
        self.menuFile.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuView.setTitle(_translate("MainWindow", "Vie&w"))
        self.menuHelp.setTitle(_translate("MainWindow", "&Help"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))
        self.actionSettings.setToolTip(_translate("MainWindow", "Open settings window"))
        self.actionSettings.setShortcut(_translate("MainWindow", "F9"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setToolTip(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionMarkets.setText(_translate("MainWindow", "Markets"))
        self.actionMarkets.setToolTip(_translate("MainWindow", "Show/hide markets"))
        self.actionMarkets.setShortcut(_translate("MainWindow", "F1"))
        self.actionAlarms.setText(_translate("MainWindow", "Alarms"))
        self.actionAlarms.setToolTip(_translate("MainWindow", "Show/hide alarms"))
        self.actionAlarms.setShortcut(_translate("MainWindow", "F2"))
        self.actionFull_Screen.setText(_translate("MainWindow", "Full Screen"))
        self.actionFull_Screen.setToolTip(_translate("MainWindow", "Activate/deactivate full screen"))
        self.actionFull_Screen.setShortcut(_translate("MainWindow", "F11"))
        self.actionDebug.setText(_translate("MainWindow", "Debug"))
        self.actionDebug.setToolTip(_translate("MainWindow", "Show/hide debug panel"))
        self.actionToolbar.setText(_translate("MainWindow", "Toolbar"))
        self.actionToolbar.setStatusTip(_translate("MainWindow", "Show/hide toolbar"))
        self.actionToolbar.setShortcut(_translate("MainWindow", "F4"))
        self.actionPortfolio.setText(_translate("MainWindow", "Portfolio"))
        self.actionPortfolio.setShortcut(_translate("MainWindow", "F3"))
from PyQt5 import QtWebEngineWidgets
import iconos_rc
