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
    condition = peewee.IntegerField(choices=CONDITIONS_CHOICES, default=0)
    price = peewee.FloatField(null=True)

# ────────────────────────────────────────────────────────────────────────────────
