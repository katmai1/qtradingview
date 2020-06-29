from PyQt5.QtCore import QAbstractTableModel, Qt


# ─── TRADES MODEL FOR TABLE ─────────────────────────────────────────────────────

class TradesTableModel(QAbstractTableModel):
    
    headers = ['ID', 'Exchange', 'Market', 'PosType', 'OpenPrice', 'Amount']
    
    def __init__(self, data):
        super(TradesTableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            valor = self._data[index.row()][index.column()]
            if index.column() == 1:
                return valor.title()
            elif index.column() == 4:
                return "%.8f" % valor
            elif index.column() == 5:
                return "%.8f" % valor
            return valor

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)
        # if role == Qt.DisplayRole and orientation == Qt.Vertical:
        #     return self._data[section][0]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

# ────────────────────────────────────────────────────────────────────────────────
