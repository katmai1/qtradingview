import logging
import coloredlogs

from pathlib import Path
import os
from PyQt5 import QtWidgets
from ui.dock_debug_Ui import Ui_DockDebug


class DockDebug(QtWidgets.QDockWidget, Ui_DockDebug):

    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.setVisible(parent.actionDebug.isChecked())


# ─── QLOGGER CLASS ──────────────────────────────────────────────────────────────

class Qlogger(logging.Handler):

    def __init__(self, parent):
        # home = str(Path.home()) + "/.qtradingview"
        # if not os.path.exists(home):
        #     os.mkdir(home)
        # filename = f"{home}/qtradingview.log"
        super().__init__()
        self.parent = parent
        coloredlogs.install()
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.parent.dock_debug.edit_logger.append(msg)

# ────────────────────────────────────────────────────────────────────────────────
