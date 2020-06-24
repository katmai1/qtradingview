import logging
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from app.markets.dock import DockMarkets
from app.debug.dock import DockDebug, Qlogger

from app.base.widgets import CustomWebEnginePage
from app.base.dialog_config import DialogConfig
from app.ui.mainwindow_Ui import Ui_MainWindow


# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, ctx, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #
        # self.html = None
        self.ctx = ctx
        self.config = ctx.config

        # webenginepage
        page = CustomWebEnginePage(self.webview)
        self.webview.setPage(page)

        # signals
        self._docks()
        self._signals()

        # logs
        log_mode = logging.INFO
        if self.ctx.debug:
            log_mode = logging.DEBUG
        qlog = Qlogger(self)
        logging.getLogger().addHandler(qlog)
        logging.getLogger().setLevel(log_mode)

        # carga market inicial
        self.load_chart(self.config['initial_market'], self.config['initial_exchange'])

    # translate
    def _tr(self, contexto, mensaje):
        return self.ctx.tr(contexto, mensaje)

    # signal connectors
    def _signals(self):
        self.actionSettings.triggered.connect(self.openDialogSettings)
        self.actionFull_Screen.toggled.connect(self.onActionFullScreen)
        self.actionMarkets.toggled['bool'].connect(self.dock_markets.setVisible)
        self.actionDebug.toggled['bool'].connect(self.dock_debug.setVisible)
        self.dock_markets.statusbar_signal.connect(self.set_text_status)

    def _docks(self):
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        self.dock_markets = DockMarkets(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_markets)
        self.dock_debug = DockDebug(self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock_debug)

    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    def set_text_status(self, text, ms=2000):
        self.statusbar.showMessage(text, msecs=ms)

    # config dialog
    def openDialogSettings(self):
        dialog = DialogConfig(self)
        dialog.load_config(self.config)
        if dialog.exec_():
            if dialog.exchanges_is_changed:
                self.dock_markets._load_exchanges()

    # fullscreen
    def onActionFullScreen(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()
            self.showMaximized()

    # confirmacion de salida
    def closeEvent(self, event):
        result = QMessageBox.question(self, self._tr("mainwindow", 'Exit'), self._tr("mainwindow", "Do you want quit?"))
        if int(result) == 16384:
            self.ctx.app.quit()
        else:
            event.ignore()

    # ────────────────────────────────────────────────────────────────────────────────

    # carga un market en la pagina
    def load_chart(self, market, exchange):
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QtCore.QUrl(url))
        self.currentExchange = exchange
        self.currentMarket = market
