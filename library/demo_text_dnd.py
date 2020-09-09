import tkinter as tk
import library.TkinterDnD2.TkinterDnD as tkdnd


def drop(event):
    print("x: %d" % event.x_root, "y: %d" %
          event.y_root, "text:'%s'" % event.data)


root = tkdnd.Tk()
text = tk.Text(root, width=50, height=30)
text.pack()
text.drop_target_register("DND_Text")
text.dnd_bind('<<Drop>>', drop)
root.mainloop()
