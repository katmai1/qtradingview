import os
import toml

from signal import signal, SIGINT, SIG_DFL
from cached_property import cached_property

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLibraryInfo, QTranslator

from app.utils import AppUtil
from app.models.base import get_db, migrate
from app.base.mainwindow import MainWindow


# ─── CONTEXTO APP ───────────────────────────────────────────────────────────────

class ContextoApp:

    def __init__(self, args):
        self.app = QApplication([])
        self.debug = args['--debug']
        signal(SIGINT, SIG_DFL)
        self.args = args
        # disable qt logging if not debug mode
        if args['--updatedb']:
            migrate(self.db)
        if not self.debug:
            os.system("export QT_LOGGING_RULES='*=false'")
            os.environ['QT_LOGGING_RULES'] = '*=false'
        #
        if AppUtil.isPyinstaller():
            print("pyinstaller")
        else:
            print("no pyinstaller")
        AppUtil.create_app_dir()
        AppUtil.create_default_config()
        self.check_db_file()

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

    def check_db_file(self):
        """ Check if database file exists and create tables """
        if not os.path.isfile(AppUtil.get_db_file_path()):
            migrate(self.db)

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
