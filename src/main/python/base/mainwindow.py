
import logging

from PyQt5 import QtCore, QtWidgets, QtGui

from ui.mainwindow_Ui import Ui_MainWindow

from debug.dock import DockDebug, Qlogger
from markets.dock import DockMarkets
from markets.tasks import UpdateMarkets_DB

from .utils import TradingSource
from .widgets import CustomWebEnginePage, CustomSplashScreen

from db import Markets


# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    htmlFinished = QtCore.pyqtSignal(str)
    
    # default config
    initial_exchange = "bitfinex"
    initial_market = "BTC/USD"
    exchanges_enabled = ['binance', 'bitfinex', 'poloniex']

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.html = None
        # splash
        splash = CustomSplashScreen(self)
        splash.show()
        splash.set_texto("loading...")
        # webenginepage
        page = CustomWebEnginePage(self.webview)
        self.webview.setPage(page)

        # si la tabla markets esta vacía hacemos el primer update
        if Markets.select().count() == 0:
            splash.set_texto("updating markets database...")
            t = UpdateMarkets_DB(self)
            t.run()

        # docks
        self._docks()
        self._signals()
        
        # carga datos
        self.chart = TradingSource()
        
        # logs
        qlog = Qlogger(self)
        logging.getLogger().addHandler(qlog)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # loaded
        splash.finish(self)
        self.load_chart(self.initial_market, self.initial_exchange)

    # ─── BASE ───────────────────────────────────────────────────────────────────────

    def _docks(self):
        self.dock_markets = DockMarkets(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_markets)
        self.dock_debug = DockDebug(self)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock_debug)

    def _signals(self):
        # docks actions
        self.actionMarkets.toggled['bool'].connect(self.dock_markets.setVisible)
        self.actionDebug.toggled['bool'].connect(self.dock_debug.setVisible)
        # other actions
        self.actionPantalla_completa.toggled.connect(self.onActionPantallaCompleta)
        self.actionActualizar_markets.triggered.connect(self.dock_markets.onActionActualizaMarkets)
        # webview related
        self.webview.loadFinished.connect(self.update_page_info)
        self.htmlFinished.connect(self.onLoadPage)
        # test action
        self.actiontest.triggered.connect(self.update_page_info)

    # ─── EVENTOS ────────────────────────────────────────────────────────────────────

    def onLoadPage(self, html):
        """ recibe la señal para recibir el html"""
        self.chart.read_html(html)
        if self.chart.market is not None or self.chart.exchange is not None:
            self.statusbar.clearMessage()
            titol = f"{self.currentMarket} ({self.chart.exchange.title()}) | QTradingView"
            self.setWindowTitle(titol)
            self.dock_markets.set_currentInfo(self.currentExchange, self.currentMarket)
            self.webview.page().adblocker_tradingview()                               
        else:
            QtCore.QTimer.singleShot(10000, self.update_page_info)

    def onActionPantallaCompleta(self):
        if self.actionPantalla_completa.isChecked():
            self.showFullScreen()
        else:
            self.showMaximized()

    # ─── PUBLIC METHODS ─────────────────────────────────────────────────────────────

    def update_page_info(self):
        page = self.webview.page()
        page.toHtml(self._html_parser)

    def load_chart(self, market, exchange):
        self.chart.clear()
        self.setWindowTitle("QTradingView")
        self.statusbar.showMessage(f"Cargando market '{market}' en {exchange.title()}...")
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QtCore.QUrl(url))
        self.currentExchange = exchange
        self.currentMarket = market
        self.dock_markets.clear_currentInfo()

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def _html_parser(self, html):
        self.htmlFinished.emit(html)

# ────────────────────────────────────────────────────────────────────────────────
