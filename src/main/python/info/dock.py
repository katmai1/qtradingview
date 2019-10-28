from PyQt5 import QtWidgets
from ui.dock_info_Ui import Ui_dock_info


class DockInfo(QtWidgets.QDockWidget, Ui_dock_info):
    
    def __init__(self, *args, **kwargs):
        QtWidgets.QDockWidget.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.hide()

# if self.pagina_info.symbol is not None:
#     path = f'ico/{self.pagina_info.exchange}.png'
#     pixmap = QtGui.QPixmap(path)