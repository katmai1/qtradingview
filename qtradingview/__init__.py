"""
QTradingView

Usage:
  qtradingview [--debug]
  qtradingview -h | --help
  qtradingview -v | --version


Options:
  -h --help     Show this screen.
  -v --version  Show version.
  --debug       Execute in debug mode.
"""
import os
import sys
import docopt

from .base.context import ContextoApp


def get_version():
    try:
        version = os.popen('ver read').read()
        return version.split(":")[1].strip()
    except Exception as e:
        print("Error reading VERSION file")
        print(e.__str__())
        return "0.0.0_fail"


# ─── MAIN ───────────────────────────────────────────────────────────────────────

def main():
    args = docopt.docopt(__doc__, version=get_version())
    appctx = ContextoApp(args)
    appctx.app.installTranslator(appctx.app_language)
    appctx.app.installTranslator(appctx.system_language)
    exit_code = appctx.run()
    sys.exit(exit_code)
