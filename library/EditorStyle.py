from sys import platform

COMMAND = ['new_file', 'open_file', 'save',
           'cut', 'copy', 'paste', 'undo', 'redo', 'find_text']
CH_COMM = ['新建文件', '打开文件', '保存文件', '剪切', '复制', '粘贴', '撤销', '重做', '查找']


theme_color = {  # 行号栏     背景色      前景色
    'Default': ['#F0E68C', '#000000', '#FFFFFF'],
    'Greygarious': ['#F0E68C', '#83406A', '#D1D4D1'],
    'Aquamarine': ['#F0E68C', '#5B8340', '#D1E7E0'],
    'Bold Beige': ['#F0E68C', '#4B4620', '#FFF0E1'],
    'Cobalt Blue': ['#F0E68C', '#ffffBB', '#3333aa'],
    'Olive Green': ['#F0E68C', '#D1E7E0', '#5B8340'],
}

NOT_DIRTY = ["F1", "F2", "F3", "F4", "F5", "F6", "F7",
             "F8", "F9", "F10", "F11", "F12", "Escape"]

if platform == "darwin":
    # If platform is macOS
    accelerator = {
        "new": "Command+N",
        "open": "Command+O",
        "save": "Command+S",
        "exit": "Command+W",
        "undo": "Command+Z",
        "redo": "Shift+Command+Z",
        "cut": "Command+X",
        "copy": "Command+C",
        "paste": "Command+V",
        "find": "Command+F",
        "select_all": "Command+A"
    }
    key_binding = {  # TODO: macOS 下按键绑定无效
        "new": ["<Meta_L><n>", "<Meta_L><N>"],
        "open": ["<Meta_L><o>", "<Meta_L><O>"],
        "save": ["<Meta_L><s>", "<Meta_L><S>"],
        "exit": ["<Meta_L><w>", "<Meta_L><W>"],
        "cut": ["<Meta_L><x>", "<Meta_L><X>"],
        "copy": ["<Meta_L><c>", "<Meta_L><C>"],
        "paste": ["<Meta_L><v>", "<Meta_L><V>"],
        "find": ["<Meta_L><f>", "<Meta_L><F>"],
        "select_all": ["<Meta_L><a>", "<Meta_L><A>"]
    }
else:
    accelerator = {
        "new": "Ctrl+N",
        "open": "Ctrl+O",
        "save": "Ctrl+S",
        "save_as": "Shift+Ctrl+S",
        "exit": "Alt+F4",
        "undo": "Ctrl+Z",
        "redo": "Shift+Y",
        "cut": "Ctrl+X",
        "copy": "Ctrl+C",
        "paste": "Ctrl+V",
        "find": "Ctrl+F",
        "select_all": "Ctrl+A"
    }
    key_binding = {
        "new": ["<Control-n>", "<Control-N>"],
        "open": ["<Control-o>", "<Control-O>"],
        "save": ["<Control-s>", "<Control-S>"],
        "save_as": ["<Shift-Control-s>", "<Shift-Control-S>"],
        "exit": ["<Control-w>", "<Control-W>"],
        "undo": ["<Control-z>", "<Control-Z>"],
        "redo": ["<Shift-Control-z>", "<Shift-Control-Z>"],
        "cut": ["<Control-x>", "<Control-X>"],
        "copy": ["<Control-c>", "<Control-C>"],
        "paste": ["<Control-v>", "<Control-V>"],
        "find": ["<Control-f>", "<Control-F>"],
        "select_all": ["<Control-a>", "<Control-A>"]
    }
