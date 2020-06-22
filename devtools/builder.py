#!/usr/bin/env python
"""
QTradingView Builder

Usage:
  build.py [--debug] [--force]
  build.py -h | --help

Options:
  -h --help     Show this screen.
  --debug       Execute in debug mode.
  --force       Try build with generic options.
"""
__VERSION__ = 0.9

import sys
import docopt
from time import sleep

from PyInstaller import os, PLATFORM, is_win
import PyInstaller.__main__


class BuilderManager:

    basepath = "."
    opt = []

    def __init__(self, args):
        self.force = args['--force']
        self.debug = args['--debug']
        if self.debug:
            self.opt.append("--log-level=DEBUG")
        #
        self._add_generic_options()

    @property
    def platform(self):
        if is_win:
            return "windows"
        if 'linux' in PLATFORM.lower():
            return "linux"
        return PLATFORM.lower()

    def add_platform(self):
        if self.platform == "linux":
            self._add_linux_options()
        elif self.platform == "windows":
            self.custom_print("Windows can need a SDK package, if build fails, install it and try again.")
            self.custom_print("https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk/")
            self._add_windows_options()
        else:
            sys.exit("Unkwnown platform. You can try with --force option")

    def run(self):
        self.opt.append(self._dirjoin(['apprun.py']))
        print(self.opt)
        PyInstaller.__main__.run(self.opt)

    def custom_print(self, texto, tipo="i", secs=3):
        print(f" [i] {texto}")
        if self.debug:
            secs = 10
        sleep(secs)

    # ─── PRIVATE METHODS ────────────────────────────────────────────────────────────
    def _dirjoin(self, lista_folders):
        return os.path.join(self.basepath, *lista_folders)

    # Generic options
    def _add_generic_options(self):
        self.opt.append('--onefile')
        self.opt.append('--name=qtradingview')
        self.opt.append('--noconfirm')
        self.opt.append('--clean')
        self.opt.append('--noupx')
        self.opt.append(f'--distpath={self._dirjoin(["devtools", "dist"])}')
        self.opt.append(f'--workpath={self._dirjoin(["devtools", "build"])}')
        # self.opt.append(f'--specpath={self._dirjoin(["devtools"])}')

    # Linux options
    def _add_linux_options(self):
        os.system("export PYTHONOPTIMIZE=1")
        os.system(f"find {self.basepath} -name '*.pyc' -type f -delete")
        # self.opt.append('--strip')  # Apply a symbol-table strip to the executable and shared libs (not recommended for Windows)
        self.opt.append('--add-data=README.md:.')

    # Windows options
    def _add_windows_options(self):
        os.system("set PYTHONOPTIMIZE=1")
        os.system('del /s *.pyc')
        self.opt.append('--windowed')
        self.opt.append(f"--icon={self._dirjoin(['icons', 'logo.ico'])}")
        self.opt.append(f'--version={__VERSION__}')
        self.opt.append('--add-data=README.md;.')
        self.opt.append(f'--distpath={self._dirjoin(["devtools", "dist"])}')


# ─── MAIN ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    bl = BuilderManager(args)
    if bl.force:
        bl.custom_print(f"Using forced mode on platform '{bl.platform}'")
        bl.run()
    else:
        bl.custom_print(f"Detected system {bl.platform}. Adding custom options...")
        bl.add_platform()
        bl.run()
