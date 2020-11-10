import os
import shutil

from signal import signal, SIGINT, SIG_DFL
from cached_property import cached_property

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLibraryInfo, QTranslator, QSettings

from qtradingview.utils import AppUtil
from qtradingview.models.base import get_db, migrate

from qtradingview.models.markets import Markets
from qtradingview.portfolio.models import Trades
from qtradingview.alarms.models import Alarms

from qtradingview.base.mainwindow import MainWindow


# ─── CONTEXTO APP ───────────────────────────────────────────────────────────────

class ContextoApp:

    #     os.system("export QT_LOGGING_RULES='*=false'")
    def __init__(self, args):
        self.app = QApplication([])
        self.debug = args['--debug']
        signal(SIGINT, SIG_DFL)
        self.args = args
        self.setDefaultConfig()

    def run(self):
        self.window.show()
        return self.app.exec_()

    def tr(self, context, message):
        return self.app.translate(context, message)

    def deleteDatabaseFile(self):
        dirname = os.path.dirname(self.settings.fileName())
        nou_path = os.path.join(dirname, 'database.db')
        os.remove(nou_path)
        if not AppUtil.isPyinstaller():
            shutil.rmtree('migrations', ignore_errors=True)

    def createDB(self):
        self.db.create_tables([Markets, Trades, Alarms])

    def createTablesDB(self):
        """ Creating or updating database tables. """
        if AppUtil.isPyinstaller():
            self.db.create_tables([Markets, Trades, Alarms])
        else:
            migrate(self.db)

    def checkTablesExists(self):
        """ Returns True if all tables exists """
        if not Markets.table_exists():
            return False
        if not Trades.table_exists():
            return False
        if not Alarms.table_exists():
            return False
        return True

    def setDefaultConfig(self):
        if self.settings.value("settings/exchanges") is None:
            self.settings.setValue("settings/exchanges", ["Binance", "Bitfinex"])
        if self.settings.value("settings/language") is None:
            self.settings.setValue("settings/language", "en_EN")
        if self.settings.value("settings/initial_exchange") is None:
            self.settings.setValue("settings/initial_exchange", "Binance")
        if self.settings.value("settings/initial_market") is None:
            self.settings.setValue("settings/initial_market", "BTC/USDT")

    # ─── PROPIEDADES ────────────────────────────────────────────────────────────────

    @cached_property
    def settings(self):
        return QSettings("QTradingView", "Settings")

    @cached_property
    def window(self):
        return MainWindow(self)

    @cached_property
    def db(self):
        db = get_db()
        return db

    @cached_property
    def app_language(self):
        language = self.settings.value('settings/language')
        qtrans = QTranslator()
        qtrans.load(language, AppUtil.get_i18n_dir())
        return qtrans

    @cached_property
    def system_language(self):
        language = self.settings.value('settings/language')
        qtrans = QTranslator()
        lang = f"qtbase_{language}"
        qtrans.load(lang, QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        return qtrans

# ────────────────────────────────────────────────────────────────────────────────
