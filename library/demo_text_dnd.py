import tkinter as tk
import TkinterDnD2.TkinterDnD as tkdnd


def drop(event):
    print("x: %d" % event.x_root, "y: %d" %
          event.y_root, "text:'%s'" % event.data)
    text.insert("@%d,%d" % (event.x_root, event.y_root), event.data)
    # You should be able to use "@60,306" as the first parameter
    # to .insert() to directly place the text at the drop location.


root = tkdnd.Tk()
text = tk.Text(root, width=50, height=30)
text.pack()
text.drop_target_register("DND_Text")
text.dnd_bind('<<Drop>>', drop)
root.mainloop()
