from PyQt5 import QtWidgets, QtGui, QtCore
from .ui.dock_markets import Ui_dock_markets
from .db import Markets
from src.tasks.update_markets_db import UpdateMarkets_DB


class DockMarkets(QtWidgets.QDockWidget, Ui_dock_markets):
    
    exchanges = ['binance', 'bitfinex']
    
    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.parent = parent
        self.setupUi(self)
        #
        self._load_exchanges()
        # self.onExchangeChanged()
        self._signals()

    def _signals(self):
        self.combo_exchange.currentTextChanged.connect(self.onExchangeChanged)
        self.list_markets.itemDoubleClicked.connect(self.onDoubleClickMarket)
        self.list_markets.mouseReleaseEvent = self.onClickMarket
        self.list_markets.keyReleaseEvent = self.onKeyRelease
        self.edit_filtro.textEdited.connect(self.onFiltroChanged)

    @property
    def selected_exchange(self):
        return self.combo_exchange.currentText().lower()
    
    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    def onFiltroChanged(self, text):
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            if text.upper() in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def onExchangeChanged(self):
        exchange = self.combo_exchange.currentText().lower()
        self.list_markets.clear()
        lista = Markets.select().where(Markets.exchange == exchange)
        for it in lista:
            self.list_markets.addItem(it.symbol)

    def onActionActualizaMarkets(self):
        t = UpdateMarkets_DB(self)
        t.run()

    def onDoubleClickMarket(self, item):
        self.parent._load_chart(item.text(), self.selected_exchange)
    
    def onClickMarket(self, event):
        if event.button() == 2:
            row = self.list_markets.itemAt(event.pos())
            print(row.text())
        print(event.button())
    
    def onKeyRelease(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            print("espacio")

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def _load_exchanges(self):
        self.combo_exchange.clear()
        for x in self.exchanges:
            path = f"ico/{x}.png"
            self.combo_exchange.addItem(QtGui.QIcon(path), x.title())
        self.onExchangeChanged()
