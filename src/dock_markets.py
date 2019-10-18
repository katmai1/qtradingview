from PyQt5 import QtWidgets, QtGui, QtCore
from .ui.dock_markets import Ui_dock_markets
from .db import Markets
from src.tasks.update_markets_db import UpdateMarkets_DB
import logging

class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        option.decorationPosition = QtWidgets.QStyleOptionViewItem.Right
        super(ItemDelegate, self).paint(painter, option, index)


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
        self.delegate = ItemDelegate()
        self.list_markets.setItemDelegate(self.delegate)

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
        self.edit_filtro.clear()
        self.list_markets.clear()
        for it in Markets.get_all_by_exchange(self.selected_exchange):
            self.list_markets.addItem(it.symbol)
        for index in range(self.list_markets.count()):
            item = self.list_markets.item(index)
            item.setIcon(self._get_icon_by_symbol(item.text()))
                

    def onActionActualizaMarkets(self):
        t = UpdateMarkets_DB(self)
        t.run()

    def onDoubleClickMarket(self, item):
        self.parent._load_chart(item.text(), self.selected_exchange)
        logging.info("test logging")
    
    def onClickMarket(self, event):
        if event.button() == 2:
            item = self.list_markets.itemAt(event.pos())
            dbitem = Markets.get_symbol_by_exchange(item.text(), self.selected_exchange)
            dbitem.toggle_fav()
            item.setIcon(self._get_icon_by_symbol(item.text()))
    
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

    def _get_icon_by_symbol(self, symbol):
        item = Markets.get_symbol_by_exchange(symbol, self.selected_exchange)
        if item.favorite:
            return QtGui.QIcon("ico/star.svg")
        return QtGui.QIcon("ico/voidstar.svg")
