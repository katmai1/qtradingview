import peewee
import sys
import logging

peewee.logger.setLevel(logging.INFO)
db = peewee.SqliteDatabase('database.db')

# ─── CONFIGURACIONES ────────────────────────────────────────────────────────────

class Markets(peewee.Model):

    exchange = peewee.CharField(default="")
    symbol = peewee.CharField(default="")
    tag = peewee.CharField(default="all")
    favorite = peewee.BooleanField(default=False)

    class Meta:
        database = db
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
    
# ────────────────────────────────────────────────────────────────────────────────

def crea_tablas():
    try:
        db.connect()
        db.create_tables([Markets])
    except Exception as e:
        print(e)
        print("error!")

#
if __name__ == '__main__':
    crea_tablas()