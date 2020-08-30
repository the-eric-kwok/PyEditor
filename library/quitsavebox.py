import tkinter as tk


class QuitSaveBox:

    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        self.answer = ""
        top.resizable(False, False)
        lbl = tk.Label(top, text="你确定要退出吗？所有未保存的更改都会丢失")
        lbl.place(relx=.5, rely=.4, anchor='c')
        top.geometry('300x100')
        no_button = tk.Button(top, text='返回', command=self.no)
        no_button.place(relx=0.85, rely=0.85, anchor='c')
        save_button = tk.Button(top, text='保存', command=self.save)
        save_button.place(relx=0.65, rely=0.85, anchor='c')
        yes_button = tk.Button(top, text='退出', command=self.yes)
        yes_button.place(relx=0.15, rely=0.85, anchor='c')
        top.protocol('WM_DELETE_WINDOW', self.no)
        top.bind('<Return>', (lambda e, b=no_button: b.invoke()))
        top.grab_set()

    def yes(self):
        self.answer = "<<Exit>>"
        self.top.destroy()

    def no(self):
        self.answer = "<<Back>>"
        self.top.destroy()

    def save(self):
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
