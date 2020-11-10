import logging
from PyQt5.QtWidgets import QMessageBox, QLabel, QMainWindow, QTabWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSound

from notificator import notificator
from notificator.alingments import BottomRight

from qtradingview.markets.dock import DockMarkets
from qtradingview.debug.dock import DockDebug, Qlogger
from qtradingview.portfolio.dock import DockPortfolio
from qtradingview.alarms.dock import DockAlarms

from qtradingview.ui.mainwindow_Ui import Ui_MainWindow

from .widgets import CustomWebEnginePage, CustomSplashScreen
from .dialog_config import DialogConfig
from .dialog_about import DialogAbout


# ─── MAIN WINDOW ────────────────────────────────────────────────────────────────

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, ctx, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #
        self.splash = CustomSplashScreen(self)
        self.ctx = ctx
        self.cfg = self.ctx.settings
        self._notify = notificator()

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
            self.cfg.value('settings/initial_market'),
            self.cfg.value('settings/initial_exchange')
        )
        self.splash.hide()
        self.static_price = QLabel("- BTC/USDT ")
        self.statusbar.addPermanentWidget(self.static_price)

    def _loadInitialConfig(self):
        # size
        size = self.cfg.value("window/size")
        if size is None:
            self.showMaximized()
        else:
            self.resize(size)
        # position
        position = self.cfg.value("window/pos")
        if position is not None:
            self.move(position)
        # set panels checked
        self.actionDebug.setChecked(self.cfg.value("debug/checked", defaultValue=False, type=bool))
        self.actionMarkets.setChecked(self.cfg.value("markets/checked", defaultValue=True, type=bool))
        self.actionPortfolio.setChecked(self.cfg.value("portfolio/checked", defaultValue=False, type=bool))
        self.actionAlarms.setChecked(self.cfg.value("alarms/checked", defaultValue=False, type=bool))

    def _signals(self):
        """ Define signals """
        self.actionSettings.triggered.connect(self.openDialogSettings)
        self.actionFull_Screen.toggled.connect(self.onActionFullScreen)
        self.actionMarkets.toggled['bool'].connect(self.dock_markets.onActionEvent)
        self.actionDebug.toggled['bool'].connect(self.dock_debug.onActionEvent)
        self.actionPortfolio.toggled['bool'].connect(self.dock_portfolio.onActionEvent)
        self.actionAlarms.toggled['bool'].connect(self.dock_alarms.onActionEvent)
        self.actionAbout.triggered.connect(self.openAboutDialog)

    def _docks(self):
        self.setTabPosition(Qt.BottomDockWidgetArea, QTabWidget.South)
        self.setTabPosition(Qt.LeftDockWidgetArea, QTabWidget.West)
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

    def _quit(self):
        if self.dock_markets.markets_updater.isRunning():
            self.dock_markets.markets_updater.terminate()
            self.set_text_status(self.tr("Closing background processes..."))
        self.ctx.app.quit()

    def _remember_panels(self):
        self.cfg.setValue("markets/checked", self.actionMarkets.isChecked())
        self.cfg.setValue("markets/list_mode", self.dock_markets.lista_mode)
        self.cfg.setValue("portfolio/checked", self.actionPortfolio.isChecked())
        self.cfg.setValue("debug/checked", self.actionDebug.isChecked())
        self.cfg.setValue("alarms/checked", self.actionAlarms.isChecked())
        self.cfg.setValue("window/size", self.size())
        self.cfg.setValue("window/pos", self.pos())

    # ─── EVENTS ─────────────────────────────────────────────────────────────────────

    # fullscreen
    def onActionFullScreen(self):
        if self.actionFull_Screen.isChecked():
            self.showFullScreen()
        else:
            self.showNormal()
            self.showMaximized()

    def closeEvent(self, event):
        """ Quit app event """
        mbox = QMessageBox(self)
        mbox.setIcon(QMessageBox.Question)
        mbox.setWindowTitle(self.tr('Exit'))
        mbox.setText(self.tr("Do you want quit?"))
        mbox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        result = mbox.exec_()
        if int(result) == 16384:
            self._remember_panels()
            self._quit()
        event.ignore()

    # ─── PUBLIC METHODS ──────────────────────────────────────────────

    def notify(self, titulo, texto, tipo="sucess", duracion=None):
        """ Public method to generate notifications """
        QSound.play(":/base/notify")
        if tipo == "sucess":
            self._notify.sucess(titulo, texto, self, BottomRight, duracion=duracion)
        elif tipo == "critical":
            self._notify.critical(titulo, texto, self, BottomRight, duracion=duracion)
        elif tipo == "info":
            self._notify.info(titulo, texto, self, BottomRight, duracion=duracion)
        elif tipo == "warning":
            self._notify.warning(titulo, texto, self, BottomRight, duracion=duracion)
        # else:
        #     self._notify.custom(titulo, texto, self, BottomRight, duracion=duracion)

    def openAboutDialog(self):
        dialog = DialogAbout(self)
        dialog.exec_()

    def set_text_status(self, text, msecs=3000):
        self.statusbar.showMessage(text, msecs=msecs)

    def openDialogSettings(self):
        """ Open dialog settings and reload exchanges if needed """
        dialog = DialogConfig(self)
        if dialog.exec_():
            if dialog.exchanges_is_changed:
                self.dock_markets.markets_updater.first_run = True
                self.dock_markets._load_exchanges()

    # carga un market en la pagina
    def load_chart(self, market, exchange):
        mar, ket = market.split("/")
        url = f"https://es.tradingview.com/chart/?symbol={exchange.upper()}:{mar}{ket}"
        self.webview.setUrl(QUrl(url))
        self.currentExchange = exchange
        self.currentMarket = market
