# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller 配置文件
用于打包环比箭头柱状图 PyQt5 应用
"""

import os
import sys

# 获取当前目录
project_dir = os.getcwd()

# 获取Matplotlib路径
import matplotlib
mpl_data_path = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data')

block_cipher = None

a = Analysis(
    ['app_pyqt5.py'],
    pathex=[project_dir],
    binaries=[],
    datas=[
        # 添加 Matplotlib 数据文件
        (mpl_data_path, 'matplotlib/mpl-data'),
    ],
    hiddenimports=[
        # PyQt5 相关
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'PyQt5.sip',
        
        # Matplotlib 相关
        'matplotlib',
        'matplotlib.backends',
        'matplotlib.backends.backend_qt5agg',
        'matplotlib.backends.backend_pdf',
        'matplotlib.figure',
        'matplotlib.pyplot',
        'matplotlib.patches',
        'matplotlib.path',
        
        # 数据处理相关
        'pandas',
        'numpy',
        'openpyxl',
        
        # 其他
        'PIL',
        'pydoc',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的库以减小体积并避免问题
        'tkinter',
        'unittest',
        'nltk',
        'torch',
        'torchvision',
        'torchaudio',
        'skimage',
        'sklearn',
        'cv2',
        'astropy',
        'sympy',
        'notebook',
        'ipython',
        'IPython',
        'jupyter',
        'pytest',
        'scipy',
        'statsmodels',
        'xarray',
        'altair',
        'plotly',
        'bokeh',
        'seaborn',
        'theano',
        'keras',
        'tensorflow',
        'mxnet',
        'caffe',
        'theano',
        'patsy',
        'imageio',
        'PIL._tkinter_finder',
        'pyi_rth_nltk',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='环比箭头柱状图',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # 如果有图标文件，取消下面注释
    # icon='app_icon.ico',
)
