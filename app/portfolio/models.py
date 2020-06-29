import peewee
from app.models.base import CustomModel
from app.models.markets import Markets


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
    
    def profit(self):
        if self.market.last_price is not None:
            close_total = self.market.last_price * self.amount
            open_total = self.open_price * self.amount
            if self.position == "long":
                return close_total - open_total
            if self.position == "short":
                return open_total - close_total
        return None

    def profit100(self):
        if self.market.last_price is not None:
            if self.position == "long":
                return ((self.market.last_price - self.open_price) / self.open_price) * 100
            if self.position == "short":
                return ((self.open_price - self.market.last_price) / self.market.last_price) * 100
        return None

# ────────────────────────────────────────────────────────────────────────────────
