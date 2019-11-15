import peewee
import logging
from pathlib import Path
import os
import sys


peewee.logger.setLevel(logging.INFO)
home = str(Path.home()) + "/.qtradingview"
if not os.path.exists(home):
    os.mkdir(home)
db = peewee.SqliteDatabase(f'{home}/database.db')

# ─── CUSTOM MODEL BASE ──────────────────────────────────────────────────────────


class CustomModel(peewee.Model):

    class Meta:
        database = db

    @classmethod
    def count_all(cls):
        return cls.select().count()

# ────────────────────────────────────────────────────────────────────────────────


# ─── MIGRATE ────────────────────────────────────────────────────────────────────


def migrate_tables():
    from peewee_migrate import Router
    router = Router(db)
    # Create migration
    router.create('migration_name', auto=True)
    # Run migration/migrations
    router.run('migration_name')
    # Run all unapplied migrations
    router.run()


#
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "migrate":
            migrate_tables()
    else:
        print("parameter missing")
