# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(650, 480)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(600, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../ico/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        self.webview.setUrl(QtCore.QUrl("https://es.tradingview.com/chart/"))
        self.webview.setObjectName("webview")
        self.horizontalLayout.addWidget(self.webview)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dock_markets = QtWidgets.QDockWidget(MainWindow)
        self.dock_markets.setObjectName("dock_markets")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.combo_exchange = QtWidgets.QComboBox(self.dockWidgetContents)
        self.combo_exchange.setObjectName("combo_exchange")
        self.verticalLayout.addWidget(self.combo_exchange)
        self.list_markets = QtWidgets.QListWidget(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.list_markets.setFont(font)
        self.list_markets.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_markets.setObjectName("list_markets")
        self.verticalLayout.addWidget(self.list_markets)
        self.dock_markets.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dock_markets)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 650, 20))
        self.menuBar.setObjectName("menuBar")
        self.menuVer = QtWidgets.QMenu(self.menuBar)
        self.menuVer.setObjectName("menuVer")
        self.menuArchivo = QtWidgets.QMenu(self.menuBar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuOpciones = QtWidgets.QMenu(self.menuBar)
        self.menuOpciones.setObjectName("menuOpciones")
        MainWindow.setMenuBar(self.menuBar)
        self.actionMarkets_list = QtWidgets.QAction(MainWindow)
        self.actionMarkets_list.setCheckable(True)
        self.actionMarkets_list.setChecked(True)
        self.actionMarkets_list.setObjectName("actionMarkets_list")
        self.actionSalir = QtWidgets.QAction(MainWindow)
        self.actionSalir.setObjectName("actionSalir")
        self.actionPantalla_completa = QtWidgets.QAction(MainWindow)
        self.actionPantalla_completa.setCheckable(True)
        self.actionPantalla_completa.setObjectName("actionPantalla_completa")
        self.actionVentana_Normal = QtWidgets.QAction(MainWindow)
        self.actionVentana_Normal.setObjectName("actionVentana_Normal")
        self.actionActualizar_markets = QtWidgets.QAction(MainWindow)
        self.actionActualizar_markets.setObjectName("actionActualizar_markets")
        self.menuVer.addAction(self.actionMarkets_list)
        self.menuVer.addSeparator()
        self.menuVer.addAction(self.actionPantalla_completa)
        self.menuVer.addAction(self.actionVentana_Normal)
        self.menuArchivo.addAction(self.actionSalir)
        self.menuOpciones.addAction(self.actionActualizar_markets)
        self.menuBar.addAction(self.menuArchivo.menuAction())
        self.menuBar.addAction(self.menuVer.menuAction())
        self.menuBar.addAction(self.menuOpciones.menuAction())

        self.retranslateUi(MainWindow)
        self.actionMarkets_list.toggled['bool'].connect(self.dock_markets.setVisible)
        self.actionSalir.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QTradingview"))
        self.dock_markets.setWindowTitle(_translate("MainWindow", "Markets List"))
        self.list_markets.setSortingEnabled(True)
        self.menuVer.setTitle(_translate("MainWindow", "Ver"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuOpciones.setTitle(_translate("MainWindow", "Herramientas"))
        self.actionMarkets_list.setText(_translate("MainWindow", "Markets list"))
        self.actionMarkets_list.setShortcut(_translate("MainWindow", "F1"))
        self.actionSalir.setText(_translate("MainWindow", "Salir"))
        self.actionSalir.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionPantalla_completa.setText(_translate("MainWindow", "Pantalla completa"))
        self.actionPantalla_completa.setShortcut(_translate("MainWindow", "F11"))
        self.actionVentana_Normal.setText(_translate("MainWindow", "Ventana Normal"))
        self.actionActualizar_markets.setText(_translate("MainWindow", "Actualizar markets"))

from PyQt5 import QtWebEngineWidgets
