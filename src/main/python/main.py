# import logging
import os
import sys

import yaml
import toml
# import peewee
from fbs_runtime.application_context import cached_property
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import QLibraryInfo, QLocale, QTranslator
from PyQt5.QtWidgets import QApplication

from base.mainwindow import MainWindow
from db import db, home

# from pathlib import Path


# ─── APPLICATION CONTEXT ────────────────────────────────────────────────────────

class AppContext(ApplicationContext):

    config_file = f"{home}/config.toml"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not os.path.isfile(self.config_file):
            os.system(f"cp default_config.toml {self.config_file}")

    def run(self):
        self.window.showMaximized()
        return self.app.exec_()

    def tr(self, context, message):
        return self.app.translate(context, message)

    # ─── PROPERTIES ─────────────────────────────────────────────────────────────────
    @cached_property
    def window(self):
        return MainWindow(self)

    @cached_property
    def config(self):
        # with open(self.config_file) as file:
        #     config = yaml.full_load(file)
        config = toml.load(self.config_file)
        return config

    @cached_property
    def db(self):
        return db

    @cached_property
    def app_language(self):
        qtrans = QTranslator()
        qtrans.load(self.config['language'], "src/main/python/i18n")
        return qtrans

    @cached_property
    def system_language(self):
        qtrans = QTranslator()
        lang = f"qtbase_{self.config['language']}"
        qtrans.load(lang, QLibraryInfo.location(QLibraryInfo.TranslationsPath))
        return qtrans

# ────────────────────────────────────────────────────────────────────────────────


if __name__ == '__main__':
    appctxt = AppContext()
    appctxt.app.installTranslator(appctxt.app_language)
    appctxt.app.installTranslator(appctxt.system_language)
    exit_code = appctxt.run()
    sys.exit(exit_code)
