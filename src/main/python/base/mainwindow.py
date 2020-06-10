
import logging

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication as qapp

from ui.mainwindow_Ui import Ui_MainWindow

from debug.dock import DockDebug, Qlogger
from markets.dock import DockMarkets
from alarms.dock import DockAlarms

from .dialog_config import DialogConfig
from .utils import TradingSource
from .widgets import CustomWebEnginePage, CustomSplashScreen
# from .tasks import UpdateMarkets_DB

from models.markets import Markets


# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    htmlFinished = QtCore.pyqtSignal(str)

    def __init__(self, ctx, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.html = None
        self.ctx = ctx
        self.config = ctx.config
        # splash
        splash = CustomSplashScreen(self)
        splash.show()
        # webenginepage
        page = CustomWebEnginePage(self.webview)
        self.webview.setPage(page)

        # docks
        self._docks()
        self._signals()

        # carga datos
        self.chart = TradingSource()

        # logs
        qlog = Qlogger(self)
        logging.getLogger().addHandler(qlog)
        logging.getLogger().setLevel(logging.INFO)

        # loaded
        splash.finish(self)
        self.load_chart(self.config['initial_market'], self.config['initial_exchange'])

    # ─── BASE ───────────────────────────────────────────────────────────────────────

    def _tr(self, contexto, mensaje):
        return self.ctx.app.translate(contexto, mensaje)

    def _docks(self):
        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QtWidgets.QTabWidget.North)
        self.dock_markets = DockMarkets(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_markets)
        self.dock_alarms = DockAlarms(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_alarms)
        self.dock_debug = DockDebug(self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock_debug)
        self.tabifyDockWidget(self.dock_markets, self.dock_alarms)

    def _signals(self):
        # docks actions
        self.actionMarkets.toggled['bool'].connect(self.dock_markets.setVisible)
        self.actionDebug.toggled['bool'].connect(self.dock_debug.setVisible)
        self.actionAlarms.toggled['bool'].connect(self.dock_alarms.setVisible)
        self.actionConfigurar.triggered.connect(self.openDialogConfigurar)
        # other actions
        self.actionPantalla_completa.toggled.connect(self.onActionPantallaCompleta)
        # self.actionActualizar_markets.triggered.connect(self.dock_markets.onActionActualizaMarkets)
        # webview related
        self.webview.loadFinished.connect(self.update_page_info)
        self.htmlFinished.connect(self.onLoadPage)

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.question(
            self, qapp.translate("mainwindow", 'Salir'),
            qapp.translate("mainwindow", "Quieres cerrar la aplicacion?"),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        if result:
            return super().closeEvent(event)

    # ─── EVENTOS ────────────────────────────────────────────────────────────────────
        
    def openDialogConfigurar(self):
        dialog = DialogConfig(self)
        dialog.load_config(self.config)
        dialog.exec_()

    def onLoadPage(self, html):
        """ recibe la señal para recibir el html"""
        self.chart.read_html(html)
        if self.chart.market is not None or self.chart.exchange is not None:
            self.statusbar.clearMessage()
            titol = f"{self.currentMarket} ({self.chart.exchange.title()}) | QTradingView"
            self.setWindowTitle(titol)
            self.webview.page().adblocker_tradingview()
        else:
            QtCore.QTimer.singleShot(10000, self.update_page_info)

    def onActionPantallaCompleta(self):
        if self.actionPantalla_completa.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()
            self.showMaximized()

    # ─── PUBLIC METHODS ─────────────────────────────────────────────────────────────

    def update_page_info(self):
        page = self.webview.page()
        page.toHtml(self._html_parser)

    def load_chart(self, market, exchange):
        self.chart.clear()
        self.setWindowTitle("QTradingView")
        mensaje = qapp.translate("mainwindow", "Cargando mercado")
        self.statusbar.showMessage(f"{mensaje} {market} ({exchange.title()})...")
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QtCore.QUrl(url))
        self.currentExchange = exchange
        self.currentMarket = market

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def _html_parser(self, html):
        self.htmlFinished.emit(html)

# ────────────────────────────────────────────────────────────────────────────────
