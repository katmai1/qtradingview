import logging
import ccxt

from PyQt5 import QtCore
from qtradingview.models.markets import Markets


# ─── MARKETS UPDATER ────────────────────────────────────────────────────────────

class UpdateAllMarkets(QtCore.QThread):

    onFinished = QtCore.pyqtSignal()
    infoEvent = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.first_run = True
        self.exchanges_list = parent.mw.cfg.value('settings/exchanges')

    def _load_client(self, exchange):
        """ Load client for an exchange """
        self.exchange = exchange.lower()
        self.client = getattr(ccxt, self.exchange)()
        self.client.enableRateLimit = True

    def _get_markets_by_exchange(self):
        """ Return all markets of current exchange """
        try:
            return self.client.load_markets()
        except Exception as e:
            logging.error(e)
            return None

    def _get_tickers_by_exchange(self):
        """ Return all prices of current exchange """
        try:
            return self.client.fetch_tickers()
        except Exception as e:
            logging.error(e)
            return None

    def _one_exchange(self):
        """ Run for one exchange """
        if self.first_run:
            self._update_markets_by_exchange()
            self.first_run = False
        self._update_tickers_by_exchange()

    def _update_markets_by_exchange(self):
        """ Update markets of current exchange """
        self.infoEvent.emit(f"Updating markets of {self.exchange.title()}")
        markets = self._get_markets_by_exchange()
        if markets is not None:
            for symbol in markets:
                item, created = Markets.get_or_create(exchange=self.exchange, symbol=symbol)
                item.update_data(markets[symbol])
                item.save()
    
    def _update_tickers_by_exchange(self):
        """ Update prices of current exchange """
        self.infoEvent.emit(f"Updating prices of {self.exchange.title()}")
        prices = self._get_tickers_by_exchange()
        if prices is not None:
            for symbol in prices:
                item, created = Markets.get_or_create(exchange=self.exchange, symbol=symbol)
                item.update_prices(prices[symbol])
                item.save()

    def run(self):
        """ Update all enabled exchange """
        for exchange in self.exchanges_list:
            self._load_client(exchange)
            self._one_exchange()
        self.onFinished.emit()
