from fbs_runtime.application_context.PyQt5 import ApplicationContext
from base.mainwindow import MainWindow
from db import db, crea_tablas

import sys


if __name__ == '__main__': 
    if not db.table_exists("markets"):
        print("No existe la tabla markets, creando...")
        crea_tablas()
    #
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow()
    window.showMaximized()
    #
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)