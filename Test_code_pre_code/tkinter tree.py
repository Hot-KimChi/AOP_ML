from tkinter import *
from tkinter import ttk

root = Tk()
root.minsize(width=600, height=700)
#root.resizable(width=0, height=0)

tree = ttk.Treeview(root, selectmode='browse',height='10')
tree.place(x=330, y=45)

vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.place(x=320, y=45, height=200 + 180)

tree.configure(yscrollcommand=vsb.set)

#frm = Frame(root)
#frm.pack(padx=0, pady=10, anchor='nw')
#frm.pack(side=tk.LEFT,padx=0,pady=10)
#frm.pack(padx=0,pady=10)

tree["columns"] = (1,2)
tree['show'] = 'headings'
tree['height'] = '20'

tree.column(1, width=150, anchor='c')
tree.heading(1, text="Date")
tree.column(2, width=150, anchor='c')
tree.heading(2, text="GT")


def delete_command():
    for col in tree['columns']:
        tree.heading(col, text='')
    tree.delete(*tree.get_children())


b2 = Button(root, text="delete all", width=12, command=delete_command)
b2.place(x=130, y=45)

root.title('New Data')
root.geometry('650x500')
#root.resizable(False,False)
root.mainloop()