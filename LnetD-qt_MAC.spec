# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['lnetd_qt.py'],
             pathex=['/Users/catalin.petrescu/Desktop/LnetD-BUILD'],
             binaries=[],
             datas=[('./config.ini','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += Tree('./theme', prefix='theme')
a.datas += Tree('./icons', prefix='icons')
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='LnetD-qt',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='LnetD-qt')
app = BUNDLE(coll,
             name='LnetD-qt.app',
             icon=None,
             bundle_identifier=None,
             info_plist={
               'NSHighResolutionCapable': 'True'
             })
