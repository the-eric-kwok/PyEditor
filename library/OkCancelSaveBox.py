import tkinter as tk
from tkinter.constants import ACTIVE


class OkCancelSaveBox:

    def __init__(self, parent, text):
        top = self.top = tk.Toplevel(parent)
        self.answer = ""
        top.resizable(False, False)
        lbl = tk.Label(top, text=text)
        lbl.place(relx=.5, rely=.4, anchor='c')
        top.geometry('300x100')
        no_button = tk.Button(top, text='取消', command=self.onCancel, width=6)
        no_button.place(relx=0.15, rely=0.8, anchor='c')
        no_button.focus_get()
        save_button = tk.Button(
            top, text='保存', command=self.onSave, width=6, default="active")
        save_button.place(relx=0.85, rely=0.8, anchor='c')
        yes_button = tk.Button(top, text='确定', command=self.onOk, width=6)
        yes_button.place(relx=0.65, rely=0.8, anchor='c')
        top.protocol('WM_DELETE_WINDOW', self.onCancel)
        top.bind('<Return>', (lambda e, b=save_button: b.invoke()))
        top.grab_set()  # 拦截对底下窗口的点击

    def onOk(self):
        self.answer = "<<Ok>>"
        self.top.destroy()

    def onCancel(self):
        self.answer = "<<Cancel>>"
        self.top.destroy()

    def onSave(self):
        self.answer = "<<Save>>"
        self.top.destroy()

    def get(self):
        return self.answer


if __name__ == '__main__':
    def onClick():
        dialog = OkCancelSaveBox(root, "Hello")
        root.wait_window(dialog.top)
        print('Answer: ', dialog.get())

    root = tk.Tk()
    root.geometry("250x100+600+250")
    mainLabel = tk.Label(root, text='Example for OkCancelSaveBox')
    mainLabel.place(relx=.5, rely=.4, anchor='c')

    mainButton = tk.Button(root, text='Click me',
                           command=onClick, width=8, default="active")
    mainButton.place(relx=.5, rely=.8, anchor='c')

    root.mainloop()
