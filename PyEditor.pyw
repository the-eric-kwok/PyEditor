import os
import json
import getopt
import sys

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button, Style
import tkinter.font as tkFont

import chardet

from library.FontPanel import FontPanel
from library.EditorStyle import *
from library.Tooltip import Tooltip
from library.OkCancelSaveBox import OkCancelSaveBox


class Root(Tk):
    def exit(self):
        # 判断apps中实例是否为0，若为0则退出
        global apps
        if len(apps) < 1:
            self.quit()


class PyEditor(Toplevel):
    icon_res = []
    file_name = None
    full_path = None
    config = {
        "line_num": True,
        "highlight": True,
        "theme": "Default"
    }
    config_file = os.path.join(os.path.curdir, ".config.json")
    pos_x = 0
    pos_y = 0
    encoding = "utf-8"

    def __init__(self, argv, parent):
        super().__init__()
        self.parent = parent
        self.custom_font = tkFont.Font(self, family='TkFixedFont', size=14)

        self._parse_argv_(argv)
        self._read_config_()
        self._set_window_(pos_x=self.pos_x, pos_y=self.pos_y)
        self._create_menu_bar_()
        self._create_shortcut_bar_()
        self._create_body_()
        self._create_right_popup_menu()
        self.change_theme()
        self._update_line_num()

    def destroy(self):
        apps.remove(self)
        super().destroy()

    def _parse_argv_(self, argv):
        '''
        处理参数 - 使用参数方式传递窗口位置信息
        '''
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
        '''
        读取配置文件
        '''
        try:
            with open(self.config_file, "r") as f:
                self.config = json.load(f)
        except IOError:
            # create if config file doesn't exist
            with open(self.config_file, "w") as f:
                json.dump(self.config, f)

    def _write_config_(self):
        '''
        保存配置文件
        '''
        try:
            with open(self.config_file, "w") as f:
                json.dump(self.config, f)
        except:
            pass

    def _set_window_(self, pos_x=0, pos_y=0):
        '''
        设置初始窗口的属性
        '''
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
        self.iconbitmap(resource_path("editor.ico"))
        self.protocol('WM_DELETE_WINDOW', self.close_editor)

    def _create_file_menu_(self, menu_bar):
        '''
        创建文件子菜单
        '''
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(
            label='新建', accelerator=accelerator["new"], command=self.new_file)
        file_menu.add_command(
            label='打开', accelerator=accelerator["open"], command=self.open_file)
        file_menu.add_command(
            label='保存', accelerator=accelerator["save"], command=self.save)
        if sys.platform == "win32":
            file_menu.add_command(
                label='另存为', accelerator=accelerator["save_as"], command=self.save_as)
        else:
            file_menu.add_command(label="另存为", command=self.save_as)

        file_menu.add_separator()
        file_menu.add_command(
            label='退出', accelerator=accelerator["exit"], command=self.close_editor)
        return file_menu

    def _create_edit_menu_(self, menu_bar):
        '''
        创建编辑子菜单
        '''
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(
            label='撤销', accelerator=accelerator["undo"], command=lambda: self.handle_menu_action('撤销'))
        edit_menu.add_command(
            label='恢复', accelerator=accelerator["redo"], command=lambda: self.handle_menu_action('恢复'))
        edit_menu.add_separator()
        edit_menu.add_command(
            label='剪切', accelerator=accelerator["cut"], command=lambda: self.handle_menu_action('剪切'))
        edit_menu.add_command(
            label='复制', accelerator=accelerator["copy"], command=lambda: self.handle_menu_action('复制'))
        edit_menu.add_command(
            label='粘贴', accelerator=accelerator["paste"], command=lambda: self.handle_menu_action('粘贴'))
        edit_menu.add_separator()
        edit_menu.add_command(
            label='查找', accelerator=accelerator["find"], command=self.find_text)
        edit_menu.add_separator()
        edit_menu.add_command(
            label='全选', accelerator=accelerator["select_all"], command=self.select_all)
        return edit_menu

    def _create_view_menu_(self, menu_bar):
        '''
        创建视图子菜单
        '''
        view_menu = Menu(menu_bar, tearoff=0)
        self.is_show_line_num = IntVar()
        self.is_show_line_num.set(int(self.config["line_num"]))
        view_menu.add_checkbutton(
            label='显示行号', variable=self.is_show_line_num, command=self._toggle_line_num)
        self.is_highlight_line = IntVar()
        self.is_highlight_line.set(int(self.config["highlight"]))
        view_menu.add_checkbutton(
            label='高亮当前行', variable=self.is_highlight_line, command=self._toggle_highlight)
        view_menu.add_command(
            label='字体设置', command=self.toggle_font)
        # 在主题菜单中再添加一个子菜单列表
        themes_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_cascade(label='主题', menu=themes_menu)
        self.theme_choice = StringVar()
        self.theme_choice.set(self.config["theme"])
        for k in sorted(theme_color):
            themes_menu.add_radiobutton(
                label=k, variable=self.theme_choice, command=self.toggle_change_theme)
        return view_menu

    def _create_about_menu_(self, menu_bar):
        '''
        创建关于子菜单
        '''
        about_menu = Menu(menu_bar, tearoff=0)
        about_menu.add_command(
            label='关于', command=lambda: self.show_messagebox('关于'))
        about_menu.add_command(
            label='帮助', command=lambda: self.show_messagebox('帮助'))
        return about_menu

    def _create_menu_bar_(self):
        '''
        创建整个菜单栏
        '''
        menu_bar = Menu(self)
        file_menu = self._create_file_menu_(menu_bar)
        menu_bar.add_cascade(label='文件', menu=file_menu)  # 将文件菜单添加到菜单栏
        edit_menu = self._create_edit_menu_(menu_bar)
        menu_bar.add_cascade(label='编辑', menu=edit_menu)  # 将编辑菜单添加到菜单栏
        view_menu = self._create_view_menu_(menu_bar)
        menu_bar.add_cascade(label='视图', menu=view_menu)  # 将视图菜单添加到菜单栏
        about_menu = self._create_about_menu_(menu_bar)
        menu_bar.add_cascade(label='关于', menu=about_menu)  # 将关于菜单添加到菜单栏
        self["menu"] = menu_bar

    def _create_shortcut_bar_(self):
        '''
        创建快捷菜单栏
        '''
        shortcut_bar = Frame(self, height=25, background='#ECECEC')
        shortcut_bar.pack(fill='x')

        for comm, tip in zip(COMMAND, CH_COMM):
            tool_icon = PhotoImage(file=resource_path('%s.gif' % comm))
            tool_btn = Button(shortcut_bar, image=tool_icon,
                              command=self._shortcut_action(comm))
            tool_btn.pack(side='left')
            Tooltip(tool_btn, text=tip)  # 鼠标停留会出现提示信息
            self.icon_res.append(tool_icon)

    def _sync_title_dirty_(self, *event):
        '''
        修改标题，提示需要保存

        实际标记工作交给编辑器控件自动完成
        '''
        if self.content_text.edit_modified():
            if self.file_name:
                self.title("%s* - PyEditor" % self.file_name)
            else:
                self.title("New* - PyEditor")
        else:
            if self.file_name:
                self.title("%s - PyEditor" % self.file_name)
            else:
                self.title("New - PyEditor")

    def _mark_as_clean_(self):
        '''
        修改标题，提示文件未经编辑

        调用Text.edit_modified(False)来标记编辑器为未经编辑
        '''
        if self.file_name:
            self.title("%s - PyEditor" % self.file_name)
        else:
            self.title("New - PyEditor")
        self.content_text.edit_modified(False)

    def _create_body_(self):
        '''
        创建程序主体
        '''

        # TODO 将文本框和行号栏的行高设为一致的，以解决长文本行号错位的问题
        # 创建文本输入框(undo=True启用撤销机制)
        self.content_text = Text(
            self, wrap='word', undo=True, font=self.custom_font, exportselection=False)
        # 创建行号栏 （takefocus=0 屏蔽焦点）
        self.line_number_bar = Text(self, width=3, padx=3, takefocus=0, border=0,
                                    background="#F0E68C", state=DISABLED, font=self.custom_font)
        # 创建滚动条
        self.scroll_bar = Scrollbar(self.content_text)
        self.scroll_bar["command"] = self.__on_scrollbar__
        self.content_text["yscrollcommand"] = self.__on_textscroll__
        self.line_number_bar["yscrollcommand"] = self.__on_textscroll__
        self.scroll_bar.pack(side='right', fill='y')
        self.content_text.pack(side='right', expand='yes', fill='both')

        self.line_number_bar.pack(side='right', fill='y')

        # Binding part
        self.bind(key_binding["new"][0], self.new_file)
        self.bind(key_binding["new"][1], self.new_file)
        self.bind(key_binding["open"][0], self.open_file)
        self.bind(key_binding["open"][1], self.open_file)
        self.bind(key_binding["save"][0], self.save)
        self.bind(key_binding["save"][1], self.save)
        if sys.platform == "win32":
            self.bind(key_binding["save_as"][0], self.save_as)
            self.bind(key_binding["save_as"][1], self.save_as)
        self.bind(key_binding["select_all"][0], self.select_all)
        self.bind(key_binding["select_all"][1], self.select_all)
        self.bind(key_binding["find"][0], self.find_text)
        self.bind(key_binding["find"][1], self.find_text)
        self.bind('<Any-KeyPress>', lambda e: self._update_line_num())
        self.bind("<Button-1>", lambda e: self._update_line_num())
        # TODO 使用 <Any-KeyPress> 更新高亮当前行

        # 将鼠标左键点击绑定为将焦点赋予content_text
        self.content_text.bind("<Button-1>", lambda e: self.grab_focus())
        self.content_text.bind(
            "<<Modified>>", lambda e: self._sync_title_dirty_(e))
        self.bind_all('<KeyPress-F1>', lambda e: self.show_messagebox("帮助"))
        self.content_text.tag_configure('active_line', background='#EEEEE0')
        self.line_number_bar.config(state=NORMAL)
        self.line_number_bar.insert(1.0, "1")
        self.line_number_bar.config(state=DISABLED)

    def __on_scrollbar__(self, *args):
        # 使文本框和行号栏同步滚动的方法
        self.content_text.yview(*args)
        self.line_number_bar.yview(*args)

    def __on_textscroll__(self, *args):
        # 使文本框和行号栏同步滚动的方法
        self.scroll_bar.set(*args)
        self.__on_scrollbar__("moveto", args[0])

    def _create_right_popup_menu(self):
        '''
        鼠标右键弹出菜单
        '''
        popup_menu = Menu(self.content_text, tearoff=0)
        for it1, it2 in zip(CH_COMM[3:8], COMMAND[3:8]):
            popup_menu.add_command(label=it1, compound='left',
                                   command=self._shortcut_action(it2))
        popup_menu.add_separator()
        popup_menu.add_command(label='全选', command=self.select_all)
        if sys.platform == "darwin":
            # macOS 的右键为鼠标第二键
            self.content_text.bind(
                '<Button-2>', lambda event: popup_menu.tk_popup(event.x_root, event.y_root))
        else:
            self.content_text.bind(
                '<Button-3>', lambda event: popup_menu.tk_popup(event.x_root, event.y_root))

    def _update_line_num(self):
        '''
        更新行号
        '''
        # 先获取原文，和 line_num_content 的长度做对比，如果长则相减并追加，短则相减并删除
        row, col = self.content_text.index("end").split('.')
        line_num_content = ""
        for i in range(1, int(row)):
            line_num_content += ('\n' + str(i))
        origin = self.line_number_bar.get(1.0, END)
        diff = len(line_num_content) - len(origin)
        if diff > 0:
            # Append
            self.line_number_bar.config(state=NORMAL)
            self.line_number_bar.insert(END, line_num_content[-diff:])
            self.line_number_bar.config(state=DISABLED)

        elif diff < 0:
            # Substract
            self.line_number_bar.config(state=NORMAL)
            delete = "%s%dc" % (INSERT, diff)
            self.line_number_bar.delete("%s%dc" % (INSERT, diff), END)
            delete = self.line_number_bar.get(1.0, END)
            self.line_number_bar.config(state=DISABLED)

        else:
            # Do nothing
            pass

    def _toggle_line_num(self):
        self.config["show_line_num"] = bool(self.is_show_line_num.get())
        self._write_config_()
        if self.config["show_line_num"]:
            self._update_line_num()
            try:
                # 尝试获取pack信息，获取失败就意味着还没有pack过
                self.line_number_bar.pack_info()
            except TclError as e:
                if "isn't packed" in str(e):
                    self.line_number_bar.pack(side='right')
        else:
            try:
                self.line_number_bar.pack_forget()
            except TclError:
                pass

    def _update_hightlight(self):
        # TODO 将_toggle_hightlight中更新高亮显示的部分放到此处作为调用
        pass

    def _toggle_highlight(self):
        self.config["highlight"] = bool(self.is_highlight_line.get())
        self._write_config_()
        if self.is_highlight_line.get():
            self.content_text.tag_remove("active_line", 1.0, "end")
            self.content_text.tag_add(
                "active_line", "insert linestart", "insert lineend+1c")
            self.content_text.after(200, self._toggle_highlight)
        else:
            self.content_text.tag_remove("active_line", 1.0, "end")

    def _write_to_file(self, file_name):
        try:
            content = self.content_text.get(1.0, 'end')
            b_content = content.encode(self.encoding)
            with open(file_name, 'wb') as f:
                f.write(b_content)
            self.file_name = os.path.basename(file_name)
            self.title("%s - PyEditor" % self.file_name)
        except IOError:
            messagebox.showwarning("保存", "保存失败！")

    def _shortcut_action(self, type):
        '''
        响应快捷菜单
        '''
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

            if type != "copy" and type != "save":
                self._update_line_num()
                if type != "new_file" and type != "open_file":
                    self._sync_title_dirty_()
        return handle

    def toggle_change_theme(self):
        '''
        保存主题并调用更改主题方法
        '''
        self.config["theme"] = self.theme_choice.get()
        self._write_config_()
        self.change_theme()

    def change_theme(self):
        '''
        更改主题
        '''
        selected_theme = self.theme_choice.get()
        try:
            theme = theme_color[selected_theme]
        except KeyError:
            theme = theme_color.get("Default")
            self.config["theme"] = "Default"
            self._write_config_()
        line_num_color = theme[0]
        self.line_number_bar.config(bg=line_num_color)
        fg_color = theme[1]
        bg_color = theme[2]
        self.content_text.config(bg=bg_color, fg=fg_color)

    def toggle_font(self):
        dialog = FontPanel(self)
        self.wait_window(dialog.top)

    def handle_menu_action(self, action_type):
        '''
        处理菜单响应，返回break，使事件不再传递
        '''
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

    def select_all(self, event=None):
        self.content_text.tag_add('sel', '1.0', 'end')
        return "break"

    def new_file(self, event=None):
        self.pos_x += 20
        self.pos_y += 20
        new = PyEditor(['-x', str(self.pos_x), '-y',
                        str(self.pos_y)], self.parent)
        global apps
        apps.append(new)

    def open_file(self, event=None):
        # TODO 若编辑器为脏，则在打开新文件之前询问
        def __opener__():
            input_file = filedialog.askopenfilename(
                filetypes=[("All", "*.*"), ("Text file", "*.txt"), ("Markdown", "*.md"),
                           ("Python code", "*.py"), ("Python code", "*.pyw")],
                title="选择一个文件")
            if input_file:
                self.file_name = os.path.basename(input_file)
                self.full_path = input_file
                self.title("%s - PyEditor" % self.file_name)
                self.content_text.delete(1.0, END)
                with open(input_file, 'rb') as _file:
                    byte = _file.read()
                    result = chardet.detect(byte)
                    text = byte.decode(encoding=result['encoding'])
                    self.content_text.insert(1.0, text)
                    self.encoding = result['encoding']
            self._update_line_num()
            self._mark_as_clean_()

        if self.content_text.edit_modified():
            dialog = OkCancelSaveBox(self, "你确定要打开新文件吗？\n当前文件中所有的修改都将丢失")
            self.wait_window(dialog.top)
            if dialog.get() == "<<Ok>>":
                __opener__()

            elif dialog.get() == "<<Save>>":
                self.save()
        else:
            __opener__()

    def save(self, event=None):
        if self.full_path is None:
            self.save_as()
        else:
            self._write_to_file(self.full_path)
            self._mark_as_clean_()

    def save_as(self, event=None):
        input_file = filedialog.asksaveasfilename(
            filetypes=[("All Files", "*.*"), ("文本文档", "*.txt")]
        )
        if input_file:
            self.file_name = os.path.basename(input_file)
            self.full_path = input_file
            self._write_to_file(self.full_path)
            self._mark_as_clean_()

    def find_text(self, event=None):
        '''
        创建查找对话框
        '''
        search_toplevel = Toplevel(self)
        search_toplevel.title('查找文本')
        search_toplevel.transient(self)  # 总是让搜索框显示在其父窗体之上
        search_toplevel.resizable(False, False)
        Label(search_toplevel, text="查找全部:").grid(
            row=0, column=0, sticky='e')
        search_entry_widget = Entry(search_toplevel, width=25)
        search_entry_widget.grid(
            row=0, column=1, padx=2, pady=2, sticky='we')
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

    def close_editor(self):
        '''
        处理编辑器关闭操作
        '''
        if self.content_text.edit_modified():
            dialog = OkCancelSaveBox(self, "你确定要退出吗？\n所有未保存的更改都会丢失")
            self.wait_window(dialog.top)
            if dialog.get() == "<<Ok>>":
                self.destroy()
            elif dialog.get() == "<<Save>>":
                self.save()
        else:
            self.destroy()
        # 调用根窗口（不可见）中的exit方法，根据实例个数判断是否需要退出
        self.parent.exit()

    def grab_focus(self):
        '''
        强制将焦点指向文本框

        此方法被绑定到编辑器控件的鼠标左键单击事件
        '''
        self.content_text.focus_force()


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = os.path.join(sys._MEIPASS, 'img')
    except Exception:
        base_path = os.path.abspath(os.path.join(".", "img"))
    return os.path.join(base_path, relative_path)


if "__main__" == __name__:
    root = Root()
    root.withdraw()
    apps = []
    app = PyEditor(sys.argv[1:], root)
    apps.append(app)
    app.lift()
    app.attributes('-topmost', True)
    app.after_idle(app.attributes, '-topmost', False)
    app.focus_force()
    app.mainloop()
