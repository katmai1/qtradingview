import os
import sys
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow
from src.mainwindow import MainWindow

if __name__ == '__main__':
    # is_new_db = False
    # if not db.table_exists('markets'):
    #     print("tabla no existe")
    #     crea_tablas()
    #     is_new_db = True
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow()
    window.showMaximized()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)