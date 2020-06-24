import logging
import ccxt

from PyQt5.QtCore import QThread, pyqtSignal

from app.models.markets import Markets


# ─── MARKETS UPDATER ────────────────────────────────────────────────────────────
# SOLO ACTUALIZARA MAKRETS
class UpdateMarkets(QThread):

    onFinished = pyqtSignal()

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
