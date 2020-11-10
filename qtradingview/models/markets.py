import peewee
import logging
from datetime import datetime
from .base import CustomModel


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
    actived = peewee.BooleanField(null=True, default=True)
    # prices
    ask_price = peewee.FloatField(null=True)
    bid_price = peewee.FloatField(null=True)
    last_price = peewee.FloatField(null=True)
    date = peewee.DateTimeField(default=datetime.now)

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
        return cls.get(cls.exchange == exchange.lower(), cls.symbol == symbol)

    @classmethod
    def check_symbol_is_fav(cls, symbol, exchange):
        item = cls.get_symbol_by_exchange(symbol, exchange)
        return item.favorite

    @classmethod
    def check_symbol_is_margin(cls, symbol, exchange):
        item = cls.get_symbol_by_exchange(symbol, exchange)
        return item.margin

    def update_data(self, data):
        self.limit_min_price = data['limits']['price']['min']
        self.limit_max_price = data['limits']['price']['max']
        self.limit_min_amount = data['limits']['amount']['min']
        self.limit_max_amount = data['limits']['amount']['max']
        # pprint(data)
        if data.get('active'):
            self.actived = data['active']
        self.margin = self.get_margin(data)

    def get_margin(self, data):
        try:
            if data.get("margin"):
                return data.get("margin")
            if data.get('info'):
                if data['info'].get("margin"):
                    return data['info'].get("margin")
        except Exception as e:
            logging.debug(e)
            return False

    def update_prices(self, prices):
        self.ask_price = prices['ask']
        self.bid_price = prices['bid']
        self.last_price = prices['last']
        self.date = datetime.now()

    @property
    def since_update(self):
        dif = datetime.now() - self.date
        minutes, seconds = divmod(dif.total_seconds(), 60)
        return [int(minutes), int(seconds)]

# ────────────────────────────────────────────────────────────────────────────────
