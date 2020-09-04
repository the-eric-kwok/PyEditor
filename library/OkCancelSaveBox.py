import tkinter as tk


class OkCancelSaveBox:

    def __init__(self, parent, text):
        top = self.top = tk.Toplevel(parent)
        self.answer = ""
        top.resizable(False, False)
        lbl = tk.Label(top, text=text)
        lbl.place(relx=.5, rely=.4, anchor='c')
        top.geometry('300x100')
        no_button = tk.Button(top, text='取消', command=self.onCancel)
        no_button.place(relx=0.85, rely=0.8, anchor='c')
        save_button = tk.Button(top, text='保存', command=self.onSave)
        save_button.place(relx=0.65, rely=0.8, anchor='c')
        yes_button = tk.Button(top, text='确定', command=self.onOk)
        yes_button.place(relx=0.15, rely=0.8, anchor='c')
        top.protocol('WM_DELETE_WINDOW', self.onCancel)
        top.bind('<Return>', (lambda e, b=no_button: b.invoke()))
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
        dialog = QuitSaveBox(root)
        root.wait_window(dialog.top)
        print('Username: ', dialog.get())

    root = tk.Tk()
    mainLabel = tk.Label(root, text='Example for pop up input box')
    mainLabel.pack()

    mainButton = tk.Button(root, text='Click me', command=onClick)
    mainButton.pack()

    root.mainloop()
