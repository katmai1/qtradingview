from PyQt5 import QtWidgets, QtGui, QtCore

from app.ui.dock_portfolio_Ui import Ui_DockPortfolio
from .dialog import DialogTrade
from .models import Trades
from .widgets import TradesTableModel


# ─── DOCK PORTFOLIO ─────────────────────────────────────────────────────────────

class DockPortfolio(QtWidgets.QDockWidget, Ui_DockPortfolio):
    
    def __init__(self, parent=None):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.mw = parent
        self.setVisible(self.mw.actionPortfolio.isChecked())
        #
        self._signals()
        self.refreshTable()

    def getSelectedTrade(self):
        row = self.tabla.currentIndex().row()
        trade_id = self.model._data[row][0]
        return Trades.get_by_id(trade_id)

    def setVisible(self, visible):
        super().setVisible(visible)
        if visible:
            self.raise_()

    def _signals(self):
        self.btn_edit.clicked.connect(self.onButtonEdit)
        self.btn_delete.clicked.connect(self.onButtonDelete)
        self.btn_update.clicked.connect(self.refreshTable)

    def addPortfolio(self, exchange, market):
        d = DialogTrade(self)
        d.loadNewTradeData(exchange, market)
        if d.exec_():
            d.createTrade()
            self.refreshTable()

    def onButtonEdit(self):
        row = self.tabla.currentIndex().row()
        trade_id = self.model._data[row][0]
        d = DialogTrade(self)
        d.loadEditTradeData(trade_id)
        if d.exec_():
            d.updateTrade()
            self.refreshTable()

    def onButtonDelete(self):
        t = self.getSelectedTrade()
        t.delete_instance()
        t.save()
        self.refreshTable()

    def onButtonUpdate(self):
        self.mw.dock_markets.markets_updater.start()

    def refreshTable(self):
        data = []
        for trade in Trades.get_all():
            data.append([
                trade.id, trade.market.exchange, trade.market.symbol, trade.position,
                trade.open_price, trade.amount, trade.market.last_price, trade.market.since_update(),
                trade.profit100(), trade.profit()
            ])
        if len(data) > 0:
            self.model = TradesTableModel(data)
            self.tabla.setModel(self.model)
            self.tabla.resizeColumnsToContents()

# ────────────────────────────────────────────────────────────────────────────────
