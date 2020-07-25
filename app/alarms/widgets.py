import logging
from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QMenu, QAction

from .models import Alarms


# ─── ALARMS TABLE MODEL ─────────────────────────────────────────────────────────

class AlarmsTableModel(QAbstractTableModel):

    def __init__(self, data, headers):
        QAbstractTableModel.__init__(self)
        self._data = data
        self.headers = headers

    def data(self, index, role=Qt.DisplayRole):
        valor = self._data[index.row()][index.column()]
        col = self.headers[index.column()]
        if role == Qt.DisplayRole:
            if col == "exchange":
                return valor.title()
            return valor
        if role == Qt.BackgroundRole:
            isEnabled = self._data[index.row()][5]
            if isEnabled:
                return QColor(127, 212, 150)
            else:
                return QColor(189, 121, 100)
        if role == Qt.DecorationRole:
            if col == "exchange":
                return QIcon(f":/exchanges/{valor}")

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self.headers)

# ────────────────────────────────────────────────────────────────────────────────


class CustomContextMenu(QMenu):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mw = self.parent().parent().parent().parent()
        self.dock = self.parent().parent().parent()

    def handler(self, position):
        index = self.parent().indexAt(position)
        self._valor = self.parent().model().data(index)
        self._alarm = self._get_alarm(position)
        if self._valor is not None and self._alarm is not None:
            self._insertActions()
            self.exec_(self.parent().viewport().mapToGlobal(position))

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def _insertActions(self):
        if self._alarm.enabled:
            self.addAction(self._action("Disable", self.runActionDisable))
        else:
            self.addAction(self._action("Enable", self.runActionEnable))
        self.addSeparator()
        self.addAction(self._action("Edit...", self.runActionEdit))
        self.addAction(self._action("Delete", self.runActionDelete))

    def _get_alarm(self, position):
        try:
            index = self.parent().indexAt(position)
            newindex = self.parent().model().index(index.row(), 0)
            alarm_id = self.parent().model().data(newindex)
            return Alarms.get_by_id(alarm_id)
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

    def runActionDisable(self):
        self._alarm.enabled = False
        self._alarm.save()
        self.dock.refreshTable()

    def runActionEnable(self):
        self._alarm.enabled = True
        self._alarm.save()
        self.dock.refreshTable()

    def runActionEdit(self):
        self.dock.editAlarm(self._alarm.id)

    def runActionDelete(self):
        self.dock.deleteAlarm(self._alarm.id)
