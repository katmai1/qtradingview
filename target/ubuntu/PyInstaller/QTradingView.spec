# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/root/QTradingView/src/main/python/QTradingView/main.py'],
             pathex=['/root/QTradingView/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/root/QTradingView/venv/lib/python3.6/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/root/QTradingView/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='QTradingView',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               upx_exclude=[],
               name='QTradingView')
