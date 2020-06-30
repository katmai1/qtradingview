from PyQt5 import QtWidgets, QtGui, QtCore

from app.ui.dock_portfolio_Ui import Ui_DockPortfolio
from .dialog import DialogTrade
from .models import Trades
from .widgets import TradesTableModel, CustomContextMenu


# ─── DOCK PORTFOLIO ─────────────────────────────────────────────────────────────

class DockPortfolio(QtWidgets.QDockWidget, Ui_DockPortfolio):

    def __init__(self, parent=None):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.mw = parent
        self.setWindowTitle("Portfolio")
        #
        self.refresh_timer = QtCore.QTimer(self)
        self.refresh_timer.setInterval(10000)
        self._signals()
        self.setVisible(self.mw.actionPortfolio.isChecked())

    def setVisible(self, active):
        """Show/hide this dock and start/stop refreshing table timer"""
        self.refresh_timer.start() if active else self.refresh_timer.stop()
        return super().setVisible(active)

    def _signals(self):
        self.tabla.customContextMenuRequested.connect(self.contextMenuEvent)
        self.refresh_timer.timeout.connect(self.refreshTable)
        self.combo_trades.currentTextChanged.connect(self.refreshTable)

    def addPortfolio(self, exchange, market):
        """Create new trade in portfolio"""
        d = DialogTrade(self)
        d.loadNewTradeData(exchange, market)
        if d.exec_():
            d.createTrade()
            self.refreshTable()

    def contextMenuEvent(self, position):
        """Load contextual menu"""
        contextMenu = CustomContextMenu(self.tabla)
        index = self.tabla.indexAt(position)
        if index.isValid():
            contextMenu.handler(position)

    def openDialogEdit(self, trade_id):
        """Edit trade from trade_id"""
        d = DialogTrade(self)
        d.loadEditTradeData(trade_id)
        if d.exec_():
            d.updateTrade()
            self.refreshTable()

    def deleteTrade(self, trade_id):
        """Delete trade from trade_id"""
        result = QtWidgets.QMessageBox.question(
            self, f"Trade {trade_id}", self.tr("Do you want delete this trade?"),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            Trades.delete_by_id(trade_id)
            self.refreshTable()

    def closeTrade(self, trade_id):
        trade = Trades.get_by_id(trade_id)
        close_price, okPressed = QtWidgets.QInputDialog.getDouble(
            self, f"Trade {trade_id}", self.tr("Input close price:"),
            decimals=8, value=trade.market.last_price)
        if okPressed:
            trade.close_price = close_price
            trade.save()
        self.refreshTable()

    def refreshTable(self):
        """Add data from database"""
        selected = self.combo_trades.currentText().lower()
        if selected == "open":
            data, headers = Trades.getOpenTradesDataAndHeader()
        elif selected == "closed":
            data, headers = Trades.getClosedTradesDataAndHeader()
        else:
            data = []
        if len(data) > 0:
            self.model = TradesTableModel(data, headers)
            self.tabla.setModel(self.model)
            self.resizeTableColumns()

    def resizeTableColumns(self):
        """Custom resize columns method"""
        self.tabla.resizeColumnsToContents()
        for col, header in enumerate(self.model.headers):
            new_size = self.tabla.columnWidth(col) + 15
            self.tabla.setColumnWidth(col, new_size)

# ────────────────────────────────────────────────────────────────────────────────
