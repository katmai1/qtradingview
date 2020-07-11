import logging
from PyQt5 import QtWidgets, QtGui, QtCore

from app.markets.widgets import CustomItem, CustomItemDelegate, CustomContextMenu
from app.markets.updater import UpdateMarkets, UpdateAllMarkets

from app.models.markets import Markets
from app.ui.dock_markets_Ui import Ui_dock_markets


# ─── DOCK MARKETS ───────────────────────────────────────────────────────────────

class DockMarkets(QtWidgets.QDockWidget, Ui_dock_markets):

    # statusbar_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Markets")
        #
        self.mw = self.parent()  # mainwindow
        self.setVisible(self.mw.actionMarkets.isChecked())
                
        self.markets_updater = UpdateAllMarkets(self)
        self.lista_mode = "all"
        self._load_exchanges()
        self._signals()
        #
        self.delegate = CustomItemDelegate()
        self.list_markets.setItemDelegate(self.delegate)
        self.list_markets.customContextMenuRequested.connect(self.contextMenuEvent)
        self.onClickAllButton(True)
        self.markets_updater.start()

    def _signals(self):
        self.combo_exchange.currentTextChanged.connect(self.onExchangeChanged)
        self.list_markets.itemDoubleClicked.connect(self.onDoubleClickMarket)
        self.edit_filtro.textEdited.connect(self.onFiltroChanged)
        self.btn_all.toggled.connect(self.onClickAllButton)
        self.btn_favorite.toggled.connect(self.onClickFavoriteButton)
        self.btn_margin.toggled.connect(self.onClickMarginButton)
        self.btn_update.clicked.connect(self.markets_updater.start)
        self.markets_updater.infoEvent.connect(self.onEventUpdater)
        self.markets_updater.onFinished.connect(self.onMarketsUpdaterFinished)

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

    def onMarketsUpdaterFinished(self):
        if self.list_markets.count() == 0:
            self._load_markets
        QtCore.QTimer.singleShot(120 * 1000, self.markets_updater.start)
        self.mw.dock_portfolio.refreshTable()

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

    def onEventUpdater(self, texto):
        logging.debug(texto)
        self.mw.set_text_status(texto)

    # actualiza markets del exchange seleccionado en la db
    def start_update_market(self):
        self.mw.set_text_status(f'Updating markets from {self.selected_exchange.title()}...')
        QtCore.QCoreApplication.processEvents()
        self.updater = UpdateMarkets(self.selected_exchange)
        self.updater.onFinished.connect(self.onExchangeChanged)
        self.updater.run()

    # filtro al
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
        self.combo_exchange.blockSignals(True)
        self.combo_exchange.clear()
        for x in self.mw.config['exchanges']:
            path = f":/exchanges/{x.lower()}"
            self.combo_exchange.addItem(QtGui.QIcon(path), x.title())
        default_index = self.combo_exchange.findText(self.mw.config['initial_exchange'].title())
        if default_index != -1:
            self.combo_exchange.setCurrentIndex(default_index)
        self.combo_exchange.blockSignals(False)
        self.onExchangeChanged()

    # carga lista de markets
    def _load_markets(self):
        self.combo_exchange.setDisabled(True)
        filtro = self.edit_filtro.text()
        self.list_markets.clear()
        for i, item in enumerate(Markets.get_all_by_exchange(self.selected_exchange)):
            if i % 20 == 0:
                QtCore.QCoreApplication.processEvents()
            nuevo = CustomItem(self.list_markets)
            nuevo.configurar(item.symbol, self.selected_exchange)
            nuevo.mostrar(self.lista_mode, filtro)
        self.combo_exchange.setEnabled(True)
