# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['scout.py'],
             pathex=['/Users/leif/PycharmProjects/Scout/scout'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='scout',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='scout_logo.png')
app = BUNDLE(exe,
             name='scout.app',
             icon='scout_logo.png',
             bundle_identifier=com.leifadev.scout)
