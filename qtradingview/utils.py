import os
import sys
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
        panel_markets_active = false
        panel_portfolio_active = false
        panel_debug_active = false
    """

    @classmethod
    def get_app_dir(cls):
        """ Return app dir into home folder """
        return os.path.join(Path.home(), ".qtradingview")

    @classmethod
    def get_config_file_path(cls):
        """ Return config file path """
        return os.path.join(cls.get_app_dir(), "config.toml")

    @classmethod
    def get_db_file_path(cls):
        """ Return database file path """
        return os.path.join(cls.get_app_dir(), "database.db")

    @classmethod
    def get_i18n_dir(cls):
        """ Return i18n resource path """
        return resource_path(os.path.join("app", "i18n"))

    @classmethod
    def create_app_dir(cls):
        """ Create app folder if not exists """
        if not os.path.exists(cls.get_app_dir()):
            os.mkdir(cls.get_app_dir())

    @classmethod
    def create_default_config(cls):
        """ Create default config file if not exists """
        if not os.path.exists(cls.get_config_file_path()):
            config = toml.loads(cls.default_config)
            with open(AppUtil.get_config_file_path(), "w") as f:
                toml.dump(config, f)

    @classmethod
    def isPyinstaller(cls):
        try:
            _ = sys._MEIPASS
            return True
        except Exception:
            return False
    
    @classmethod
    def existsFileDB(cls):
        return os.path.isfile(cls.get_db_file_path())

# ────────────────────────────────────────────────────────────────────────────────
