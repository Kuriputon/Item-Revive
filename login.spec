# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images'),
		    ('fonts', 'fonts'),
		    ('databases', 'databases')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='物品交换平台',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['E:\\python_projects\\normal_projects\\item_exhange\\pythonProject\\images\\configs\\diamond.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='物品交换平台',
)
