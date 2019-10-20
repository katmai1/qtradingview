import PyInstaller.__main__


parametros = [
    '--clean',
    '--name=QTradingView',
    '--onefile',
    '--windowed',
    '--icon=ico/logo.png',
    '--specpath=build/spec',
    '--workpath=build/src',
    '--distpath=build/dist',
    'run.py'
]

PyInstaller.__main__.run(parametros)
