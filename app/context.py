import os
import shutil
import sys

from signal import signal, SIGINT, SIG_DFL
from cached_property import cached_property

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLibraryInfo, QTranslator, QSettings

from app.utils import AppUtil
from app.models.base import get_db, migrate

from app.models.markets import Markets
from app.portfolio.models import Trades
from app.alarms.models import Alarms

from app.base.mainwindow import MainWindow


# ─── CONTEXTO APP ───────────────────────────────────────────────────────────────

class ContextoApp:

    def __init__(self, args):
        self.app = QApplication([])
        self.debug = args['--debug']
        signal(SIGINT, SIG_DFL)
        self.args = args
        # # disable qt logging if not debug mode
        # if not self.debug:
        #     os.system("export QT_LOGGING_RULES='*=false'")
        #     os.environ['QT_LOGGING_RULES'] = '*=false'
        #
        AppUtil.create_app_dir()
        # AppUtil.create_default_config()
        self.check_db()
        self.setDefaultConfig()

    def run(self):
        self.window.show()
        return self.app.exec_()

    def tr(self, context, message):
        return self.app.translate(context, message)

    def check_db(self):
        """ Main method to checks related with database. """
        # delete database file if is required by user
        if self.args['--deletedb']:
            self.deleteDatabaseFile()
        # update db tables if is required by user
        if self.args['--updatedb']:
            self.createTablesDB()
        # check if db file exists
        if not AppUtil.existsFileDB():
            self.createTablesDB()
        # check if all tables are created
        if not self.checkTablesExists():
            self.createTablesDB()

    def deleteDatabaseFile(self):
        if AppUtil.existsFileDB():
            os.remove(AppUtil.get_db_file_path())
        if not AppUtil.isPyinstaller():
            shutil.rmtree('migrations', ignore_errors=True)
        sys.exit("Execute again")

    def createTablesDB(self):
        """ Creating or updating database tables. """
        if AppUtil.isPyinstaller():
            self.db.create_tables([Markets, Trades, Alarms])
        else:
            migrate(self.db)
        sys.exit("Execute again")

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
