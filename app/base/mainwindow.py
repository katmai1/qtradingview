import logging
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMessageBox

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
        self.splash.hide()

    # signal connectors
    def _signals(self):
        self.actionSettings.triggered.connect(self.openDialogSettings)
        self.actionFull_Screen.toggled.connect(self.onActionFullScreen)
        self.actionMarkets.toggled['bool'].connect(self.dock_markets.setVisible)
        self.actionDebug.toggled['bool'].connect(self.dock_debug.setVisible)
        self.actionPortfolio.toggled['bool'].connect(self.dock_portfolio.setVisible)
        self.actionAlarms.toggled['bool'].connect(self.dock_alarms.setVisible)
        self.actionAbout.triggered.connect(self.openAboutDialog)

    def _docks(self):
        self.setTabPosition(QtCore.Qt.BottomDockWidgetArea, QtWidgets.QTabWidget.South)
        self.setTabPosition(QtCore.Qt.LeftDockWidgetArea, QtWidgets.QTabWidget.North)
        self.actionDebug.setChecked(self.config['panel_debug_active'])
        self.actionMarkets.setChecked(self.config['panel_markets_active'])
        self.actionPortfolio.setChecked(self.config['panel_portfolio_active'])
        #
        self.dock_markets = DockMarkets(self)
        self.dock_debug = DockDebug(self)
        self.dock_portfolio = DockPortfolio(self)
        self.dock_alarms = DockAlarms(self)
        #
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_markets)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dock_alarms)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock_debug)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dock_portfolio)
        self.tabifyDockWidget(self.dock_markets, self.dock_alarms)
        self.tabifyDockWidget(self.dock_portfolio, self.dock_debug)

    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    def openAboutDialog(self):
        dialog = DialogAbout(self)
        dialog.exec_()

    def set_text_status(self, text, msecs=3000):
        self.statusbar.showMessage(text, msecs=msecs)

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
        self.config['panel_markets_active'] = self.actionMarkets.isChecked()
        self.config['panel_portfolio_active'] = self.actionPortfolio.isChecked()
        self.config['panel_debug_active'] = self.actionDebug.isChecked()
        self.ctx.save_config()

    # ────────────────────────────────────────────────────────────────────────────────

    # carga un market en la pagina
    def load_chart(self, market, exchange):
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QtCore.QUrl(url))
        self.currentExchange = exchange
        self.currentMarket = market
