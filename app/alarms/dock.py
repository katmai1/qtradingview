from PyQt5 import QtWidgets, QtCore

from app.ui.dock_alarms_Ui import Ui_DockAlarms
from .models import Alarms


# ─── DOCK PORTFOLIO ─────────────────────────────────────────────────────────────

class DockAlarms(QtWidgets.QDockWidget, Ui_DockAlarms):

    def __init__(self, parent=None):
        QtWidgets.QDockWidget.__init__(self, parent=parent)
        self.setupUi(self)
        self.mw = parent
        self.setWindowTitle("Alarms")
        #
        self.setVisible(self.mw.actionAlarms.isChecked())

    def closeEvent(self, event):
        self.mw.actionAlarms.setChecked(False)
        self.setVisible(False)

    def setVisible(self, active):
        """Show/hide this dock and start/stop refreshing table timer"""
        return super().setVisible(active)

# ────────────────────────────────────────────────────────────────────────────────
