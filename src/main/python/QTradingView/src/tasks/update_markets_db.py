from PyQt5.QtCore import QThread
import ccxt

from src.db import Markets


# ─── MARKETS UPDATER ────────────────────────────────────────────────────────────

class UpdateMarkets_DB(QThread):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
    
    def get_markets_by_exchange(self, exchange):
        ex = getattr(ccxt, exchange)()
        return ex.load_markets()

    def update_one_exchange(self, exchange):
        # self.parent.statusbar.showMessage(f"Actualizando lista de markets de '{exchange.title()}'...")
        markets = self.get_markets_by_exchange(exchange)
        for symbol in markets:
            it, created = Markets.get_or_create(exchange=exchange, symbol=symbol)
            if created:
                it.save()

    def run(self):
        for exchange in self.parent.exchanges:
            self.update_one_exchange(exchange)
        # self.parent.statusbar.showMessage("Lista de markets actualizada", 3000)