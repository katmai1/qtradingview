import logging
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMenu, QAction

from .models import Trades


# ─── TRADES MODEL FOR TABLE ─────────────────────────────────────────────────────

class TradesTableModel(QAbstractTableModel):

    def __init__(self, data, headers):
        QAbstractTableModel.__init__(self)
        self._data = data
        self.headers = headers

    @property
    def suma_profit100(self):
        index = self.headers.index('Profit100')
        total = 0.0
        for d in self._data:
            total += d[index]
        return f"{total:.2f}%"

    def data(self, index, role=Qt.DisplayRole):
        """ Insert data  on table """
        col = self.headers[index.column()].lower()
        valor = self._data[index.row()][index.column()]

        if role == Qt.DisplayRole:
            return self.customDisplayRole(col, valor)

        elif role == Qt.ForegroundRole:
            return self.customForegroundRole(col, valor)

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        elif role == Qt.DecorationRole:
            if col == "exchange":
                return QIcon(f":/exchanges/{valor}")

        elif role == Qt.ToolTipRole:
            return self.customTooltipRole(col, valor)

    def customDisplayRole(self, col, valor):
        """ Custom method to display values """
        floats_heads = ["openprice", "closeprice", "amount", "lastprice", "profit"]
        if valor is not None:
            if col == "exchange" or col == "postype":
                return valor.title()
            elif col in floats_heads:
                return f"{valor:.8f}"
            elif col == "profit100":
                return f"{valor:.2f}%"
            elif col == "lastupdate":
                return f"{valor[0]}m {valor[1]}s ago"
        return valor

    def customForegroundRole(self, col, valor):
        """ Custom method to set text color """
        if col == "profit100" or col == "profit":
            if valor > 0:
                return QColor('green')
            elif valor < 0:
                return QColor('red')
        elif col == "lastupdate":
            if valor[0] > 2:
                return QColor('red')
        return

    def customTooltipRole(self, col, valor):
        if col == "id":
            return self.tr("Identifier number of this position")
        elif col == "exchange":
            return self.tr("Exchange where be open position")
        elif col == "market":
            return self.tr("Market of this position")
        return
    
    # ────────────────────────────────────────────────────────────────────────────────

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self.headers)

# ────────────────────────────────────────────────────────────────────────────────


# ─── PORTFOLIO CONTEXT MENU ─────────────────────────────────────────────────────

class CustomContextMenu(QMenu):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mw = self.parent().parent().parent().parent()
        self.dock = self.parent().parent().parent()

    def handler(self, position):
        index = self.parent().indexAt(position)
        self._valor = self.parent().model().data(index)
        self._trade = self._get_trade(position)
        if self._valor is not None and self._trade is not None:
            self._insertActions()
            self.exec_(self.parent().viewport().mapToGlobal(position))

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def _insertActions(self):
        self.addAction(self._action("Close...", self.runActionClose))
        self.addAction(self._action("Edit...", self.runActionEdit))
        self.addAction(self._action("Delete", self.runActionDelete))
        self.addSeparator()
        self.addAction(self._action(f"Copy to clipboard: '{self._valor}'", self.runActionCopyClipboard))

    def _get_trade(self, position):
        try:
            index = self.parent().indexAt(position)
            newindex = self.parent().model().index(index.row(), 0)
            trade_id = self.parent().model().data(newindex)
            return Trades.get_by_id(trade_id)
        except Exception as e:
            logging.warning("Exception trying get item on this position.")
            logging.error(e.__str__())
            return None

    def _action(self, texto, cmd, icono=None, shortcut=None):
        action = QAction(texto, self, triggered=cmd)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icono is not None:
            action.setIcon(QIcon(icono))
        return action

    # ─── ACTIONS ────────────────────────────────────────────────────────────────────

    def runActionClose(self):
        self.dock.closeTrade(self._trade.id)

    def runActionEdit(self):
        self.dock.openDialogEdit(self._trade.id)

    def runActionDelete(self):
        self.dock.deleteTrade(self._trade.id)

    def runActionCopyClipboard(self):
        clip = self.mw.ctx.app.clipboard()
        clip.setText(self._valor)

# ────────────────────────────────────────────────────────────────────────────────
