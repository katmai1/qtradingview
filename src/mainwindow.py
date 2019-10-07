from PyQt5 import QtWidgets, QtCore, QtGui, QtTest
from src.ui.mainwindow import Ui_MainWindow
from src.db import Markets
from .dock_info import DockInfo
from .dock_markets import DockMarkets
from .utils.tradingsource import TradingSource
from time import sleep
from threading import Timer

# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    htmlFinished = QtCore.pyqtSignal(str)

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.html = None
        # carga datos
        self.setWindowIcon(QtGui.QIcon('ico/logo.png'))
        self.chart = TradingSource()
        self._docks()
        self._signals()
    
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
        if onLoad:
            QtCore.QTimer.singleShot(10000, self.update_page_info)
        page = self.webview.page()
        page.toHtml(self._html_parser)

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────
    
    def _docks(self):
        self.dock_markets = DockMarkets(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_markets)
        
        # self.dock_info = DockInfo(self)
        # self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_info)
    
    def _signals(self):
        self.actionPantalla_completa.toggled.connect(self.onActionPantallaCompleta)
        self.actionActualizar_markets.triggered.connect(self.dock_markets.onActionActualizaMarkets)
        self.actiontest.triggered.connect(self.update_page_info)
        self.webview.loadFinished.connect(self.update_page_info)
        self.htmlFinished.connect(self.onLoadPage)
        self.actionMarkets_list.toggled['bool'].connect(self.dock_markets.setVisible)

    def _html_parser(self, html):
        """[funcion async que recibe y emite el codigo fuente de la pagina]
        
        Arguments:
            html {[str]} -- [codigo fuente de la pagina]
        """
        self.htmlFinished.emit(html)
    
    def _load_chart(self, market, exchange=None):
        """[carrega nou market a la grafica]
        
        Arguments:
            market {[str]} -- [market a cargar, tipo: BTC/USD]
        
        Keyword Arguments:
            exchange {[str]} -- [nombre del exchange] (default: {None})
        """
        self.chart.clear()
        self.setWindowTitle("QTradingView")
        self.statusbar.showMessage(f"Cargando market '{market}' en {exchange.title()}")
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QtCore.QUrl(url))
