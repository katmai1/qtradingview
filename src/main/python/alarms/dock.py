import logging
from PyQt5 import QtWidgets, QtCore, QtGui
import notify2

from ui.dock_alarms_Ui import Ui_DockAlarms
from models.markets import Alarms
from .dialog import DialogAlarm
from .tasks import CheckAlarms


class DockAlarms(QtWidgets.QDockWidget, Ui_DockAlarms):

    worker = CheckAlarms()

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.setVisible(parent.actionAlarms.isChecked())
        self.tabla_alarms.setColumnHidden(0, True)
        self.refresh_alarms()
        self.btn_delete.released.connect(self.delete_alarm)
        self.tabla_alarms.itemDoubleClicked.connect(self.edit_alarm)
        self.worker.finished.connect(self.start_check_alarms)
        self.worker.start()

    def setVisible(self, visible):
        super().setVisible(visible)
        if visible:
            self.raise_()

    def start_check_alarms(self):
        self.refresh_alarms()
        self.worker.start()

    def refresh_alarms(self):
        self.tabla_alarms.clearContents()
        self.tabla_alarms.setRowCount(0)
        alarms = Alarms.select()
        for row, al in enumerate(alarms):
            self._insert_alarm_to_table(row, al)

    def _insert_alarm_to_table(self, row, data):
        self.tabla_alarms.insertRow(row)
        self._set_cell(row, 0, data.id)
        self._set_cell(row, 1, data.market.symbol)
        self._set_cell(row, 2, data.market.exchange.title())
        self._set_cell(row, 3, data.condition_text())
        self._set_cell(row, 4, "%.8f" % data.price)

    def _set_cell(self, row, col, data):
        self.tabla_alarms.setItem(row, col, QtWidgets.QTableWidgetItem(str(data)))

    def delete_alarm(self):
        item_id = self.tabla_alarms.item(self.tabla_alarms.currentRow(), 0)
        Alarms.delete_by_id(int(item_id.text()))
        self.refresh_alarms()

    def edit_alarm(self, item):
        item_id = self.tabla_alarms.item(item.row(), 0)
        dialog = DialogAlarm(self)
        dialog.edit_alarm(int(item_id.text()))
        result = dialog.exec_()
        if result:
            self.parentWidget().dock_alarms.refresh_alarms()
            self.parentWidget().dock_alarms.raise_()
