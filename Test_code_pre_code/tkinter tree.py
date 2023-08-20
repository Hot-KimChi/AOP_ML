import tkinter as tk
from tkinter import ttk

def clear_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)

def create_treeview(parent_frame):
    # 새로운 Treeview 생성
    tree = ttk.Treeview(parent_frame)
    tree["columns"] = ("Name", "Age")
    tree.column("#0", width=0, stretch=tk.NO)  # 숨길 첫 번째 컬럼
    tree.column("Name", anchor=tk.W, width=100)
    tree.column("Age", anchor=tk.W, width=50)
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")

    # Treeview에 데이터 추가 예시
    tree.insert("", tk.END, text="1", values=("Alice", 25))
    tree.insert("", tk.END, text="2", values=("Bob", 30))

    tree.pack(fill=tk.BOTH, expand=True)
    return tree

def clear_and_create_treeview():
    clear_treeview(treeview_frame.tree)
    treeview_frame.tree.destroy()
    treeview_frame.tree = create_treeview(treeview_frame)

class TreeviewFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.tree = create_treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)
        clear_button = tk.Button(self, text="Clear Treeview", command=clear_and_create_treeview)
        clear_button.pack()

root = tk.Tk()
treeview_frame = TreeviewFrame(root)
treeview_frame.pack(fill=tk.BOTH, expand=True)
root.mainloop()
