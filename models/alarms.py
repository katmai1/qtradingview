import peewee

from models.base import CustomModel
from models.markets import Markets


# ─── ALARMS ─────────────────────────────────────────────────────────────────────
class Alarms(CustomModel):

    market = peewee.ForeignKeyField(Markets, backref="alarms")
    description = peewee.TextField(null=True, default="")
    condition = peewee.SmallIntegerField(null=True, default=0)
    price = peewee.FloatField(null=True)
    autodelete = peewee.BooleanField(default=True)
    enabled = peewee.BooleanField(default=True)

    @classmethod
    def get_by_id(cls, id):
        return cls.get(cls.id == id)

    def condition_text(self):
        if self.condition is None:
            self.condition = 0
            self.save()
        conditions = ['less', 'great']
        return conditions[self.condition]

    def check_condition(self):
        if self.condition == 0:
            return self._check_less_condition(self.market.last_price)
        elif self.condition == 1:
            return self._check_great_condition(self.market.last_price)
        return False

    def _check_less_condition(self, current_price):
        if current_price <= self.price:
            return True
        return False

    def _check_great_condition(self, current_price):
        if current_price >= self.price:
            return True
        return False
