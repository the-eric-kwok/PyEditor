import os
from platform import system
import json
import subprocess as sp
import getopt
import sys

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button

from library.tooltip import Tooltip
from library.editor_style import *


class PyEditor(Tk):
    icon_res = []
    file_name = None
    dirty = False  # 标记文件是否修改过，默认为未修改，可直接关闭，不用提示保存
    config = {
        "show_line_num": True,
        "hightlight_current_line": True,
        "theme": "Default"
    }
    config_file = os.path.join(os.path.curdir, ".config.json")
    pos_x = 0
    pos_y = 0

    def __init__(self, argv):
        super().__init__()
        self._parse_argv_(argv)
        self._read_config_()
        self._set_window_(pos_x=self.pos_x, pos_y=self.pos_y)
        self._create_menu_bar_()
        self._create_shortcut_bar_()
        self._create_body_()
        self._create_right_popup_menu()

    def _parse_argv_(self, argv):
        # 使用参数方式传递位置信息
        try:
            opts, args = getopt.getopt(argv, "x:y:")
        except getopt.GetoptError:
            return
        for opt, arg in opts:
            if opt == '-x':
                self.pos_x = float(arg)
            elif opt == '-y':
                self.pos_y = float(arg)

    def _read_config_(self):
        try:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        except IOError:
            # create if config file doesn't exist
            with open(self.config_file, "w") as f:
                json.dump(self.config, f)

    def _write_config_(self):
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f)
        except:
            pass

    # 设置初始窗口的属性
    def _set_window_(self, pos_x=0, pos_y=0):
        self.title("New - PyEditor")
        scn_width, scn_height = self.maxsize()
        if (pos_x == 0 and pos_y == 0) or (pos_x < 0 or pos_y < 0):
            self.pos_x = (scn_width - 750) / 4
            self.pos_y = (scn_height - 450) / 4
        else:
            self.pos_x = pos_x
            self.pos_y = pos_y
        wm_val = '750x450+%d+%d' % (self.pos_x, self.pos_y)
        self.geometry(wm_val)
        self.iconbitmap("img/editor.ico")
        self.protocol('WM_DELETE_WINDOW', self.exit_editor)

    # 创建整个菜单栏
    def _create_menu_bar_(self):
        menu_bar = Menu(self)
        # 创建文件的联级菜单
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label='新建', accelerator=accelerator["new"], command=self.new_file)
        file_menu.add_command(
            label='打开', accelerator=accelerator["open"], command=self.open_file)
        file_menu.add_command(
            label='保存', accelerator=accelerator["save"], command=self.save)
        file_menu.add_command(
            label='另存为', accelerator=accelerator["save_as"], command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(
            label='退出', accelerator=accelerator["exit"], command=self.exit_editor)

        # 在菜单栏上添加菜单标签，并将该标签与相应的联级菜单关联起来
        menu_bar.add_cascade(label='文件', menu=file_menu)

        # 创建编辑的联级菜单
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label='撤销', accelerator=accelerator["undo"],
                              command=lambda: self.handle_menu_action('撤销'))
        edit_menu.add_command(label='恢复', accelerator=accelerator["redo"],
                              command=lambda: self.handle_menu_action('恢复'))
        edit_menu.add_separator()
        edit_menu.add_command(label='剪切', accelerator=accelerator["cut"],
                              command=lambda: self.handle_menu_action('剪切'))
        edit_menu.add_command(label='复制', accelerator=accelerator["copy"],
                              command=lambda: self.handle_menu_action('复制'))
        edit_menu.add_command(label='粘贴', accelerator=accelerator["paste"],
                              command=lambda: self.handle_menu_action('粘贴'))
        edit_menu.add_separator()
        edit_menu.add_command(
            label='查找', accelerator=accelerator["find"], command=self.find_text)
        edit_menu.add_separator()
        edit_menu.add_command(
            label='全选', accelerator=accelerator["select_all"], command=self.select_all)
        menu_bar.add_cascade(label='编辑', menu=edit_menu)

        # 视图菜单
        view_menu = Menu(menu_bar, tearoff=0)
        self.is_show_line_num = IntVar()
        self.is_show_line_num.set(1)
        view_menu.add_checkbutton(label='显示行号', variable=self.is_show_line_num,
                                  command=self._update_line_num)

        self.is_highlight_line = IntVar()
        view_menu.add_checkbutton(
            label='高亮当前行', variable=self.is_highlight_line, command=self._toggle_highlight)

        # 在主题菜单中再添加一个子菜单列表
        themes_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_cascade(label='主题', menu=themes_menu)

        self.theme_choice = StringVar()
        self.theme_choice.set(self.config["theme"])
        for k in sorted(theme_color):
            themes_menu.add_radiobutton(label=k, variable=self.theme_choice,
                                        command=self.change_theme)

        menu_bar.add_cascade(label='视图', menu=view_menu)

        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(
            label='关于', command=lambda: self.show_messagebox('关于'))
        about_menu.add_command(
            label='帮助', command=lambda: self.show_messagebox('帮助'))
        menu_bar.add_cascade(label='关于', menu=about_menu)
        self["menu"] = menu_bar

    # 创建快捷菜单栏
    def _create_shortcut_bar_(self):
        shortcut_bar = Frame(self, height=25, background='#ECECEC')
        shortcut_bar.pack(fill='x')

        for icon, tip in zip(ICONS, TIPS):
            tool_icon = PhotoImage(file=os.path.join('img', '%s.gif' % icon))
            tool_btn = Button(shortcut_bar, image=tool_icon,
                              command=self._shortcut_action(icon))
            tool_btn.pack(side='left')
            Tooltip(tool_btn, text=tip)  # 鼠标停留会出现提示信息
            self.icon_res.append(tool_icon)

    # 创建程序主体
    def _create_body_(self):
        # 创建行号栏 （takefocus=0 屏蔽焦点）
        self.line_number_bar = Text(self, width=4, padx=3, takefocus=0, border=0,
                                    background='#F0E68C', state='disabled')
        self.line_number_bar.pack(side='left', fill='y')
        # 创建文本输入框(undo=True启用撤销机制)
        self.content_text = Text(self, wrap='word', undo=True)
        self.content_text.pack(expand='yes', fill='both')
        #self.content_text.bind(key_binding["new"], self.new_file)
        #self.content_text.bind('<Control-n>', self.new_file)
        #self.content_text.bind(key_binding["open"], self.open_file)
        #self.content_text.bind('<Control-o>', self.open_file)
        #self.content_text.bind(key_binding["save"], self.save)
        #self.content_text.bind('<Control-s>', self.save)
        #self.content_text.bind(key_binding["select_all"], self.select_all)
        #self.content_text.bind('<Control-a>', self.select_all)
        #self.content_text.bind('<Control-f>', self.find_text)
        #self.content_text.bind(key_binding["find"], self.find_text)
        self.content_text.bind(
            '<Any-KeyPress>', lambda e: self._update_line_num())
        self.bind_all('<KeyPress-F1>', lambda e: self.show_messagebox("帮助"))
        self.content_text.tag_configure('active_line', background='#EEEEE0')

        # 创建滚动条
        scroll_bar = Scrollbar(self.content_text)
        scroll_bar["command"] = self.content_text.yview
        self.content_text["yscrollcommand"] = scroll_bar.set
        scroll_bar.pack(side='right', fill='y')

    # 鼠标右键弹出菜单
    def _create_right_popup_menu(self):
        popup_menu = Menu(self.content_text, tearoff=0)
        for it1, it2 in zip(TIPS[3:8], ICONS[3:8]):
            popup_menu.add_command(label=it1, compound='left',
                                   command=self._shortcut_action(it2))
        popup_menu.add_separator()
        popup_menu.add_command(label='全选', command=self.select_all)
        if system() == "Darwin":
            self.content_text.bind(
                '<Button-2>', lambda event: popup_menu.tk_popup(event.x_root, event.y_root))
        else:
            self.content_text.bind(
                '<Button-3>', lambda event: popup_menu.tk_popup(event.x_root, event.y_root))

    def _update_line_num(self):
        if self.is_show_line_num.get():
            row, col = self.content_text.index("end").split('.')
            line_num_content = "\n".join([str(i) for i in range(1, int(row))])
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.insert('1.0', line_num_content)
            self.line_number_bar.config(state='disabled')
        else:
            self.line_number_bar.config(state='normal')
            self.line_number_bar.delete('1.0', 'end')
            self.line_number_bar.config(state='disabled')

    def _toggle_highlight(self):
        if self.is_highlight_line.get():
            self.content_text.tag_remove("active_line", 1.0, "end")
            self.content_text.tag_add(
                "active_line", "insert linestart", "insert lineend+1c")
            self.content_text.after(200, self._toggle_highlight)
        else:
            self.content_text.tag_remove("active_line", 1.0, "end")

    def change_theme(self):
        # TODO 更换字体功能
        selected_theme = self.theme_choice.get()
        fg_bg = theme_color.get(selected_theme)
        fg_color, bg_color = fg_bg.split('.')
        self.content_text.config(bg=bg_color, fg=fg_color)

    # 处理菜单响应，返回break，使事件不在传递
    def handle_menu_action(self, action_type):
        if action_type == "撤销":
            self.content_text.event_generate("<<Undo>>")
        elif action_type == "恢复":
            self.content_text.event_generate("<<Redo>>")
        elif action_type == "剪切":
            self.content_text.event_generate("<<Cut>>")
        elif action_type == "复制":
            self.content_text.event_generate("<<Copy>>")
        elif action_type == "粘贴":
            self.content_text.event_generate("<<Paste>>")

        if action_type != "复制":
            self._update_line_num()

        return "break"

    def show_messagebox(self, type):
        if type == "帮助":
            messagebox.showinfo("帮助", "这是帮助文档！", icon='question')
        else:
            messagebox.showinfo("关于", "PyEditor_V0.1")

    # 响应快捷菜单
    def _shortcut_action(self, type):
        def handle():
            if type == "new_file":
                self.new_file()
            elif type == "open_file":
                self.open_file()
            elif type == "save":
                self.save()
            elif type == "cut":
                self.handle_menu_action("剪切")
            elif type == "copy":
                self.handle_menu_action("复制")
            elif type == "paste":
                self.handle_menu_action("粘贴")
            elif type == "undo":
                self.handle_menu_action("撤销")
            elif type == "redo":
                self.handle_menu_action("恢复")
            elif type == "find_text":
                self.find_text()

            # if type != "copy" and type != "save":
            self._update_line_num()

        return handle

    def select_all(self, event=None):
        self.content_text.tag_add('sel', '1.0', 'end')
        return "break"

    def new_file(self, event=None):
        self.pos_x += 20
        self.pos_y += 20
        sp.Popen(["python3", os.path.join(os.getcwd(), "editor.py"),
                  "-x", str(self.pos_x), "-y", str(self.pos_y)])

    def open_file(self, event=None):
        input_file = filedialog.askopenfilename(
            filetypes=[("所有文件", "*.*"), ("文本文档", "*.txt")])
        if input_file:
            self.title("%s - PyEditor" % os.path.basename(input_file))
            self.file_name = input_file
            self.content_text.delete(1.0, END)
            with open(input_file, 'r') as _file:
                self.content_text.insert(1.0, _file.read())

    def save(self, event=None):
        if not self.file_name:
            self.save_as()
        else:
            self._write_to_file(self.file_name)

    def save_as(self, event=None):
        input_file = filedialog.asksaveasfilename(
            filetypes=[("All Files", "*.*"), ("文本文档", "*.txt")])
        if input_file:
            self.file_name = input_file
            self._write_to_file(self.file_name)

    def _write_to_file(self, file_name):
        try:
            content = self.content_text.get(1.0, 'end')
            with open(file_name, 'w') as the_file:
                the_file.write(content)
            self.title("%s - PyEditor" % os.path.basename(file_name))
        except IOError:
            messagebox.showwarning("保存", "保存失败！")

    # 查找对话框
    def find_text(self, event=None):
        search_toplevel = Toplevel(self)
        search_toplevel.title('查找文本')
        search_toplevel.transient(self)  # 总是让搜索框显示在其父窗体之上
        search_toplevel.resizable(False, False)
        Label(search_toplevel, text="查找全部:").grid(row=0, column=0, sticky='e')
        search_entry_widget = Entry(search_toplevel, width=25)
        search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
        search_entry_widget.focus_set()
        ignore_case_value = IntVar()
        Checkbutton(search_toplevel, text='忽略大小写', variable=ignore_case_value).grid(
            row=1, column=1, sticky='e', padx=2, pady=2)

        Button(search_toplevel, text="查找", command=lambda: self.search_result(
            search_entry_widget.get(), ignore_case_value.get(), search_toplevel, search_entry_widget)
        ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)

        def close_search_window():
            self.content_text.tag_remove('match', '1.0', "end")
            search_toplevel.destroy()

        search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
        return "break"

    def search_result(self, key, ignore_case, search_toplevel, search_box):
        self.content_text.tag_remove('match', '1.0', "end")
        matches_found = 0
        if key:
            start_pos = '1.0'
            while True:
                # search返回第一个匹配上的结果的开始索引，返回空则没有匹配的（nocase：忽略大小写）
                start_pos = self.content_text.search(
                    key, start_pos, nocase=ignore_case, stopindex="end")
                if not start_pos:
                    break
                end_pos = '{}+{}c'.format(start_pos, len(key))
                self.content_text.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos
            self.content_text.tag_config(
                'match', foreground='red', background='yellow')
        search_box.focus_set()
        search_toplevel.title('发现%d个匹配的' % matches_found)

    def exit_editor(self):
        if messagebox.askokcancel("退出?", "确定退出吗?"):
            self.destroy()


if "__main__" == __name__:
    app = PyEditor(sys.argv[1:])
    app.lift()
    app.attributes('-topmost', True)
    app.after_idle(app.attributes, '-topmost', False)
    app.focus_force()
    app.mainloop()
