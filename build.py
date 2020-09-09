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
        # Build both bundle and standalone
        command = ""
        python_path = os.popen("where.exe python3").read().splitlines()[0]
        if "WindowsApps" in python_path:
            python_path = os.popen("where.exe python").read().splitlines()[0]
            if "WindowsApps" in python_path:
                print("找不到 python 可执行环境，请检查你的 PATH 环境变量")
        print(python_path.replace("python.exe", "tcl\\tkdnd2.8"))
        base_command_1 = 'pyinstaller -w --icon="Icon.ico" --noconfirm --add-data "%s;tkdnd2.8" ' % python_path.replace(
            "python.exe", "tcl\\tkdnd2.8")
        base_command_2 = 'pyinstaller -w -F --icon="Icon.ico" --noconfirm --add-data "%s;tkdnd2.8" ' % python_path.replace(
            "python.exe", "tcl\\tkdnd2.8")
        for (dirpath, dirnames, filenames) in os.walk("img"):
            for file in filenames:
                command += '--add-binary="img\%s;img" ' % file
        command += 'PyEditor.pyw'
        os.system(base_command_1 + command)
        os.system(base_command_2 + command)

    elif platform == "linux":
        command = ""
        base_command_1 = 'pyinstaller -w --icon="Icon.ico" --hidden-import="PIL._tkinter_finder" --noconfirm '
        base_command_2 = 'pyinstaller -w -F --icon="Icon.ico" --hidden-import="PIL._tkinter_finder" --path="dist/standalone" --noconfirm '
        for (dirpath, dirnames, filenames) in os.walk("img"):
            for file in filenames:
                command += '--add-binary="img/%s:img" ' % file
        command += 'PyEditor.pyw'
        os.system(base_command_1 + command)
        if os.path.exists("dist/PyEditor"):
            if os.path.exists("dist/PyEditor.bundle"):
                os.system("rm -rf dist/PyEditor.bundle")
            os.system("mv dist/PyEditor dist/PyEditor.bundle")
        os.system(base_command_2 + command)

    else:
        print("""
        Platform not implemented! Please run
            python3 PyEditor.pyw
        """)

