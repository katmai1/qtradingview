import logging
from PyQt5 import QtWidgets, QtGui, QtCore

from qtradingview.markets.widgets import CustomItem, CustomItemDelegate, CustomContextMenu
from qtradingview.markets.updater import UpdateAllMarkets

from qtradingview.models.markets import Markets
from qtradingview.ui.Ui_dock_markets import Ui_dock_markets


# ─── DOCK MARKETS ───────────────────────────────────────────────────────────────

class DockMarkets(QtWidgets.QDockWidget, Ui_dock_markets):

    # statusbar_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowTitle("Markets")
        self.mw = self.parent()  # mainwindow
        self.setVisible(self.mw.actionMarkets.isChecked())
        # base
        self.markets_updater = UpdateAllMarkets(self)
        self.lista_mode = self.mw.cfg.value("markets/list_mode", defaultValue="all")
        self._load_exchanges()
        self._signals()
        # list markets
        self.delegate = CustomItemDelegate()
        self.list_markets.setItemDelegate(self.delegate)
        self.list_markets.customContextMenuRequested.connect(self.contextMenuEvent)
        # markets updater
        self.loadListMode(self.lista_mode)
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
    
    def closeEvent(self, event):
        self.mw.actionMarkets.setChecked(False)
        self.setVisible(False)
        
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

    def onActionEvent(self, actived):
        """ Show/hide this dock and raise if actived """
        self.setVisible(actived)
        if actived:
            self.raise_()

    def onMarketsUpdaterFinished(self):
        if self.list_markets.count() == 0:
            r = QtWidgets.QMessageBox.information(self, "debes reiniciar", "reiniciaaaa")
            if r:
                self.mw.ctx.app.quit()
        #
        m = Markets.get_symbol_by_exchange("BTC/USDT", "binance")
        self.mw.static_price.setText(f"{m.last_price: .8} BTC/USDT ")
        QtCore.QTimer.singleShot(30 * 1000, self.markets_updater.start)
        self.mw.dock_portfolio.refreshTable()

    # gestiona los shortcuts del dock
    def keyPressEvent(self, event):
        # f5 actualiza markets
        if event.key() == QtCore.Qt.Key_F5:
            self.markets_updater.start()
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

    # ─── LIST MODE ──────────────────────────────────────────────────────────────────

    def loadListMode(self, mode):
        if mode == "fav":
            self.btn_favorite.setChecked(True)
            self.onClickFavoriteButton(True)
        elif mode == "margin":
            self.btn_margin.setChecked(True)
            self.onClickMarginButton(True)
        else:
            self.btn_all.setChecked(True)
            self.onClickAllButton(True)

    def onClickAllButton(self, actived):
        self.lista_mode = "all"
        filtro = self.edit_filtro.text()
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, filtro)

    def onClickFavoriteButton(self, actived):
        self.lista_mode = "fav"
        filtro = self.edit_filtro.text()
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, filtro)

    def onClickMarginButton(self, actived):
        self.lista_mode = "margin"
        filtro = self.edit_filtro.text()
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, filtro)

    # ────────────────────────────────────────────────────────────────────────────────

    # filtro de texto
    def onFiltroChanged(self, text):
        """ On write/modify filter field """
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.mostrar(self.lista_mode, text)

    def onExchangeChanged(self):
        """ When exchange combo is changed """
        self.edit_filtro.clear()
        self._load_markets()

    def onDoubleClickMarket(self, item):
        """ When double click over market """
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
        for x in self.mw.cfg.value('settings/exchanges'):
            path = f":/exchanges/{x.lower()}"
            self.combo_exchange.addItem(QtGui.QIcon(path), x.title())
        default_index = self.combo_exchange.findText(self.mw.cfg.value('settings/initial_exchange').title())
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
