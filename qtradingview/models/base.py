import os
from PyQt5.QtCore import QSettings
from peewee import SqliteDatabase, Model

from qtradingview.utils import AppUtil


# genera el objeto db y lo devuelve
def get_db():
    settings = QSettings("QTradingView", "Settings")
    dirname = os.path.dirname(settings.fileName())
    nou_path = os.path.join(dirname, 'database.db')
    db_file_path = AppUtil.get_db_file_path()
    db = SqliteDatabase(nou_path, pragmas={
        'journal_mode': 'wal',
        'cache_size': -1 * 64000,  # 64MB
        'foreign_keys': 1,
        'ignore_check_constraints': 0,
        'synchronous': 0})
    return db


def migrate(db):
    from peewee_migrate import Router
    router = Router(db)
    # Create migration
    router.create('migration_name', auto=True)
    # Run migration/migrations
    router.run('migration_name')
    # Run all unapplied migrations
    router.run()


# ─── CUSTOM MODEL BASE ──────────────────────────────────────────────────────────

class CustomModel(Model):

    class Meta:
        database = get_db()

    @classmethod
    def count_all(cls):
        return cls.select().count()

# ────────────────────────────────────────────────────────────────────────────────
