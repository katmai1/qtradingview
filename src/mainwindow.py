from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui.mainwindow import Ui_MainWindow
from src.db import Markets
from src.tasks.update_markets_db import UpdateMarkets_DB
from bs4 import BeautifulSoup


class TradingSource:
    '''clase per extreure dades de la pagina de tradingview'''

    def __init__(self):
        self.html = None
        self.soup = None

    def read_html(self, html):
        self.html = html
        self.soup = BeautifulSoup(html, 'html5lib')
    
    @property
    def titulo(self):
        return self.soup.title.string

    @property
    def full_symbol(self):
        for script in self.soup.find_all("script"):
            if "editchart.model.symbol" in script.text:
                raw = str(script.text).split('"editchart.model.symbol":')[1].split(',')[0]
                return raw.replace('"', '')
        return None
    
    @property
    def exchange(self):
        return self.full_symbol.split(":")[0].lower()
    
    @property
    def symbol(self):
        return self.full_symbol.split(":")[1]


# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    
    exchanges = ['binance', 'bitfinex']

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        # signals
        self.actionPantalla_completa.toggled.connect(self.onActionPantallaCompleta)
        self.actionActualizar_markets.triggered.connect(self.onActionActualizaMarkets)
        self.combo_exchange.currentTextChanged.connect(self.onExchangeChanged)
        self.list_markets.itemDoubleClicked.connect(self.onDoubleClickMarket)
        self.actiontest.triggered.connect(self.update_page_info)
        # carga datos
        self.setWindowIcon(QtGui.QIcon('ico/logo.png'))
        self._load_exchanges()
        self.onExchangeChanged()
        self.pagina_info = TradingSource()

    @property
    def selected_exchange(self):
        return self.combo_exchange.currentText().lower()
    
    # ─── EVENTOS ────────────────────────────────────────────────────────────────────

    def onActionPantallaCompleta(self):
        if self.actionPantalla_completa.isChecked():
            self.showFullScreen()
        else:
            self.showMaximized()

    def onActionActualizaMarkets(self):
        t = UpdateMarkets_DB(self)
        t.run()
    
    def onExchangeChanged(self):
        exchange = self.combo_exchange.currentText().lower()
        self.list_markets.clear()
        lista = Markets.select().where(Markets.exchange == exchange)
        for it in lista:
            self.list_markets.addItem(it.symbol)
    
    def onDoubleClickMarket(self, item):
        self._load_chart(item.text(), self.selected_exchange)

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────
    
    def update_page_info(self):
        def html_parser(html):
            self.pagina_info.read_html(html)
            self.label_loaded.setText(self.pagina_info.symbol)
            path = f'ico/{self.pagina_info.exchange}.png'
            pixmap = QtGui.QPixmap(path)
            self.label_logo.setPixmap(pixmap.scaled(64, 64))
            print(self.pagina_info.titulo)
        self.webview.page().toHtml(html_parser)

    def _load_exchanges(self):
        '''Carga la lista de exchanges en el combo'''
        self.combo_exchange.clear()
        for x in self.exchanges:
            path = f"ico/{x}.png"
            self.combo_exchange.addItem(QtGui.QIcon(path), x.title())

    def _load_chart(self, market, exchange=None):
        if exchange is None:
            exchange = self.selected_exchange
        self.statusbar.showMessage(f"Cargando market '{market}' en {exchange.title()}", 3000)
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QtCore.QUrl(url))
