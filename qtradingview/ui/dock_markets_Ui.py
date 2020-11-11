# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/dock_markets.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dock_markets(object):
    def setupUi(self, dock_markets):
        dock_markets.setObjectName("dock_markets")
        dock_markets.resize(281, 581)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dock_markets.sizePolicy().hasHeightForWidth())
        dock_markets.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/actions/markets"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dock_markets.setWindowIcon(icon)
        dock_markets.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        dock_markets.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        dock_markets.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.combo_exchange = QtWidgets.QComboBox(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.combo_exchange.setFont(font)
        self.combo_exchange.setIconSize(QtCore.QSize(32, 32))
        self.combo_exchange.setObjectName("combo_exchange")
        self.horizontalLayout_2.addWidget(self.combo_exchange)
        self.btn_update = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_update.sizePolicy().hasHeightForWidth())
        self.btn_update.setSizePolicy(sizePolicy)
        self.btn_update.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.btn_update.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/actions/update"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_update.setIcon(icon1)
        self.btn_update.setIconSize(QtCore.QSize(32, 32))
        self.btn_update.setObjectName("btn_update")
        self.horizontalLayout_2.addWidget(self.btn_update)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_all = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_all.sizePolicy().hasHeightForWidth())
        self.btn_all.setSizePolicy(sizePolicy)
        self.btn_all.setMinimumSize(QtCore.QSize(0, 35))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btn_all.setFont(font)
        self.btn_all.setAutoFillBackground(True)
        self.btn_all.setIconSize(QtCore.QSize(24, 24))
        self.btn_all.setCheckable(True)
        self.btn_all.setChecked(False)
        self.btn_all.setAutoExclusive(True)
        self.btn_all.setFlat(False)
        self.btn_all.setObjectName("btn_all")
        self.horizontalLayout.addWidget(self.btn_all)
        self.btn_favorite = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_favorite.sizePolicy().hasHeightForWidth())
        self.btn_favorite.setSizePolicy(sizePolicy)
        self.btn_favorite.setMinimumSize(QtCore.QSize(0, 35))
        self.btn_favorite.setAutoFillBackground(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/base/star"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_favorite.setIcon(icon2)
        self.btn_favorite.setIconSize(QtCore.QSize(24, 24))
        self.btn_favorite.setCheckable(True)
        self.btn_favorite.setChecked(False)
        self.btn_favorite.setAutoExclusive(True)
        self.btn_favorite.setDefault(False)
        self.btn_favorite.setFlat(False)
        self.btn_favorite.setObjectName("btn_favorite")
        self.horizontalLayout.addWidget(self.btn_favorite)
        self.btn_margin = QtWidgets.QPushButton(self.dockWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_margin.sizePolicy().hasHeightForWidth())
        self.btn_margin.setSizePolicy(sizePolicy)
        self.btn_margin.setMinimumSize(QtCore.QSize(0, 35))
        self.btn_margin.setAutoFillBackground(True)
        self.btn_margin.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/base/margin"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_margin.setIcon(icon3)
        self.btn_margin.setIconSize(QtCore.QSize(24, 24))
        self.btn_margin.setCheckable(True)
        self.btn_margin.setChecked(False)
        self.btn_margin.setAutoExclusive(True)
        self.btn_margin.setFlat(False)
        self.btn_margin.setObjectName("btn_margin")
        self.horizontalLayout.addWidget(self.btn_margin)
        self.verticalLayout.addLayout(self.horizontalLayout)
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
        dock_markets.setTabOrder(self.edit_filtro, self.list_markets)

    def retranslateUi(self, dock_markets):
        _translate = QtCore.QCoreApplication.translate
        self.combo_exchange.setToolTip(_translate("dock_markets", "Select an exchange"))
        self.btn_update.setToolTip(_translate("dock_markets", "Update markets on db (F5)"))
        self.btn_update.setShortcut(_translate("dock_markets", "F5"))
        self.btn_all.setToolTip(_translate("dock_markets", "Show all markets in list"))
        self.btn_all.setText(_translate("dock_markets", "ALL"))
        self.btn_all.setShortcut(_translate("dock_markets", "Ctrl+A"))
        self.btn_favorite.setToolTip(_translate("dock_markets", "Show only favorite markets"))
        self.btn_favorite.setShortcut(_translate("dock_markets", "Ctrl+F"))
        self.btn_margin.setToolTip(_translate("dock_markets", "Show only margin markets"))
        self.btn_margin.setShortcut(_translate("dock_markets", "Ctrl+M"))
        self.edit_filtro.setToolTip(_translate("dock_markets", "Filter markets by symbol"))
        self.edit_filtro.setPlaceholderText(_translate("dock_markets", "Filter"))
        self.list_markets.setSortingEnabled(True)
import iconos_rc
