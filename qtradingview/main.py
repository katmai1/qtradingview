"""
QTradingView

Usage:
  qtradingview [--debug]
  qtradingview [--deletedb]
  qtradingview [--updatedb]
  qtradingview -h | --help
  qtradingview -v | --version


Options:
  -h --help     Show this screen.
  -v --version  Show version.
  --debug       Execute in debug mode.
  --updatedb    Update db tables.
  --deletedb    Delete db file.
"""
# export QT_LOGGING_RULES='*=false'
__version__ = '0.17.0'

import sys
import docopt

from qtradingview.context import ContextoApp


def run():
    args = docopt.docopt(__doc__, version=__version__)
    appctx = ContextoApp(args)

    if args['--deletedb']:
        appctx.deleteDatabaseFile()
    appctx.createDB()

    appctx.app.installTranslator(appctx.app_language)
    appctx.app.installTranslator(appctx.system_language)
    exit_code = appctx.run()
    sys.exit(exit_code)


# ─── MAIN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run()
