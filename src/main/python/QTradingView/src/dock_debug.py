from PyQt5 import QtWidgets
from .ui.dock_debug import Ui_DockDebug


class DockDebug(QtWidgets.QDockWidget, Ui_DockDebug):
    
    def __init__(self, parent):
        QtWidgets.QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.setVisible(parent.actionDebug.isChecked())


# if self.pagina_info.symbol is not None:
#     path = f'ico/{self.pagina_info.exchange}.png'
#     pixmap = QtGui.QPixmap(path)
