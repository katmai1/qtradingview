# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dock_markets.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dock_markets(object):
    def setupUi(self, dock_markets):
        dock_markets.setObjectName("dock_markets")
        dock_markets.resize(302, 532)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dock_markets.sizePolicy().hasHeightForWidth())
        dock_markets.setSizePolicy(sizePolicy)
        dock_markets.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        dock_markets.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.combo_exchange = QtWidgets.QComboBox(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.combo_exchange.setFont(font)
        self.combo_exchange.setIconSize(QtCore.QSize(32, 32))
        self.combo_exchange.setObjectName("combo_exchange")
        self.verticalLayout.addWidget(self.combo_exchange)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.btn_favorite = QtWidgets.QPushButton(self.dockWidgetContents)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/base/star.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_favorite.setIcon(icon)
        self.btn_favorite.setIconSize(QtCore.QSize(24, 24))
        self.btn_favorite.setCheckable(True)
        self.btn_favorite.setChecked(False)
        self.btn_favorite.setDefault(False)
        self.btn_favorite.setFlat(False)
        self.btn_favorite.setObjectName("btn_favorite")
        self.verticalLayout.addWidget(self.btn_favorite)
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem1)
        self.edit_filtro = QtWidgets.QLineEdit(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.edit_filtro.setFont(font)
        self.edit_filtro.setAcceptDrops(False)
        self.edit_filtro.setInputMethodHints(QtCore.Qt.ImhUppercaseOnly)
        self.edit_filtro.setText("")
        self.edit_filtro.setFrame(True)
        self.edit_filtro.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.edit_filtro.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.edit_filtro.setClearButtonEnabled(True)
        self.edit_filtro.setObjectName("edit_filtro")
        self.verticalLayout.addWidget(self.edit_filtro)
        self.list_markets = QtWidgets.QListWidget(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.list_markets.setFont(font)
        self.list_markets.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.list_markets.setAutoScrollMargin(20)
        self.list_markets.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.list_markets.setTabKeyNavigation(False)
        self.list_markets.setProperty("showDropIndicator", False)
        self.list_markets.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.list_markets.setAlternatingRowColors(True)
        self.list_markets.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.list_markets.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.list_markets.setSelectionRectVisible(False)
        self.list_markets.setObjectName("list_markets")
        self.verticalLayout.addWidget(self.list_markets)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem2)
        dock_markets.setWidget(self.dockWidgetContents)

        self.retranslateUi(dock_markets)
        QtCore.QMetaObject.connectSlotsByName(dock_markets)
        dock_markets.setTabOrder(self.combo_exchange, self.edit_filtro)
        dock_markets.setTabOrder(self.edit_filtro, self.list_markets)

    def retranslateUi(self, dock_markets):
        _translate = QtCore.QCoreApplication.translate
        dock_markets.setWindowTitle(_translate("dock_markets", "&Mercados"))
        self.btn_favorite.setStatusTip(_translate("dock_markets", "Filtrar mercados marcados como favoritos"))
        self.btn_favorite.setText(_translate("dock_markets", "Mostrar solo favoritos"))
        self.edit_filtro.setStatusTip(_translate("dock_markets", "Filtrar mercados por nombre"))
        self.edit_filtro.setPlaceholderText(_translate("dock_markets", "Filtro"))
        self.list_markets.setSortingEnabled(True)
import iconos_rc
