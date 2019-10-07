from PyQt5 import QtWidgets
import sys
from src.db import crea_tablas

from src.mainwindow import MainWindow


if __name__ == "__main__":
    crea_tablas()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())