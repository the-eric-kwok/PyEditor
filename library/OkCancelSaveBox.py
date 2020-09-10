import tkinter as tk
from tkinter.constants import ACTIVE


class OkCancelSaveBox:

    def __init__(self, parent, text="All modifications will be discard", title="Sure?", yes="Quit", no="Back", save="Save", font=("Helvetica", 11)):
        top = self.top = tk.Toplevel(parent)
        self.answer = ""
        top.resizable(False, False)
        top.title(title)
        lbl = tk.Label(top, text=text, wrap=250,
                       font=font)
        lbl.place(relx=.5, rely=.4, anchor='c')
        x, y = parent.winfo_geometry().split("+")[1:]
        x = int(x) + int(parent.winfo_width()/2) - 150
        y = int(y) + int(parent.winfo_height()/2) - 50
        top.geometry('300x100+%s+%s' % (x, y))
        no_button = tk.Button(top, text=no, command=self.onCancel, width=6)
        no_button.place(relx=0.65, rely=0.8, anchor='c')
        no_button.focus_get()
        save_button = tk.Button(
            top, text=save, command=self.onSave, width=6, default="active")
        save_button.place(relx=0.85, rely=0.8, anchor='c')
        top.bind_all("<Return>", lambda e: save_button.invoke())
        yes_button = tk.Button(top, text=yes, command=self.onOk, width=6)
        yes_button.place(relx=0.15, rely=0.8, anchor='c')
        top.protocol('WM_DELETE_WINDOW', self.onCancel)
        top.grab_set()  # 拦截对底下窗口的点击
        top.lift()
        top.attributes('-topmost', True)
        top.focus_force()

    def onOk(self):
        self.answer = "<<Yes>>"
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
        dialog = OkCancelSaveBox(root)
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
