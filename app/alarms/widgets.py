from PyQt5.QtCore import QAbstractTableModel, Qt


# ─── ALARMS TABLE MODEL ─────────────────────────────────────────────────────────

class AlarmsTableModel(QAbstractTableModel):
    
    def __init__(self, data, headers):
        QAbstractTableModel.__init__(self)
        self._data = data
        self.headers = headers

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            valor = self._data[index.row()][index.column()]
            return valor

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self.headers)
# ────────────────────────────────────────────────────────────────────────────────
