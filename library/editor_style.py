from platform import system

ICONS = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste',
         'undo', 'redo', 'find_text']
TIPS = ['新建文件', '打开文件', '保存文件', '剪切', '复制', '粘贴', '撤销', '重做', '查找']


theme_color = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}

if system() == "Darwin":
    # If platform is macOS
    accelerator = {
        "new": "Command+N",
        "open": "Command+O",
        "save": "Command+S",
        "save_as": "Shift+Command+S",
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
        "new": ["<Meta-n>", "<Meta-N>"],
        "open": ["<Meta-o>", "<Meta-O>"],
        "save": ["<Meta-s>", "<Meta-S>"],
        "save_as": ["<Shift-Meta-s>", "<Shift-Meta-S>"],
        "exit": ["<Meta-w>", "<Meta-W>"],
        "undo": ["<Meta-z>", "<Meta-Z>"],
        "redo": ["<Shift-Meta-z>", "<Shift-Meta-Z>"],
        "cut": ["<Meta-x>", "<Meta-X>"],
        "copy": ["<Meta-c>", "<Meta-C>"],
        "paste": ["<Meta-v>", "<Meta-V>"],
        "find": ["<Meta-f>", "<Meta-F>"],
        "select_all": ["<Meta-a>", "<Meta-A>"]
    }
else:
    accelerator = {
        "new": "Ctrl+N",
        "open": "Ctrl+O",
        "save": "Ctrl+S",
        "save_as": "Shift+Ctrl+S",
        "exit": "Alt+F4",
        "undo": "Ctrl+Z",
        "redo": "Shift+Ctrl+Z",
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
