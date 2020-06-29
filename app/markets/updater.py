import logging
import ccxt

from PyQt5 import QtCore
from app.models.markets import Markets


# ─── MARKETS UPDATER ────────────────────────────────────────────────────────────
# SOLO ACTUALIZARA MAKRETS
class UpdateMarkets(QtCore.QThread):

    onFinished = QtCore.pyqtSignal()

    def __init__(self, exchange, parent=None):
        super().__init__(parent=parent)
        #
        self.exchange = exchange.lower()
        self.client = getattr(ccxt, self.exchange)()
        self.client.enableRateLimit = True

    # consigue los markets
    def _get_markets_by_exchange(self):
        try:
            return self.client.load_markets()
        except Exception as e:
            logging.error(e)
            return []

    # consigue los tickers
    # def _get_tickers_by_exchange(self):
    #     try:
    #         return self.client.fetch_tickers()
    #     except Exception as e:
    #         logging.error(e)
    #         return []

    # hace la rutina completa con la bd
    def run(self):
        logging.info(f"Updating markets of {self.exchange.title()}")
        markets = self._get_markets_by_exchange()
        # tickers = self._get_tickers_by_exchange()
        for symbol in markets:
            item, created = Markets.get_or_create(exchange=self.exchange, symbol=symbol)
            if created:
                item.save()
            item.update_data(markets[symbol])
        self.onFinished.emit()

# ────────────────────────────────────────────────────────────────────────────────


class UpdateAllMarkets(QtCore.QThread):
    
    onFinished = QtCore.pyqtSignal()
    infoEvent = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.exchanges_list = parent.mw.config['exchanges']
    
    def _load_client(self, exchange):
        self.exchange = exchange.lower()
        self.client = getattr(ccxt, self.exchange)()
        self.client.enableRateLimit = True

    # consigue los markets
    def _get_markets_by_exchange(self):
        try:
            return self.client.load_markets()
        except Exception as e:
            logging.error(e)
            return []

    def _get_tickers_by_exchange(self):
        try:
            return self.client.fetch_tickers()
        except Exception as e:
            logging.error(e)
            return []
    
    # hace la rutina completa con la bd
    def _one_exchange(self):
        markets = self._get_markets_by_exchange()
        prices = self._get_tickers_by_exchange()
        for symbol in markets:
            item, created = Markets.get_or_create(exchange=self.exchange, symbol=symbol)
            if created:
                item.save()
            item.update_data(markets[symbol])
            item.update_prices(prices[symbol])
            item.save()

    def run(self):
        for exchange in self.exchanges_list:
            self._load_client(exchange)
            self.infoEvent.emit(f"Updating markets of {self.exchange.title()}")
            self._one_exchange()
        self.onFinished.emit()
