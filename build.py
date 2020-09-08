#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fileinput import filename
import os
from sys import platform

if __name__ == "__main__":
    if platform == "darwin":
        print("请输入版本号: ", end="")
        version = input()
        os.system("python3 ./library/setup.py py2app")
        os.system("cp -r -v ./img ./dist/PyEditor.app/Contents/Resources/")
        with open("./dist/PyEditor.app/Contents/Info.plist", "r") as f:
            string = f.read()
        with open("./dist/PyEditor.app/Contents/Info.plist", "w") as f:
            string = string.replace("0.0.0", version)
            string = string.replace(
                "org.pythonmac.unspecified", "space.erickwok")
            f.write(string)

    elif platform == "win32":
        command = 'pyinstaller -w --icon="Icon.ico" '
        for (dirpath, dirnames, filenames) in os.walk("img"):
            for file in filenames:
                command += '--add-binary="img\%s;img" ' % file
        command += 'PyEditor.pyw'
        os.system(command)

    else:
        print("""
        Platform not implemented! Please run
            python3 PyEditor.pyw
        """)
