import peewee
from app.models.base import CustomModel
from app.models.markets import Markets


# ─── TRADE MODEL ────────────────────────────────────────────────────────────────


class Alarms(CustomModel):
    CONDITIONS_CHOICES = (
        (0, "Less than"),
        (1, "Great than")
    )
    market = peewee.ForeignKeyField(Markets, backref="alarms")
    description = peewee.CharField(null=True)
    condition = peewee.IntegerField(choices=CONDITIONS_CHOICES, default=0)
    price = peewee.FloatField(null=True)
    autodelete = peewee.BooleanField(null=True)

    @property
    def condition_label(self):
        return dict(self.CONDITIONS_CHOICES)[self.condition]

    @classmethod
    def getAlarmsToTable(cls):
        data = []
        headers = ['id', 'exchange', 'market', 'condition', 'price']
        for t in cls.select():
            data.append([
                t.id, t.market.exchange, t.market.symbol,
                t.condition_label, t.price
            ])
        return data, headers
# ────────────────────────────────────────────────────────────────────────────────
