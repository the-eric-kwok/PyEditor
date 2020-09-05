#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from sys import platform

if __name__ == "__main__":
    print("请输入版本号: ", end="")
    version = input()
    if platform == "darwin":
        os.system("python3 ./library/setup.py py2app")
        os.system("cp -r -v ./img ./dist/PyEditor.app/Contents/Resources/")
        with open("./dist/PyEditor.app/Contents/Info.plist", "r+") as f:
            string = f.read()
            string = string.replace("0.0.0", version)
            string = string.replace(
                "org.pythonmac.unspecified", "space.erickwok")
            f.write(string)
    elif platform == "win32":
        import pyinstaller.__main__ as PyInst
        version_file = '''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(6, 1, 7601, 17514),
    prodvers=(6, 1, 7601, 17514),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Eric Kwok'),
        StringStruct(u'FileDescription', u'A simple python editor.'),
        StringStruct(u'FileVersion', u'%s'),
        StringStruct(u'InternalName', u'PyEditor'),
        StringStruct(u'LegalCopyright', u'Eric Kwok. All rights reserved.'),
        StringStruct(u'OriginalFilename', u'PyEditor.Exe'),
        StringStruct(u'ProductName', u'PyEditor'),
        StringStruct(u'ProductVersion', u'%s')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
        ''' % version

        with open(".\.version_file", "w") as f:
            f.write(version_file)

        PyInst.run([
            '--name=%s' % "PyEditor",
            '--onefile',
            '--windowed',
            '--add-binary=%s;img' % os.path.join('img', '*.gif'),
            '--icon=%s' % os.path.join('.\Icon.ico'),
            os.path.join('my_package', '__main__.py'),
        ])
    else:
        print("""
        Platform not implemented! Please run
            python3 PyEditor.pyw
        """)
