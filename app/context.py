import os
import shutil
import toml
import sys

from signal import signal, SIGINT, SIG_DFL
from cached_property import cached_property

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLibraryInfo, QTranslator

from app.utils import AppUtil
from app.models.base import get_db, migrate

from app.models.markets import Markets
from app.portfolio.models import Trades

from app.base.mainwindow import MainWindow


# ─── CONTEXTO APP ───────────────────────────────────────────────────────────────

class ContextoApp:

    def __init__(self, args):
        self.app = QApplication([])
        self.debug = args['--debug']
        signal(SIGINT, SIG_DFL)
        self.args = args
        # disable qt logging if not debug mode
        if not self.debug:
            os.system("export QT_LOGGING_RULES='*=false'")
            os.environ['QT_LOGGING_RULES'] = '*=false'
        #
        AppUtil.create_app_dir()
        AppUtil.create_default_config()
        self.check_db()

    def run(self):
        self.window.showMaximized()
        return self.app.exec_()

    def tr(self, context, message):
        """Shortcut to translate function

        Args:

            context (str): Context word
            message (str): Message in english

        Returns:

            str: Translate string
        """
        return self.app.translate(context, message)

    def save_config(self):
        """ Save configuration changes in config file """
        with open(AppUtil.get_config_file_path(), "w") as f:
            toml.dump(self.config, f)

    def check_db(self):
        """ Main method to checks related with database. """
        self.db.close()
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
            self.db.create_tables([Markets, Trades])
        else:
            migrate(self.db)
        self.check_db()

    def checkTablesExists(self):
        """ Returns True if all tables exists """
        if not Markets.table_exists():
            return False
        if not Trades.table_exists():
            return False
        return True

    # ─── PROPIEDADES ────────────────────────────────────────────────────────────────

    @cached_property
    def config(self):
        return toml.load(AppUtil.get_config_file_path())

    @cached_property
    def window(self):
        return MainWindow(self)

    @cached_property
    def db(self):
        db = get_db()
        return db

    @cached_property
    def app_language(self):
        qtrans = QTranslator()
        qtrans.load(self.config['language'], AppUtil.get_i18n_dir())
        return qtrans

    @cached_property
    def system_language(self):
        qtrans = QTranslator()
        lang = f"qtbase_{self.config['language']}"
        qtrans.load(lang, QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        return qtrans

# ────────────────────────────────────────────────────────────────────────────────
