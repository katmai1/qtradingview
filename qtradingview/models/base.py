from peewee import SqliteDatabase, Model

from qtradingview.utils import AppUtil


# genera el objeto db y lo devuelve
def get_db():
    db_file_path = AppUtil.get_db_file_path()
    db = SqliteDatabase(db_file_path, pragmas={
        'journal_mode': 'wal',
        'cache_size': -1 * 64000,  # 64MB
        'foreign_keys': 1,
        'ignore_check_constraints': 0,
        'synchronous': 0})
    return db


# ─── CUSTOM MODEL BASE ──────────────────────────────────────────────────────────

class CustomModel(Model):

    class Meta:
        database = get_db()

    @classmethod
    def count_all(cls):
        return cls.select().count()

# ────────────────────────────────────────────────────────────────────────────────
