"""
 py2app/py2exe build script for MyApplication.

 Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage (Mac OS X):
     python setup.py py2app

 Usage (Windows):
     python setup.py py2exe
"""

from setuptools import setup
import sys
import ez_setup
ez_setup.use_setuptools()

APP = ['PyEditor.pyw']
DATA_FILES = ['PyEditor.pyw']
OPTIONS = {
    "iconfile": "Icon.icns"
}

if sys.platform == 'darwin':
    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app'],
    )
elif sys.platform == 'win32':
    setup(
        app=APP,
        setup_requires=['py2exe'],
        options={'py2exe': OPTIONS}
    )
else:
    setup(
        scripts=APP
    )
