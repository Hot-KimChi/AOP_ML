from tkinter.ttk  import *
from tkinter import *

root = Tk()
root.geometry('800x800')
root.bind('<Escape>',  lambda x:root.destroy() )

class Run_item_Tree(Frame):
    def __init__(self, roots):
        Frame.__init__(self, roots)
        t = Treeview(self, selectmode=NONE, height=10)
        self.t = t
        t["columns"] = ("1", "2")
        t['show'] = 'headings'
        t.column("1", width=100, anchor='c')
        t.column("2", width=50, anchor='c')

        t.heading("1", text="Title")
        t.heading("2", text="UL")

        t.pack(fill =BOTH,side =LEFT)

        vsb = Scrollbar(self, orient="vertical", command=t.yview)
        vsb.pack(fill = Y,side = RIGHT)
        self.vsb = vsb
        t.configure(yscrollcommand=vsb.set)
        self.pack()

a = Run_item_Tree(root)
item_num = 4000
for i in range(item_num):
    a.t.insert('',index=END,text = i,values = (i,i+1,i+2,i+4),tags=('pass',))
count = 0
update = True