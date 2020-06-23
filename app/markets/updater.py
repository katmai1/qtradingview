import logging

import ccxt

from app.models.markets import Markets


# ─── MARKETS UPDATER ────────────────────────────────────────────────────────────

class UpdateMarkets:

    exchange = None

    def _get_markets_by_exchange(self):
        try:
            return self.ex.load_markets()
        except Exception as e:
            logging.error(e)
            return []

    def _get_tickers_by_exchange(self):
        try:
            return self.ex.fetch_tickers()
        except Exception as e:
            logging.error(e)
            return []

    def _update_exchange(self):
        markets = self._get_markets_by_exchange()
        tickers = self._get_tickers_by_exchange()
        for symbol in markets:
            item, created = Markets.get_or_create(exchange=self.exchange, symbol=symbol)
            if created:
                item.save()
            item.update_data(markets[symbol])
            if symbol in tickers:
                item.update_prices(tickers[symbol])
            item.save()

    def _select_exchange(self, exchange):
        self.exchange = exchange.lower()
        self.ex = getattr(ccxt, exchange.lower())()
        self.ex.enableRateLimit = True

    def update_markets(self, exchange):
        logging.info(f"Updating markets of {exchange}")
        self._select_exchange(exchange)
        self._update_exchange()

# ────────────────────────────────────────────────────────────────────────────────
