#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import FileType
from io import FileIO
import os
import json
from getopt import getopt, GetoptError
from sys import platform
import sys

from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import Scrollbar, Checkbutton, Label, Button
import tkinter.font as tkFont

import chardet

from library.FontPanel import FontPanel
from library.EditorStyle import *
from library.Tooltip import Tooltip
from library.OkCancelSaveBox import OkCancelSaveBox
from library.TextLineNumber import TextLineNumbers


class Root(Tk):
    full_path = None

    def __init__(self, argv):
        self.parse_argv(argv)
        super().__init__()
        self.withdraw()
        self.apps = []
        if self.full_path:
            app = PyEditor(self, ['-f', self.full_path])
        else:
            app = PyEditor(self)
        self.apps.append(app)
        app.lift()
        app.attributes('-topmost', True)
        app.after_idle(app.attributes, '-topmost', False)
        app.focus_force()
        app.mainloop()

    def exit(self):
        # 判断apps中实例是否为0，若为0则退出
        if len(self.apps) < 1:
            self.quit()

    def parse_argv(self, argv):
        if len(argv) < 1:
            pass
        elif "-" not in argv[0]:
            filename = os.path.expanduser(argv[0])
            if not os.path.isabs(filename):
                filename = os.path.abspath(filename)
            if not os.path.exists(filename):
                raise Exception("File not exists!")
            if not os.path.isfile(filename):
                raise Exception("This is not a file!")
            self.full_path = filename
        else:
            try:
                opts, args = getopt(argv, "h")
            except GetoptError:
                return
            for opt_name, opt_value in opts:
                if opt_name == '-h':
                    print("""
PyEditor - A simple editor written in Python
Usage:
    PyEditor [filename]
                    """)
                    exit()
                pass


