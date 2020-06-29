from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QColor


# ─── TRADES MODEL FOR TABLE ─────────────────────────────────────────────────────

class TradesTableModel(QAbstractTableModel):
    
    headers = ['ID', 'Exchange', 'Market', 'PosType', 'OpenPrice', 'Amount', 'LastPrice', 'LastUpdate', 'Profit100', 'Profit']
    
    def __init__(self, data):
        super(TradesTableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self.customDisplayRole(index)
        elif role == Qt.ForegroundRole:
            return self.customForegroundRole(index)
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignVCenter + Qt.AlignRight

    # custom show values
    def customDisplayRole(self, index):
        valor = self._data[index.row()][index.column()]
        columna = self.headers[index.column()].lower()
        if valor is not None:
            if columna == "exchange":
                return valor.title()
            elif columna == "postype":
                return valor.title()
            elif columna == "openprice":
                quote_coin = self._data[index.row()][2].split("/")[1]
                price = str(float("%.8f" % valor))
                return f"{price} {quote_coin}"
            elif columna == "amount":
                base_coin = self._data[index.row()][2].split("/")[0]
                amount = str(float("%.8f" % valor))
                return f"{amount} {base_coin}"
            elif columna == "profit100":
                return "%.2f%%" % valor
            elif columna == "profit":
                quote_coin = self._data[index.row()][2].split("/")[1]
                profit = str(float("%.8f" % valor))
                return f"{profit} {quote_coin}"
            elif columna == "lastprice":
                quote_coin = self._data[index.row()][2].split("/")[1]
                price = str(float("%.8f" % valor))
                return f"{price} {quote_coin}"
            elif columna == "lastupdate":
                return f"{int(valor)} Minutes ago"
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
            if valor > 2:
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
