from PyQt5 import QtWidgets

from qtradingview.ui.about_Ui import Ui_aboutDialog


class DialogAbout(QtWidgets.QDialog, Ui_aboutDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
