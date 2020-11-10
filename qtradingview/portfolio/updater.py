import ccxt
from PyQt5 import QtCore
from qtradingview.models.markets import Markets


# class UpdateAllPrices(QtCore.QThread):
    
#     onFinished = QtCore.pyqtSignal()
#     infoEvent = QtCore.pyqtSignal(str)

#     def __init__(self, parent=None):
#         super().__init__(parent=parent)
#         self.exchanges_list = parent.mw.config['exchanges']
    
#     def _load_client(self, exchange):
#         self.exchange = exchange.lower()
#         self.client = getattr(ccxt, self.exchange)()
#         self.client.enableRateLimit = True

#     # consigue los markets
#     def _get_markets_by_exchange(self):
#         try:
#             return self.client.fetch_tickers()
#         except Exception:
#             return []

#     # hace la rutina completa con la bd
#     def _one_exchange(self):
#         prices = self._get_markets_by_exchange()
#         for symbol in prices:
#             item, created = Markets.get_or_create(exchange=self.exchange, symbol=symbol)
#             if created:
#                 item.save()
#             item.update_data(markets[symbol])

#     def run(self):
#         for exchange in self.exchanges_list:
#             self._load_client(exchange)
#             self.infoEvent.emit(f"Updating prices of {self.exchange.title()}")
#             self._one_exchange()
#         self.onFinished.emit()

# ────────────────────────────────────────────────────────────────────────────────
