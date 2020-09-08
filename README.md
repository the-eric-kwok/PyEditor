# PyEditor
Simple text editor made with python.

## Run
**Dependency**
1. Tkinter

   On default this is bundled with python3, but on some Linux distro you need to install it manually by
   
   ```
   sudo apt-get install python3-tk
   ```
   
2. chardet

   Install by 
   ```
   pip3 install chardet
   ```

3. Pillow (Only on Linux)

   Install by 
   ```
   pip3 install Pillow
   sudo apt-get install python3-pil.imagetk
   ```

Then run in terminal
```
python3 editor.pyw
```
## Build
- ### On macOS
  
   **Dependency**
   
   1. py2app

      Will be satisfied automatically, 
      or you can install manually with `pip3 install py2app`
   
   then run
   ```
   python3 build.py
   ```
   
- ### On Windows
   **Dependency**

   1. PyInstaller

      Install by `pip3 install pyinstaller`

   then run

   ```
   python3 build.py
   ```
   
- ### On Linux
   **Dependency**
   
   1. PyInstaller
   
      Install by `pip3 install pyinstaller`
      
   then run
   
   ```
   python3 build.py
   ```


After that, you will find the executable file or app bundle under dist folder.


