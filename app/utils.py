import os
import sys
import shutil
import toml
from pathlib import Path


# mandatory to compile with pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# ─── APPUTIL ────────────────────────────────────────────────────────────────────

class AppUtil:

    default_config = """
        language = "es_ES"
        exchanges = [ "Bittrex", "Bitfinex", "Binance", "Poloniex",]
        initial_exchange = "Binance"
        initial_market = "BTC/USDT"
    """

    @classmethod
    def get_home_dir(cls):
        return os.path.join(Path.home(), ".qtradingview")

    @classmethod
    def get_config_file_path(cls):
        return os.path.join(cls.get_home_dir(), "config.toml")

    @classmethod
    def get_db_file_path(cls):
        return os.path.join(cls.get_home_dir(), "database.db")

    @classmethod
    def get_i18n_dir(cls):
        return resource_path(os.path.join("app", "i18n"))

    @classmethod
    def create_home_dir(cls):
        if not os.path.exists(cls.get_home_dir()):
            os.mkdir(cls.get_home_dir())

    @classmethod
    def create_default_config(cls):
        if not os.path.exists(cls.get_config_file_path()):
            config = toml.loads(cls.default_config)
            with open(AppUtil.get_config_file_path(), "w") as f:
                toml.dump(config, f)

# ────────────────────────────────────────────────────────────────────────────────


