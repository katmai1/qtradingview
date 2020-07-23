from PyQt5.QtWidgets import QDockWidget

from app.ui.dock_alarms_Ui import Ui_DockAlarms

from .widgets import AlarmsTableModel
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
        self.tb_alarms.resizeColumnsToContents()
    
    def addAlarm(self, exchange, market):
        """Create new alarm"""
        d = DialogAlarm(exchange, market)
        d.loadNewAlarm()
        if d.exec_():
            d.createAlarm()
            self.refreshTable()
 
# ────────────────────────────────────────────────────────────────────────────────
