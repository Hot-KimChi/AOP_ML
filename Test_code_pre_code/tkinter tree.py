import tkinter as tk
from tkinter import ttk

class MyTreeview1(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

    def message_input(self, msg):
        print(msg)
        return

class MyTreeview2(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind("<Double-1>", lambda e:self.notify_tv1('hello from 2'))

    def notify_tv1(self, msg=None):
        self.master.tree_dialog_tv1.message_input(msg)
        return

class SelectedView(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tree_dialog_tv1 = MyTreeview1(self)
        self.tree_dialog_tv2 = MyTreeview2(self)
        self.tree_dialog_tv1.grid(row=0,column=0)
        self.tree_dialog_tv2.grid(row=0,column=1)

if __name__ == "__main__":
    root = tk.Tk()
    selectview = SelectedView(root)
    selectview.pack(fill=tk.BOTH, expand=True)
    root.mainloop()