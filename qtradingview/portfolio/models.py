import peewee
from qtradingview.models.base import CustomModel
from qtradingview.models.markets import Markets


# ─── TRADE MODEL ────────────────────────────────────────────────────────────────

class Trades(CustomModel):

    market = peewee.ForeignKeyField(Markets, backref="trades")
    open_price = peewee.FloatField()
    close_price = peewee.FloatField(null=True)
    position = peewee.CharField(max_length=5)
    amount = peewee.FloatField()

    @classmethod
    def get_by_id(cls, id):
        return cls.get(cls.id == id)

    @classmethod
    def get_all(cls):
        return cls.select()
    
    @classmethod
    def getOpenTradesDataAndHeader(cls):
        data = []
        headers = [
            'ID', 'Exchange', 'Market', 'PosType', 'OpenPrice',
            'Amount', 'LastPrice', 'LastUpdate', 'Profit100', 'Profit'
        ]
        for t in cls.select().where(cls.close_price.is_null(True)):
            data.append([
                t.id, t.market.exchange, t.market.symbol, t.position,
                t.open_price, t.amount, t.market.last_price, t.market.since_update,
                t.profit100, t.profit
            ])
        return data, headers
    
    @classmethod
    def getClosedTradesDataAndHeader(cls):
        data = []
        headers = [
            'ID', 'Exchange', 'Market', 'PosType', 'OpenPrice',
            'Amount', 'ClosePrice', 'Profit100', 'Profit'
        ]
        for t in cls.select().where(cls.close_price.is_null(False)):
            data.append([
                t.id, t.market.exchange, t.market.symbol, t.position,
                t.open_price, t.amount, t.close_price,
                t.profit100, t.profit
            ])
        return data, headers
    
    @property
    def isClosed(self):
        if self.close_price is not None:
            return True
        return False

    def getClosePrice(self):
        if self.isClosed:
            return self.close_price
        return self.market.last_price

    @property
    def profit(self):
        close_price = self.getClosePrice()
        if close_price is not None:
            close_total = close_price * self.amount
            open_total = self.open_price * self.amount
            if self.position == "long":
                return close_total - open_total
            if self.position == "short":
                return open_total - close_total
        return None

    @property
    def profit100(self):
        close_price = self.getClosePrice()
        if close_price is not None:
            if self.position == "long":
                return ((close_price - self.open_price) / self.open_price) * 100
            if self.position == "short":
                return ((self.open_price - close_price) / close_price) * 100
        return None

# ────────────────────────────────────────────────────────────────────────────────
