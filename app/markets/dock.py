import logging
import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic

from app.markets.widgets import CustomItem, CustomItemDelegate, CustomContextMenu
from app.markets.updater import UpdateMarkets

from app.models.markets import Markets
from app.utils import resource_path


# ─── DOCK MARKETS ───────────────────────────────────────────────────────────────

class DockMarkets(QtWidgets.QDockWidget):

    ui_filename = os.path.join("ui", "dock_markets.ui")

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        uic.loadUi(resource_path(self.ui_filename), self)
        #
        self.mw = self.parent()  # mainwindow
        self.setVisible(self.mw.actionMarkets.isChecked())
        #
        self.lista_mode = "all"
        self.updater = UpdateMarkets()
        self._load_exchanges()
        self._signals()
        #
        self.delegate = CustomItemDelegate()
        self.list_markets.setItemDelegate(self.delegate)
        self.list_markets.customContextMenuRequested.connect(self.contextMenuEvent)
        self.onClickAllButton(True)

    def _signals(self):
        self.combo_exchange.currentTextChanged.connect(self.onExchangeChanged)
        self.list_markets.itemDoubleClicked.connect(self.onDoubleClickMarket)
        self.edit_filtro.textEdited.connect(self.onFiltroChanged)
        self.btn_all.toggled.connect(self.onClickAllButton)
        self.btn_favorite.toggled.connect(self.onClickFavoriteButton)
        self.btn_margin.toggled.connect(self.onClickMarginButton)
        self.btn_update.clicked.connect(self.start_update_market)

    @property
    def selected_exchange(self):
        return self.combo_exchange.currentText().lower()

    @property
    def fav_is_checked(self):
        return self.btn_favorite.isChecked()

    def setVisible(self, visible):
        super().setVisible(visible)
        if visible:
            self.raise_()

    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    # gestiona los shortcuts del dock
    def keyPressEvent(self, event):
        # f5 actualiza markets
        if event.key() == QtCore.Qt.Key_F5:
            self.start_update_market()
        # si el foco esta en la lista de markets...
        if self.list_markets.hasFocus():
            item = self.list_markets.currentItem()
            # escape favorite toggle
            if event.key() == QtCore.Qt.Key_Escape:
                item.toggle_favorite()
            # return load selected market
            elif event.key() == QtCore.Qt.Key_Return:
                self.parent().load_chart(item.symbol, item.exchange)
        else:
            logging.debug(event.key())

    # actualiza markets en la db
    def start_update_market(self):
        self.mw.statusbar.showMessage('Updating markets...', 2000)
        self.updater.update_markets(self.selected_exchange)
        self.onExchangeChanged()

    # filtro all
    def onClickAllButton(self, all_actived):
        self.lista_mode = "all"
        filtro = self.edit_filtro.text()
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, filtro)

    # filtro favorite
    def onClickFavoriteButton(self, fav_actived):
        self.lista_mode = "fav"
        filtro = self.edit_filtro.text()
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, filtro)

    # filtro margin
    def onClickMarginButton(self, margin_actived):
        self.lista_mode = "margin"
        filtro = self.edit_filtro.text()
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, filtro)

    # filtro de texto
    def onFiltroChanged(self, text):
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, text)

    def onExchangeChanged(self):
        self.edit_filtro.clear()
        self._load_markets()

    def onDoubleClickMarket(self, item):
        self.mw.load_chart(item.text(), self.selected_exchange)

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def contextMenuEvent(self, position):
        contextMenu = CustomContextMenu(self.list_markets)
        if "QPoint" in str(position):
            contextMenu.handler(position)

    # carga lista de exchanges en el combo
    def _load_exchanges(self):
        self.combo_exchange.clear()
        for x in self.mw.config['exchanges']:
            path = f":/exchanges/{x.lower()}"
            self.combo_exchange.addItem(QtGui.QIcon(path), x.title())
        # initial config
        default_index = self.combo_exchange.findText(self.mw.config['initial_exchange'].title())
        if default_index != -1:
            self.combo_exchange.setCurrentIndex(default_index)
        # load markets
        self.onExchangeChanged()

    # carga lista de markets
    def _load_markets(self):
        filtro = self.edit_filtro.text()
        self.list_markets.clear()
        for it in Markets.get_all_by_exchange(self.selected_exchange):
            nuevo = CustomItem(self.list_markets)
            nuevo.configurar(it.symbol, self.selected_exchange)
            nuevo.mostrar(self.lista_mode, filtro)

    # ─── PUBLIC METHODS ─────────────────────────────────────────────────────────────

    def clear_currentInfo(self):
        self.label_currentMarket.setText(" ")
        self.label_currentExchange.setPixmap(QtGui.QPixmap())

    def set_currentInfo(self, exchange, market):
        pixmap = QtGui.QPixmap(f":/exchanges/{exchange}").scaledToWidth(100)
        self.label_currentMarket.setText(market)
        self.label_currentExchange.setPixmap(pixmap)

# ────────────────────────────────────────────────────────────────────────────────
