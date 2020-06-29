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

# ────────────────────────────────────────────────────────────────────────────────
