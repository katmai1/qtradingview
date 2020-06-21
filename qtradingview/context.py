import os
import toml

from signal import signal, SIGINT, SIG_DFL
from cached_property import cached_property

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QLibraryInfo, QLocale, QTranslator

from .utils import AppUtil
from .models.base import get_db
from .models.markets import Markets
from .base.mainwindow import MainWindow


# ─── CONTEXTO APP ───────────────────────────────────────────────────────────────

class ContextoApp:

    def __init__(self, args):
        self.app = QApplication([])
        self.debug = args['--debug']
        signal(SIGINT, SIG_DFL)
        #
        AppUtil.create_home_dir()
        AppUtil.create_default_config()
        self._check_db_file()

    def run(self):
        self.window.showMaximized()
        return self.app.exec()

    def tr(self, context, message):
        return self.app.translate(context, message)

    def save_config(self):
        with open(AppUtil.get_config_file_path(), "w") as f:
            toml.dump(self.config, f)

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────

    def _check_db_file(self):
        if not os.path.isfile(AppUtil.get_db_file_path()):
            self.db.create_tables([Markets])

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
