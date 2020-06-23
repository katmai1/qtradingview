import peewee

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

    @classmethod
    def check_symbol_is_margin(cls, symbol, exchange):
        item = cls.get_symbol_by_exchange(symbol, exchange)
        return item.margin

    def update_data(self, data):
        self.limit_min_price = data['limits']['price']['min']
        self.limit_max_price = data['limits']['price']['max']
        self.limit_min_amount = data['limits']['amount']['min']
        self.limit_max_amount = data['limits']['amount']['max']
        self.precision_price = data['precision']['price']
        if data.get("margin"):
            self.margin = data.get("margin")
        if data['info'].get("margin"):
            self.margin = data['info'].get("margin")
        # pprint(data)
        self.actived = data['active']

    def update_prices(self, prices):
        self.ask_price = prices['ask']
        self.bid_price = prices['bid']
        self.last_price = prices['last']
