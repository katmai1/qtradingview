import peewee
# from peewee_migrate import Router
import logging
from pathlib import Path
import os
import sys


peewee.logger.setLevel(logging.INFO)

home_dir = os.path.join(Path.home(), ".qtradingview")
database_file = os.path.join(home_dir, "database.db")

if not os.path.exists(home_dir):
    os.mkdir(home_dir)

db = peewee.SqliteDatabase(database_file, pragmas={
    'journal_mode': 'wal',
    'cache_size': -1 * 64000,  # 64MB
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0})


# ─── CUSTOM MODEL BASE ──────────────────────────────────────────────────────────


class CustomModel(peewee.Model):

    class Meta:
        database = db

    @classmethod
    def count_all(cls):
        return cls.select().count()

# ────────────────────────────────────────────────────────────────────────────────


# # ─── MIGRATE ────────────────────────────────────────────────────────────────────


# def migrate_tables():
#     router = Router(db)
#     # Create migration
#     router.create('migration_name', auto=True)
#     # Run migration/migrations
#     router.run('migration_name')
#     # Run all unapplied migrations
#     router.run()


# #
# if __name__ == '__main__':
#     if len(sys.argv) > 1:
#         if sys.argv[1] == "migrate":
#             migrate_tables()
#     else:
#         print("parameter missing")
