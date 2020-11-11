from PyQt5.QtWidgets import QDockWidget, QMessageBox
from PyQt5.QtCore import QTimer

from qtradingview.ui.dock_alarms_Ui import Ui_DockAlarms

from .widgets import AlarmsTableModel, CustomContextMenu
from .models import Alarms
from .dialog import DialogAlarm


# ─── DOCK PORTFOLIO ─────────────────────────────────────────────────────────────

class DockAlarms(QDockWidget, Ui_DockAlarms):

    def __init__(self, parent=None):
        QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.mw = parent
        self.setWindowTitle(self.tr("Alarms"))
        #
        self.setVisible(self.mw.actionAlarms.isChecked())
        self.refreshTable()
        #
        self.alarm_checker = QTimer(self)
        self.alarm_checker.setInterval(10000)
        self.alarm_checker.timeout.connect(self.checkAlarms)
        self.alarm_checker.start()
        self.tb_alarms.customContextMenuRequested.connect(self.contextoMenuEvent)

    def contextoMenuEvent(self, position):
        """Load contextual menu"""
        contextMenu = CustomContextMenu(self.tb_alarms)
        index = self.tb_alarms.indexAt(position)
        if index.isValid():
            contextMenu.handler(position)

    def checkAlarms(self):
        for alarm in Alarms.get_all():
            if alarm.enabled:
                if alarm.isComplished:
                    titulo = f"#{alarm.id} {alarm.market.symbol}"
                    msg = f"Alarm #{alarm.id} | This alarm is complished with condition '{alarm.condition_label} {alarm.price:.8}'"
                    self.mw.notify(titulo, msg)
                    alarm.disable()
                    if alarm.autodelete:
                        alarm.delete_instance()
        self.refreshTable()

    def onActionEvent(self, actived):
        """ Show/hide this dock and raise if actived """
        self.setVisible(actived)
        if actived:
            self.raise_()

    def closeEvent(self, event):
        self.mw.actionAlarms.setChecked(False)
        self.setVisible(False)

    def setVisible(self, active):
        """Show/hide this dock and start/stop refreshing table timer"""
        return super().setVisible(active)

    def refreshTable(self):
        """Add data from database"""
        data, headers = Alarms.getAlarmsToTable()
        self.model = AlarmsTableModel(data, headers)
        self.tb_alarms.setModel(self.model)
        self.tb_alarms.hideColumn(5)
        self.tb_alarms.resizeColumnsToContents()

    def addAlarm(self, exchange, market):
        """ Open dialog to create new alarm"""
        d = DialogAlarm(self)
        d.loadNewAlarm(exchange, market)
        if d.exec_():
            d.createAlarm()
            self.refreshTable()

    def editAlarm(self, alarm_id):
        """ Open dialog to edit alarm"""
        d = DialogAlarm(self)
        d.loadAlarm(alarm_id)
        if d.exec_():
            d.updateAlarm(alarm_id)
            self.refreshTable()

    def deleteAlarm(self, alarm_id):
        """Delete trade from trade_id"""
        result = QMessageBox.question(
            self, f"Alarm {alarm_id}", self.tr("Do you want delete this alarm?"),
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if result == QMessageBox.Yes:
            Alarms.delete_by_id(alarm_id)
            self.refreshTable()

# ────────────────────────────────────────────────────────────────────────────────
