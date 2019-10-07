import peewee
import sys

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

# ────────────────────────────────────────────────────────────────────────────────

def crea_tablas():
    try:
        db.connect()
        db.create_tables([Markets])
    except Exception as e:
        print(e)
        print("error!")

try:
    test = Markets.select()
except Exception as e:
    print(e)
    crea_tablas()
    sys.exit()
#
if __name__ == '__main__':
    crea_tablas()