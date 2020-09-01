import tkinter as tk
import tkinter as tk
from tkinter import Button, Label
import tkinter
from tkinter.constants import RIGHT, SINGLE
import tkinter.font as tkFont
from typing import Text


class FontPanel:
    def __init__(self, parent) -> None:
        top = self.top = tk.Toplevel(parent)
        top.resizable(False, False)
        self.font_list = list(tkFont.families(parent))
        scrollbar = tk.Scrollbar(top, orient=tk.VERTICAL)
        self.font_box = tk.Listbox(
            top, selectmode=SINGLE, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.font_box.yview)
        scrollbar.pack(side=RIGHT, fill="y")
        self.font_box.pack()
        for item in self.font_list:
            label = tk.Label(top, text=item, font=(item, 16))
            label.bind("<Double-Button-1>", self.onOk)
            # TODO: Change item to a Listbox of Label
            self.font_box.insert(tkinter.END, item)
        frame = tk.Frame(top)
        frame.pack()
        ok_button = tk.Button(frame, text="确定", command=self.onOk)
        ok_button.pack(side="left")
        cancel_button = tk.Button(frame, text="取消", command=self.onCancel)
        cancel_button.pack(side="left")

    def onOk(self):
        print("User clicked OK")
        for item in self.font_box.curselection():
            print("Selected font is %d: %s" % (item, self.font_list[item]))

    def onCancel(self):
        print("User clicked cancel")


if __name__ == "__main__":

    def onClick():
        dialog = FontPanel(root)
        root.wait_window(dialog.top)

    root = tk.Tk()
    button = Button(root, text="ClickMe", command=onClick)
    button.pack()
    root.mainloop()
