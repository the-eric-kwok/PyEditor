import tkinter as tk
import tkinter.font as tkFont


class FontPanel:
    font_family = "Helvetica"
    font_size = 12

    def __init__(self, parent) -> None:
        top = self.top = tk.Toplevel(parent)
        top.resizable(False, False)
        #top.geometry("200x300+%d+%d" % (500, 500))
        # 创建一个自定义字体以便等会儿更新示例文本
        self.custom_font = tkFont.Font(
            family=self.font_family, size=self.font_size)
        self.font_list = list(tkFont.families(parent))

        # 创建字体选择器区
        box_frame = tk.Frame(top)
        box_frame.pack()
        # 字体选择器
        font_selector = tk.Frame(box_frame)
        font_selector.pack(side="left", fill='y')
        label = tk.Label(font_selector, text="字体")
        label.pack()
        frame = tk.Frame(font_selector)
        frame.pack()
        font_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.font_box = tk.Listbox(
            frame, yscrollcommand=font_scrollbar.set)
        self.font_box.pack(side="left")
        # 将选择操作绑定到 onSelect 方法
        self.font_box.bind('<<ListboxSelect>>', self.onSelect)
        font_scrollbar.config(command=self.font_box.yview)
        font_scrollbar.pack(side="left", fill="y")
        for item in self.font_list:
            # 插入tkinter支持的字体列表
            self.font_box.insert(tk.END, item)

        # 字号选择器
        fontsize_selector = tk.Frame(box_frame)
        fontsize_selector.pack(side="left", fill='y')
        label = tk.Label(fontsize_selector, text="字号")
        label.pack()
        frame = tk.Frame(fontsize_selector)
        frame.pack()
        fontsize_scrollbar = tk.Scrollbar(
            frame, orient=tk.VERTICAL)
        self.fontsize_box = tk.Listbox(
            frame, yscrollcommand=fontsize_scrollbar.set, width=10)
        self.fontsize_box.pack(side="left")
        # 将选择操作绑定到 onSelect 方法
        self.fontsize_box.bind("<<ListboxSelect>>", self.onSelect)
        fontsize_scrollbar.config(command=self.fontsize_box.yview)
        fontsize_scrollbar.pack(side="left", fill="y")
        for item in range(8, 32):
            self.fontsize_box.insert(tk.END, item)

        # TODO 字号选择器

        # 创建字体预览区
        text_frame = tk.Frame(top, width=300, height=100)
        text_frame.pack(fill=None, expand=False)
        text_frame.pack_propagate(False)
        self.text_box = tk.Text(text_frame, font=self.custom_font)
        self.text_box.insert(tk.END, "This is a sample text.\n这是一段示例文字")
        self.text_box.pack()

        # 创建按钮区
        button_frame = tk.Frame(top)
        button_frame.pack()
        ok_button = tk.Button(button_frame, text="确定", command=self.onOk)
        ok_button.pack(side="left")
        cancel_button = tk.Button(
            button_frame, text="取消", command=self.onCancel)
        cancel_button.pack(side="left")
        top.grab_set()  # 拦截对底下窗口的点击

    def onSelect(self, arg):
        for item in self.font_box.curselection():
            self.font_family = self.font_box.get(item)
        for item in self.fontsize_box.curselection():
            self.font_size = self.fontsize_box.get(item)
        self.custom_font.configure(
            family=self.font_family, size=self.font_size)

    def onOk(self):
        print("User clicked OK")
        print("Selected font is %s, size %d" %
              (self.font_family, self.font_size))

    def onCancel(self):
        print("User clicked cancel")


if __name__ == "__main__":

    def onClick():
        dialog = FontPanel(root)
        root.wait_window(dialog.top)

    root = tk.Tk()
    button = tk.Button(root, text="ClickMe", command=onClick)
    button.pack()
    root.mainloop()
