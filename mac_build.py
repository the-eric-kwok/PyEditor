import os
from sys import platform

if __name__ == "__main__":
    print(platform)
    if platform == "darwin":
        os.system("python3 ./library/setup.py py2app")
        os.system("cp -r -v ./img ./dist/PyEditor.app/Contents/Resources/")
    elif platform == "win32":
        os.system("python3.exe .\\library\\setup.py py2exe")
