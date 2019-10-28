import logging
import ccxt

from PyQt5.QtCore import QThread

from db import Markets


# ─── MARKETS UPDATER ────────────────────────────────────────────────────────────

class UpdateMarkets_DB(QThread):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.lista_exchanges = parent.exchanges_enabled
    
    def get_markets_by_exchange(self, exchange):
        ex = getattr(ccxt, exchange)()
        return ex.load_markets()

    def update_one_exchange(self, exchange):
        logging.info(f"Updating available markets in '{exchange.title()}'...")
        markets = self.get_markets_by_exchange(exchange)
        for symbol in markets:
            it, created = Markets.get_or_create(exchange=exchange, symbol=symbol)
            if created:
                it.save()

    def run(self):
        for exchange in self.lista_exchanges:
            self.update_one_exchange(exchange)

# ────────────────────────────────────────────────────────────────────────────────
