import logging
import coloredlogs

from PyQt5 import QtWidgets
from qtradingview.ui.dock_debug_Ui import Ui_DockDebug


# ─── PANEL DEBUG ────────────────────────────────────────────────────────────────

class DockDebug(QtWidgets.QDockWidget, Ui_DockDebug):

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle(self.tr('Debug'))
        #
        self.mw = parent
        self.setVisible(self.mw.actionDebug.isChecked())

    def closeEvent(self, event):
        self.mw.actionDebug.setChecked(False)
        self.setVisible(False)

    def onActionEvent(self, actived):
        """ Show/hide this dock and raise if actived """
        self.setVisible(actived)
        if actived:
            self.raise_()

# ────────────────────────────────────────────────────────────────────────────────


# ─── QLOGGER CLASS ──────────────────────────────────────────────────────────────

class Qlogger(logging.Handler):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        log_mode = logging.INFO
        if self.parent.ctx.debug:
            log_mode = logging.DEBUG
        coloredlogs.install(level=log_mode)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.parent.dock_debug.edit_logger.append(msg)

# ────────────────────────────────────────────────────────────────────────────────
