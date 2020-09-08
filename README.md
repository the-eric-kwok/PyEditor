# PyEditor
Simple text editor made with python.

## Run
**Dependency**
1. Tkinter

	- Windows

		This is embedded in python3 which is downloaded from [here](https://www.python.org/downloads/)
		
	- MacOS	

		The default version of python3 do not contain tkinter. Download and install a new one from [here](https://www.python.org/downloads/)
	
	- Debian Linux / Ubuntu
		Run this command in terminal
		```
		sudo apt-get install python3-tk
		```
		and there you go!

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

4. tkdnd (Optional)

	This is an optional dependancy for supporting Drag-N-Drop feature. It's a little bit of tricky in the installation.

    Download tkdnd2.8 from [here](https://sourceforge.net/projects/tkdnd/), make sure you are downloading the right arch. For example, if you are using Python 64-bit on Windows, you should download the Windows 64-bit version.

    **How to check my python version?**

        In your terminal, type `python3` and hit enter, you will see:

        ```
        Python 3.8.5 (tags/v3.8.5:580fbb0, Jul 20 2020, 15:57:54) [MSC v.1924 64 bit (AMD64)] on win32
        Type "help", "copyright", "credits" or "license" for more information.
        ```

        In this example, there is a string "64 bit" and "win32", so we can determine that we are on 64-bit python on Windows.

    Then, 

    - On Windows:

        Nevigate to you python installation directory.

        Check `C:\Program Files\Python`, `C:\Program Files (x86)\Python`,  `D:\Program Files\Python` and `D:\Program Files (x86)\Python`

        *Hint: you can use `where.exe python3` to locate your installation directory.*

        For example, my installation directory is `D:\Program Files\Python\Python38\`. Then goto its subfolder `tcl`. Now the full path is `D:\Program Files\Python\Python38\tcl\`.

        Extract tkdnd2.8 which you downloaded in the previous step and put the `tkdnd2.8` folder here.

    - On MacOS:
		Type `which python3` to see where your python lib is. For example, mine is 
		```
		/Library/Frameworks/Python.framework/Versions/3.8/bin/python3
		```

        So open Finder, hit Shift-Command-G combo and enter `/Library/Frameworks/Python.framework/Versions/3.8/`. Be careful, the python path should **NOT** include `bin/python3`. Then hit enter. You will see a folder called `lib`, double click and open it. Here is where you want to copy the tkdnd2.8 folder to.
		
		In this example, the full path of my python lib is `/Library/Frameworks/Python.framework/Versions/3.8/lib`

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


