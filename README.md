# PyEditor
Simple text editor made with python

## Run
Run in terminal
```
python3 editor.pyw
```
## Build
- ### On macOS
    
   **Dependency**
   
   1. py2app
   
      Install by `pip3 install py2app`
   
   then run
   ```
   python3 mac_build.py
   ```
    
- ### On Windows
   **Dependency**

   1. PyInstaller

      Install by `pip3 install pyinstaller`

   then run in Powershell

   ```
   powershell -NoProfile -F win_build.ps1
   ```
   
   or right click on win_build.ps1 and select "Run in Powershell"

After that, you will find the exe file or app bundle under dist folder