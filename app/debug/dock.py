import os
import logging
import coloredlogs

from PyQt5 import QtWidgets, uic
from app.utils import resource_path


class DockDebug(QtWidgets.QDockWidget):

    ui_filename = "dock_debug.ui"

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent)
        uic.loadUi(resource_path(self.ui_filename), self)
        #
        self.mw = parent
        self.setVisible(self.mw.actionDebug.isChecked())


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
