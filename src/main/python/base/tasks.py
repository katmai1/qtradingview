import logging

import ccxt
from PyQt5 import QtCore

from models.markets import Markets


# ─── MARKETS UPDATER ────────────────────────────────────────────────────────────

class UpdateMarkets_DB(QtCore.QThread):

    finishSignal = QtCore.pyqtSignal()
    lista_exchanges = []

    def get_markets_by_exchange(self, exchange):
        try:
            return self.ex.load_markets()
        except Exception as e:
            logging.error(e)
            return []

    def get_tickers_by_exchange(self, exchange):
        try:
            return self.ex.fetch_tickers()
        except Exception as e:
            logging.error(e)
            return []

    def update_one_exchange(self, exchange):
        markets = self.get_markets_by_exchange(exchange)
        tickers = self.get_tickers_by_exchange(exchange)
        for symbol in markets:
            item, created = Markets.get_or_create(exchange=exchange, symbol=symbol)
            if created:
                item.save()
            item.update_data(markets[symbol])
            if symbol in tickers:
                item.update_prices(tickers[symbol])
            # else:
            #     mensaje = QtCore.QCoreApplication.translate(
            #         "base.tasks",
            #         "Precio no encontrado para"
            #     )
            #     logging.error(f"{mensaje} {symbol} ({exchange})")
            item.save()

    def run(self):
        for exchange in self.lista_exchanges:
            self.ex = getattr(ccxt, exchange)()
            self.ex.enableRateLimit = True
            self.update_one_exchange(exchange)
        self.sleep(10)

# ────────────────────────────────────────────────────────────────────────────────
