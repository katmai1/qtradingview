import logging
import ccxt
from pprint import pprint
import peewee
from db import CustomModel


class Markets(CustomModel):

    exchange = peewee.CharField(null=True)
    symbol = peewee.CharField(null=True)
    tag = peewee.CharField(null=True, default="all")
    favorite = peewee.BooleanField(null=True, default=False)
    #
    limit_min_price = peewee.FloatField(null=True)
    limit_max_price = peewee.FloatField(null=True)
    limit_min_amount = peewee.FloatField(null=True)
    limit_max_amount = peewee.FloatField(null=True)
    limit_min_cost = peewee.FloatField(null=True)
    precision_price = peewee.SmallIntegerField(null=True)
    margin = peewee.BooleanField(null=True, default=False)
    actived = peewee.BooleanField(null=True)
    # prices
    ask_price = peewee.FloatField(null=True)
    bid_price = peewee.FloatField(null=True)
    last_price = peewee.FloatField(null=True)

    class Meta:
        db_table = 'markets'

    def toggle_fav(self):
        self.favorite = not self.favorite
        self.save()

    @classmethod
    def get_all_by_exchange(cls, exchange):
        return cls.select().where(cls.exchange == exchange)

    @classmethod
    def get_symbol_by_exchange(cls, symbol, exchange):
        return cls.get(cls.exchange == exchange, cls.symbol == symbol)

    @classmethod
    def check_symbol_is_fav(cls, symbol, exchange):
        item = cls.get_symbol_by_exchange(symbol, exchange)
        return item.favorite

    def update_data(self, data):
        self.limit_min_price = data['limits']['price']['min']
        self.limit_max_price = data['limits']['price']['max']
        self.limit_min_amount = data['limits']['amount']['min']
        self.limit_max_amount = data['limits']['amount']['max']
        self.limit_min_cost = data['limits']['cost']['min']
        self.precision_price = data['precision']['price']
        self.actived = data['active']

    def update_prices(self, prices):
        self.ask_price = prices['ask']
        self.bid_price = prices['bid']
        self.last_price = prices['last']

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
