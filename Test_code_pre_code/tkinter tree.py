import tkinter as tk
from tkinter import ttk

class DataTable:
    def __init__(self, df=None, selected_input=None, frame=None):
        self.df = df
        self.selected_input = selected_input
        self.frame = frame
        self.treeline = 20
        self.create_treeview()

    def create_treeview(self):
        self.tree_scroll_y = tk.Scrollbar(self.frame, orient="vertical")
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_scroll_x = tk.Scrollbar(self.frame, orient="horizontal")
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        self.my_tree = ttk.Treeview(self.frame, height=self.treeline, yscrollcommand=self.tree_scroll_y.set,
                                    xscrollcommand=self.tree_scroll_x.set, selectmode="extended")

        self.tree_scroll_y.config(command=self.my_tree.yview)
        self.tree_scroll_x.config(command=self.my_tree.xview)

        self.my_tree["column"] = list(self.df.columns)
        self.my_tree["show"] = "headings"

        for column in self.my_tree["column"]:
            self.my_tree.column(column, width=100, minwidth=100)
            self.my_tree.heading(column, text=column)

        self.my_tree.tag_configure('oddrow', background="lightblue")
        self.my_tree.tag_configure('evenrow', background="white")

        self.my_tree.pack(padx=20, pady=20, side='left')

    def update_treeview(self):
        self.my_tree.delete(*self.my_tree.get_children())

        df_rows = self.df.round(3)
        df_rows = df_rows.to_numpy().tolist()

        count = 0
        for row in df_rows:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
            count += 1


# 샘플 데이터
sample_data = [
    ("John", 30, "Engineer"),
    ("Jane", 28, "Designer"),
    ("Tom", 35, "Manager"),
    # ... 이하 생략 ...
]

# tkinter 창 생성
root = tk.Tk()
root.title("Treeview Update Example")

# 프레임 생성
frame = tk.Frame(root)
frame.pack()

# DataTable 객체 생성
data_table = DataTable(df=sample_data, frame=frame)

# 새로운 데이터로 업데이트하는 버튼 클릭 시 이벤트 처리
def on_update_button_click():
    new_data = [
        ("Alice", 25, "Analyst"),
        ("Bob", 32, "Developer"),
        # ... 이하 생략 ...
    ]
    data_table.df = new_data
    data_table.update_treeview()

update_button = tk.Button(root, text="Update Treeview", command=on_update_button_click)
update_button.pack(pady=5)

root.mainloop()