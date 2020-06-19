import PyInstaller.__main__
import os


PyInstaller.__main__.run([
    '--onefile',
    '--name=qtradingview',
    '--noconfirm',
    '--distpath=./_build/dist',
    '--workpath=./_build/build',
    # '--specpath=./_build',
    '--clean',
    '--windowed',
    '--noupx',
    '--add-data=%s:.' % os.path.join('icons', 'logo.ico'),
    '--icon=%s' % os.path.join('icons', 'logo.ico'),
    os.path.join('app', 'run.py'),
])

#
# mkdir DEBIAN
# mkdir -p usr/local/bin
# mkdir -p usr/share/applications
