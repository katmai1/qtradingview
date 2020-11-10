import peewee
from qtradingview.models.base import CustomModel
from qtradingview.models.markets import Markets


# ─── TRADE MODEL ────────────────────────────────────────────────────────────────


class Alarms(CustomModel):
    CONDITIONS_CHOICES = (
        (0, "Less than"),
        (1, "Great than")
    )
    market = peewee.ForeignKeyField(column_name='market', model=Markets, null=True)
    description = peewee.CharField(null=True)
    condition = peewee.IntegerField(choices=CONDITIONS_CHOICES, default=0)
    price = peewee.FloatField(null=True)
    enabled = peewee.BooleanField(null=True, default=True)
    autodelete = peewee.BooleanField(null=True)

    @classmethod
    def get_all(cls):
        return cls.select()

    @property
    def condition_label(self):
        return dict(self.CONDITIONS_CHOICES)[self.condition]

    @classmethod
    def getAlarmsToTable(cls):
        data = []
        headers = ['id', 'exchange', 'market', 'condition', 'price', 'enabled']
        for t in cls.select():
            data.append([
                t.id, t.market.exchange, t.market.symbol,
                t.condition_label, t.price, t.enabled
            ])
        return data, headers

    @property
    def isComplished(self):
        if self.condition == 0:
            if self.market.last_price < self.price:
                return True
        if self.condition == 1:
            if self.market.last_price > self.price:
                return True
        return False

    def disable(self):
        self.enabled = False
        self.save()

    def enable(self):
        self.enabled = True
        self.save()
# ────────────────────────────────────────────────────────────────────────────────