class PyEditor(Toplevel):
    icon_res = []
    file_name = None
    full_path = None
    config = {
        "line_num": True,
        "highlight": True,
        "theme": "Default",
        "font_family": "TkFixedFont",
        "font_size": 12,
        "wrap": False
    }
    config_file = os.path.join(os.path.curdir, ".PyEditor.json")
    pos_x = 0
    pos_y = 0
    encoding = "utf-8"

    def __init__(self, parent, argv=None):
        super().__init__()
        self.parent = parent

        self._parse_argv_(argv)
        self._read_config_()

        try:
            self.custom_font = tkFont.Font(
                self, family=self.config["font_family"], size=self.config["font_size"])
        except KeyError:
            self.custom_font = tkFont.Font(self, family='TkFixedFont', size=12)

        self._set_window_(pos_x=self.pos_x, pos_y=self.pos_y)
        self._create_menu_bar_()
        self._create_shortcut_bar_()
        self._create_body_()
        self._create_right_popup_menu()
        self.change_theme()
        self._update_highlight()
        self.after(500, self.toggle_line_num)
        self.toggle_wrap()

    def destroy(self):
        self.parent.apps.remove(self)
        super().destroy()

    def _parse_argv_(self, argv):
        '''
        处理参数
        '''
        try:
            opts, args = getopt(argv, "x:y:f:")
        except GetoptError:
            return
        for name, value in opts:
            # 使用参数方式传递窗口位置信息
            if name == '-x':
                self.pos_x = float(value)
            elif name == '-y':
                self.pos_y = float(value)
            elif name == '-f':
                self.full_path = value
                self.file_name = os.path.basename(self.full_path)

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
        if self.file_name:
            self.title(self.file_name)
        else:
            self.title("New - PyEditor")
        scn_width, scn_height = self.maxsize()
        if (pos_x == 0 and pos_y == 0) or (pos_x < 0 or pos_y < 0):
            self.pos_x = (scn_width - 750) / 4
            self.pos_y = (scn_height - 450) / 4
        else:
            self.pos_x = pos_x
            self.pos_y = pos_y
        wm_val = '1050x600+%d+%d' % (self.pos_x, self.pos_y)
        self.geometry(wm_val)
        try:
            self.iconbitmap(resource_path("editor.ico"))
        except:
            import PIL.Image
            import PIL.ImageTk
            icon = PIL.Image.open(resource_path("editor.ico"))
            icon = PIL.ImageTk.PhotoImage(icon)
            self.call('wm', 'iconphoto', self._w, icon)
        self.protocol('WM_DELETE_WINDOW', self.close_editor)
        self.bind(key_binding["close"][0], self.close_editor)
        self.bind(key_binding["close"][1], self.close_editor)

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
        if platform == "win32":
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
        try:
            self.is_show_line_num.set(int(self.config["line_num"]))
        except KeyError:
            self.is_show_line_num.set(1)
        view_menu.add_checkbutton(
            label='显示行号', variable=self.is_show_line_num, command=self.toggle_line_num)

        self.is_highlight_line = IntVar()
        try:
            self.is_highlight_line.set(int(self.config["highlight"]))
        except KeyError:
            self.is_highlight_line.set(1)
        view_menu.add_checkbutton(
            label='高亮当前行', variable=self.is_highlight_line, command=self.toggle_highlight)

        self.is_wrap = IntVar()
        try:
            self.is_wrap.set(int(self.config["wrap"]))
        except KeyError:
            self.is_wrap.set(0)
        view_menu.add_checkbutton(
            label='自动换行', variable=self.is_wrap, command=self.toggle_wrap)

        view_menu.add_command(label='字体设置', command=self.toggle_font)
        # 在主题菜单中再添加一个子菜单列表
        themes_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_cascade(label='主题', menu=themes_menu)
        self.theme_choice = StringVar()
        try:
            self.theme_choice.set(self.config["theme"])
        except KeyError:
            self.theme_choice.set("Default")
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
        # 创建文本输入框(undo=True启用撤销机制，设定最小宽度为1，以免行号栏被推出窗口外)
        self.content_text = Text(
            self, wrap="none", undo=True, width=1, height=1, font=self.custom_font, exportselection=False)
        # 创建行号栏
        self.line_number_bar = TextLineNumbers(
            self, width=30, background='#ECECEC')
        self.line_number_bar.attach(self.content_text)
        # 创建纵向滚动条
        self.y_scroll_bar = Scrollbar(
            self, command=self.content_text.yview)
        self.content_text["yscrollcommand"] = self.y_scroll_bar.set
        # 创建横向滚动条
        self.x_scroll_bar = Scrollbar(
            self, orient='horizontal', command=self.content_text.xview)
        self.content_text["xscrollcommand"] = self.x_scroll_bar.set
        self.y_scroll_bar.pack(side='right', fill='y')
        if not self.is_wrap.get():  # 如果自动换行则不需要显示底部横向滚动条
            self.x_scroll_bar.pack(side="bottom", fill="x")
        self.content_text.pack(side='right', expand=True, fill='both')
        if self.is_show_line_num.get():  # 如果配置中不需要开启行号栏则不显示行号栏
            self.line_number_bar.pack(side='left', fill='y')

        # Binding part
        self.bind(key_binding["new"][0], self.new_file)
        self.bind(key_binding["new"][1], self.new_file)
        self.bind(key_binding["open"][0], self.open_file)
        self.bind(key_binding["open"][1], self.open_file)
        self.bind(key_binding["save"][0], self.save)
        self.bind(key_binding["save"][1], self.save)
        if platform == "win32":
            self.bind(key_binding["save_as"][0], self.save_as)
            self.bind(key_binding["save_as"][1], self.save_as)
        self.bind(key_binding["select_all"][0], self.select_all)
        self.bind(key_binding["select_all"][1], self.select_all)
        self.bind(key_binding["find"][0], self.find_text)
        self.bind(key_binding["find"][1], self.find_text)

        self.bind('<Key>', self._update_line_num)
        self.bind("<Button-1>", self._update_line_num)
        self.bind("<ButtonRelease-1>", self._update_highlight)
        self.y_scroll_bar.bind(
            "<Button-1>", self._update_line_num)
        self.content_text.bind(
            "<MouseWheel>", self._update_line_num)
        self.content_text.bind('<Key>', self._update_highlight)
        self.bind('<Button-1>', self._update_highlight)
        # 将鼠标左键点击绑定为将焦点赋予content_text
        self.content_text.bind("<Button-1>", lambda e: self.grab_focus())
        self.content_text.bind(
            "<<Modified>>", lambda e: self._sync_title_dirty_(e))
        self.bind_all('<KeyPress-F1>', lambda e: self.show_messagebox("帮助"))
        self.content_text.tag_configure('active_line', background='#EEEEE0')
        if self.full_path:
            self.__opener__(self.full_path)

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
        if platform == "darwin":
            # macOS 的右键为鼠标第二键
            self.content_text.bind(
                '<Button-2>', lambda event: popup_menu.tk_popup(event.x_root, event.y_root))
        else:
            self.content_text.bind(
                '<Button-3>', lambda event: popup_menu.tk_popup(event.x_root, event.y_root))

    def _update_line_num(self, event=None):
        '''
        更新行号
        '''

        def onScrollPress(self, *args):
            self.x_scroll_bar.bind("<B1-Motion>", self.line_number_bar.redraw)

        def onPressDelay(self, *args):
            self.after(2, self.line_number_bar.redraw)

        def redraw(self):
            self.line_number_bar.redraw()

        if event == None:
            redraw(self)
        else:
            if str(event.type) == "KeyPress":
                onPressDelay(self)
            elif str(event.type) == "ButtonPress":
                onScrollPress(self)
            elif str(event.type) == "MouseWheel":
                onPressDelay(self)

    def toggle_line_num(self):
        self.content_text.get(1.0, END)
        if self.config["line_num"] != bool(self.is_show_line_num.get()):
            self.config["line_num"] = bool(self.is_show_line_num.get())
            self._write_config_()
        if self.config["line_num"]:
            self._update_line_num()
            # 尝试获取pack信息，获取失败就意味着还没有pack过
            if not self.line_number_bar.winfo_ismapped():
                self.line_number_bar.pack(side='left', fill='y')
        else:
            try:
                self.line_number_bar.pack_forget()
            except TclError:
                pass

    def toggle_highlight(self, event=None):
        self.config["highlight"] = bool(self.is_highlight_line.get())
        self._write_config_()
        self._update_highlight()

    def _update_highlight(self, event=None):
        def __update_highlight__(self):
            if self.is_highlight_line.get():
                self.content_text.tag_remove("active_line", 1.0, "end")
                self.content_text.tag_add(
                    "active_line", "insert linestart", "insert lineend+1c")
                self.content_text.tag_raise("sel")
            else:
                self.content_text.tag_remove("active_line", 1.0, "end")

        if event == None:
            __update_highlight__(self)
        else:
            if str(event.type) == "KeyPress":
                self.after(5, self._update_highlight)
            elif str(event.type) == "ButtonPress":
                __update_highlight__(self)
                self.content_text.bind(
                    "<B1-Motion>", lambda e: __update_highlight__(self))
            else:
                __update_highlight__(self)

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
        fg_color = theme[0]
        bg_color = theme[1]
        self.content_text.config(bg=bg_color, fg=fg_color)

    def toggle_wrap(self):
        if self.is_wrap.get():
            if self.x_scroll_bar.winfo_ismapped():
                self.x_scroll_bar.pack_forget()
            self.config['wrap'] = True
            self.content_text.config(wrap="word")
        else:
            if not self.x_scroll_bar.winfo_ismapped():
                if self.line_number_bar.winfo_ismapped():
                    self.line_number_bar.pack_forget()
                self.content_text.pack_forget()
                self.x_scroll_bar.pack(side="bottom", fill="x")
                self.content_text.pack(side='right', expand='yes', fill='both')
                if self.is_show_line_num.get():
                    self.line_number_bar.pack(side='left', fill='y')
            self.config['wrap'] = False
            self.content_text.config(wrap="none")

        self._update_line_num()
        self._write_config_()

    def toggle_font(self):
        dialog = FontPanel(self)
        self.wait_window(dialog.top)
        self.config["font_family"] = self.custom_font.cget("family")
        self.config["font_size"] = self.custom_font.cget("size")
        self._write_config_()
        self._update_line_num()

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
            messagebox.showinfo("帮助", """
此编辑器支持简单的文本编辑，请在菜单栏中查看主要功能及主要快捷方式
            """, icon='question')
        else:
            messagebox.showinfo("关于", """
PyEditor V1.0

© 2020 郭耀铭 All Rights Reserved.
            """, icon="info")

    def select_all(self, event=None):
        self.content_text.tag_add('sel', '1.0', 'end')
        return "break"

    def new_file(self, event=None):
        self.pos_x += 20
        self.pos_y += 20
        new = PyEditor(self.parent, ['-x', str(self.pos_x), '-y',
                                     str(self.pos_y)])
        self.parent.apps.append(new)

    def __opener__(self, input_file=None):
        def __get_filename__():
            input_file = filedialog.askopenfilename(
                filetypes=[("All", "*.*"), ("Text file", "*.txt"), ("Markdown", "*.md"),
                           ("Python code", "*.py"), ("Python code", "*.pyw")],
                title="选择一个文件")
            return input_file

        if input_file is None:
            input_file = __get_filename__()

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

    def open_file(self, event=None):

        if self.content_text.edit_modified():
            dialog = OkCancelSaveBox(self, "你确定要打开新文件吗？\n当前文件中所有的修改都将丢失")
            self.wait_window(dialog.top)
            if dialog.get() == "<<Ok>>":
                self.__opener__()

            elif dialog.get() == "<<Save>>":
                self.save()
        else:
            self.__opener__()

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

    def close_editor(self, event=None):
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
        base_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "img"))
    return os.path.join(base_path, relative_path)


if "__main__" == __name__:
    root = Root(sys.argv[1:])
