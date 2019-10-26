
import logging
import time

import coloredlogs
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWebEngineWidgets import QWebEnginePage

from dock_debug import DockDebug
from dock_markets import DockMarkets
from ui.mainwindow_Ui import Ui_MainWindow
from utils.tradingsource import TradingSource
from tasks.update_markets_db import UpdateMarkets_DB
from db import Markets


# ─── QLOGGER CLASS ──────────────────────────────────────────────────────────────

class Qlogger(logging.Handler):

    """ Description	"""

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        coloredlogs.install()
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        self.parent.dock_debug.edit_logger.append(msg)

# ────────────────────────────────────────────────────────────────────────────────


# ─── CUSTOM WEBENGINEPAGE ───────────────────────────────────────────────────────

class WebEnginePage(QWebEnginePage):

    """[summary]"""

    def javaScriptConsoleMessage(self, level, msg, line, sourceID):
        pass

# ────────────────────────────────────────────────────────────────────────────────


# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    htmlFinished = QtCore.pyqtSignal(str)
    
    # default config
    initial_exchange = "bitfinex"
    initial_market = "BTC/USD"
    exchanges = ['binance', 'bitfinex']

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        # splash
        splash = self._get_splash()
        splash.showMessage("<h1>Loading...</h1>", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
        splash.show()
        # widgets
        self.setupUi(self)
        #
        self.html = None
        page = WebEnginePage(self.webview)
        self.webview.setPage(page)

        # si la tabla markets esta vacía hacemos el primer update
        if Markets.select().count() == 0:
            splash.showMessage("<h1>Updating markets database...</h1>", QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
            t = UpdateMarkets_DB(self)
            t.run()

        self._docks()
        self._signals()
        # carga datos
        self.chart = TradingSource()
        #
        qlog = Qlogger(self)
        logging.getLogger().addHandler(qlog)
        logging.getLogger().setLevel(logging.DEBUG)
        
        # loaded
        splash.finish(self)
        self._load_chart(self.initial_market, self.initial_exchange)

    # ─── BASE ───────────────────────────────────────────────────────────────────────

    # TODO: crear clase que heredi splashscreen i personalitzarla bé
    def _get_splash(self):
        splash_pix = QtGui.QPixmap(":/base/splash.png")
        splash_pix.scaledToHeight(250, QtCore.Qt.SmoothTransformation)
        splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.SplashScreen)
        font = splash.font()
        font.setPixelSize(24)
        font.setWeight(QtGui.QFont.Bold)
        splash.setFont(font)
        splash.setContentsMargins(100, 100, 100, 100)
        return splash

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
        """[recibe la señal para recibir el html]

        Arguments:
            html {[str]} -- [codigo fuente html]
        """
        self.chart.read_html(html)
        if self.chart.market is not None or self.chart.exchange is not None:
            titol = f"{self.chart.market} | {self.chart.exchange.title()} | QTradingView"
            self.setWindowTitle(titol)
            self.statusbar.clearMessage()
            self.webview.page().runJavaScript(
                                """(function() {
                'use strict';
                const checkAd = setInterval(() => {
                    const adBox = document.getElementById('tv-toasts');
                    if (adBox) {
                    adBox.remove();
                    console.log('ad removed.');
                    } else {
                    console.log('no ad present.');
                    }
                }, 5000);
                })();"""
            )
        else:
            QtCore.QTimer.singleShot(10000, self.update_page_info)

    def onActionPantallaCompleta(self):
        if self.actionPantalla_completa.isChecked():
            self.showFullScreen()
        else:
            self.showMaximized()

    # ─── PUBLIC METHODS ─────────────────────────────────────────────────────────────

    def update_page_info(self, onLoad=False):
        """[funcion para solicitar actualizacion de codigo fuente web]

        Keyword Arguments:
            onLoad {bool} -- [es True cuando venimos del evento WebLoadFinished] (default: {False})
        """
        # if onLoad:
        #     QtCore.QTimer.singleShot(10000, self.update_page_info)
        page = self.webview.page()
        page.toHtml(self._html_parser)

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────


    def _html_parser(self, html):
        """
        [funcion async que recibe y emite el codigo fuente de la pagina]

        Arguments:
            html {[str]} -- [codigo fuente de la pagina]
        """
        self.htmlFinished.emit(html)

    def _load_chart(self, market, exchange):
        """[carrega nou market a la grafica]

        Arguments:
            market {[str]} -- [market a cargar, tipo: BTC/USD]

        Keyword Arguments:
            exchange {[str]} -- [nombre del exchange] (default: {None})
        """
        self.chart.clear()
        self.setWindowTitle("QTradingView")
        self.statusbar.showMessage(f"Cargando market '{market}' en {exchange.title()}...")
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QtCore.QUrl(url))
        self.currentExchange = exchange
        self.currentMarket = market

# ────────────────────────────────────────────────────────────────────────────────
