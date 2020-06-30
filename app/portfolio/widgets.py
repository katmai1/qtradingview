import logging
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QMenu, QAction, QMessageBox

from .models import Trades


# ─── TRADES MODEL FOR TABLE ─────────────────────────────────────────────────────

class TradesTableModel(QAbstractTableModel):
    
    headers = ['ID', 'Exchange', 'Market', 'PosType', 'OpenPrice', 'Amount', 'LastPrice', 'LastUpdate', 'Profit100', 'Profit']
    
    def __init__(self, data):
        super(TradesTableModel, self).__init__()
        self._data = data

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.customDisplayRole(index)
        elif role == Qt.ForegroundRole:
            return self.customForegroundRole(index)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignRight
        elif role == "raw":
            valor = self._data[index.row()][index.column()]
            columna = self.headers[index.column()].lower()
            if type(valor) == float:
                return f"{valor:.8f}"
            if columna == "lastupdate":
                return self.customDisplayRole(index)
            return valor

    # custom show values
    def customDisplayRole(self, index):
        valor = self._data[index.row()][index.column()]
        columna = self.headers[index.column()].lower()
        if valor is not None:
            base_coin, quote_coin = self._data[index.row()][2].split("/")
            if columna == "exchange":
                return valor.title()
            elif columna == "postype":
                return valor.title()
            elif columna == "openprice":
                price = str(float("%.8f" % valor))
                return f"{price} {quote_coin}"
            elif columna == "amount":
                amount = str(float("%.8f" % valor))
                return f"{amount} {base_coin}"
            elif columna == "profit100":
                return "%.2f%%" % valor
            elif columna == "profit":
                profit = str(float("%.8f" % valor))
                return f"{profit} {quote_coin}"
            elif columna == "lastprice":
                price = str(float("%.8f" % valor))
                return f"{valor:.8f} {quote_coin}"
            elif columna == "lastupdate":
                return f"{valor[0]}m {valor[1]}s ago"
        return valor

    # custom color text
    def customForegroundRole(self, index):
        valor = self._data[index.row()][index.column()]
        columna = self.headers[index.column()].lower()
        if columna == "profit100" or columna == "profit":
            if valor > 0:
                return QColor('green')
            elif valor < 0:
                return QColor('red')
        elif columna == "lastupdate":
            if valor[0] > 3:
                return QColor('red')
        return

    # ────────────────────────────────────────────────────────────────────────────────

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

# ────────────────────────────────────────────────────────────────────────────────


# ─── PORTFOLIO CONTEXT MENU ─────────────────────────────────────────────────────

class CustomContextMenu(QMenu):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mw = self.parent().parent().parent().parent()
        self.dock = self.parent().parent().parent()
        
    def handler(self, position):
        index = self.parent().indexAt(position)
        self._valor = self.parent().model().data(index, role="raw")
        self._trade = self._get_trade(position)
        self.addAction(self._action("Edit...", self.runActionEdit))
        self.addAction(self._action("Delete", self.runActionDelete))
        self.addAction(self._action(f"Copy '{self._valor}' to clipboard", self.runActionCopyClipboard))
        self.exec_(self.parent().mapToGlobal(position))
    
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

    def runActionEdit(self):
        self.dock.openDialogEdit(self._trade.id)
    
    def runActionDelete(self):
        self.dock.deleteTrade(self._trade.id)
    
    def runActionCopyClipboard(self):
        clip = self.mw.ctx.app.clipboard()
        clip.setText(self._valor)

# ────────────────────────────────────────────────────────────────────────────────
