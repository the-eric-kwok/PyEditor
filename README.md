# PyEditor
Simple text editor made with python.

## Features
- [x] Basic edit/copy/paste/undo/redo
- [x] Multi-files edit
- [x] Showing line numbers
- [x] Hightlight current line
- [x] Files drag-n-drop
- [ ] Text drag-n-drop
- [ ] Code highlighting
- [ ] Code formatting

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

	This is an optional dependancy for supporting Drag-N-Drop feature. It's a little bit of tricky in the installation. PyEditor can run without it so it's okay to skip this process.

	- Ubuntu / Debian

		This is the most simple way:
		```
		sudo apt-get install tkdnd
		```
	
	- Fedora / RedHat
		This is untested:
		```
		sudo dnf install tkdnd
		```
	
	- Arch Linux
		
		There is an AUR called tkdnd, see [here](https://aur.archlinux.org/packages/tkdnd/). But this is untested, you need to find out yourself.
		
		For AUR install guide, see [here](https://wiki.archlinux.org/index.php/Arch_User_Repository_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)#%E5%AE%89%E8%A3%85%E8%BD%AF%E4%BB%B6%E5%8C%85)

	- Windows & MacOS

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
			Simply put tkdnd folder under `/Library/Tcl`. If your system don't have that folder, just make a new one. 

			On command line it will be
			```
			cd PathToYourTkdnd2.8Folder
			sudo mkdir /Library/Tcl
			sudo cp tkdnd2.8 /Library/Tcl/
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



