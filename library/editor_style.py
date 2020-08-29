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
    key_binding = {
        "new": "<Meta_L><N>",
        "open": "<Meta_L><O>",
        "save": "<Meta_L><S>",
        "save_as": "<Shift><Meta_L><S>",
        "exit": "<Meta_L><W>",
        "undo": "<Meta_L><Z>",
        "redo": "<Shift><Meta_L><Z>",
        "cut": "<Meta_L><X>",
        "copy": "<Meta_L><C>",
        "paste": "<Meta_L><V>",
        "find": "<Meta_L><F>",
        "select_all": "<Meta_L><A>"
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
        "new": "<Control-N>",
        "open": "<Control-O>",
        "save": "<Control-S>",
        "save_as": "<Shift-Control-S>",
        "exit": "<Control-W>",
        "undo": "<Control-Z>",
        "redo": "<Shift-Control-Z>",
        "cut": "<Control-X>",
        "copy": "<Control-C>",
        "paste": "<Control-V>",
        "find": "<Control-F>",
        "select_all": "<Control-A>"
    }
