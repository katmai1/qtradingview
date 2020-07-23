import logging
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt, QUrl

from app.markets.dock import DockMarkets
from app.debug.dock import DockDebug, Qlogger
from app.portfolio.dock import DockPortfolio
from app.alarms.dock import DockAlarms

from app.ui.mainwindow_Ui import Ui_MainWindow

from .widgets import CustomWebEnginePage, CustomSplashScreen
from .dialog_config import DialogConfig
from .dialog_about import DialogAbout


# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, ctx, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #
        self.splash = CustomSplashScreen(self)
        self.ctx = ctx
        # self.config = ctx.config
        self.cfg = self.ctx.settings
        
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
        self._loadInitialConfig()
        self.load_chart(
            self.cfg.value('initial_market', defaultValue="BTC/USDT"),
            self.cfg.value('initial_exchange', defaultValue="binance")
        )
        self.splash.hide()

    def _loadInitialConfig(self):
        # set window size and position
        if self.cfg.contains("window/size"):
            self.resize(self.cfg.value("window/size"))
        if self.cfg.contains("window/pos"):
            self.move(self.cfg.value("window/pos"))
        # set panels checked
        self.actionDebug.setChecked(self.cfg.value("debug/checked", defaultValue=False, type=bool))
        self.actionMarkets.setChecked(self.cfg.value("markets/checked", defaultValue=True, type=bool))
        self.actionPortfolio.setChecked(self.cfg.value("portfolio/checked", defaultValue=False, type=bool))
        self.actionAlarms.setChecked(self.cfg.value("alarms/checked", defaultValue=False, type=bool))

    # signal connectors
    def _signals(self):
        self.actionSettings.triggered.connect(self.openDialogSettings)
        self.actionFull_Screen.toggled.connect(self.onActionFullScreen)
        self.actionMarkets.toggled['bool'].connect(self.dock_markets.setVisible)
        self.actionDebug.toggled['bool'].connect(self.dock_debug.setVisible)
        self.actionPortfolio.toggled['bool'].connect(self.dock_portfolio.setVisible)
        self.actionAlarms.toggled['bool'].connect(self.onActionAlarms)
        self.actionAbout.triggered.connect(self.openAboutDialog)

    def _docks(self):
        self.setTabPosition(Qt.BottomDockWidgetArea, QtWidgets.QTabWidget.South)
        self.setTabPosition(Qt.LeftDockWidgetArea, QtWidgets.QTabWidget.West)
        #
        self.dock_markets = DockMarkets(self)
        self.dock_debug = DockDebug(self)
        self.dock_portfolio = DockPortfolio(self)
        self.dock_alarms = DockAlarms(self)
        #
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_markets)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock_alarms)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_debug)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock_portfolio)
        self.tabifyDockWidget(self.dock_markets, self.dock_alarms)
        self.tabifyDockWidget(self.dock_portfolio, self.dock_debug)

    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    def onActionAlarms(self, actived):
        self.dock_alarms.setVisible(actived)
        if actived:
            self.dock_alarms.raise_()

    def openAboutDialog(self):
        dialog = DialogAbout(self)
        dialog.exec_()

    def set_text_status(self, text, msecs=3000):
        self.statusbar.showMessage(text, msecs=msecs)

    # config dialog
    def openDialogSettings(self):
        dialog = DialogConfig(self)
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
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle(self.tr('Exit'))
        mbox.setText(self.tr("Do you want quit?"))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        result = mbox.exec_()
        if int(result) == 16384:
            self.remember_panels()
            self.quit()
        event.ignore()

    def quit(self):
        if self.dock_markets.markets_updater.isRunning():
            self.dock_markets.markets_updater.terminate()
            self.set_text_status(self.tr("Closing background processes..."))
        self.ctx.app.quit()
    
    def remember_panels(self):
        self.cfg.setValue("markets/checked", self.actionMarkets.isChecked())
        self.cfg.setValue("portfolio/checked", self.actionPortfolio.isChecked())
        self.cfg.setValue("debug/checked", self.actionDebug.isChecked())
        self.cfg.setValue("alarms/checked", self.actionAlarms.isChecked())
        self.cfg.setValue("window/size", self.size())
        self.cfg.setValue("window/pos", self.pos())

    # ────────────────────────────────────────────────────────────────────────────────

    # carga un market en la pagina
    def load_chart(self, market, exchange):
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QUrl(url))
        self.currentExchange = exchange
        self.currentMarket = market
