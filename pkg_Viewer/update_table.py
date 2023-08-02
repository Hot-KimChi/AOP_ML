from tkinter import *
from tkinter import ttk


class DataTable:
    def __init__(self, df=None, selected_input=None, frame=None, sel_cnt=0):

        self.df = df
        self.selected_input = selected_input
        self.frame = frame
        self.treeline = 20
        self.sel_cnt = sel_cnt
        # self.my_tree = self                 # Initialize self.my_tree to None


    def update_treeview(self):
        try:
            print(self.sel_cnt)

            # Destroy the previous tree and scrollbars, if any
            if self.sel_cnt == 1:
                pass

            else:
                self.my_tree.destroy()
                self.tree_scroll_y.destroy()
                self.tree_scroll_x.destroy()


            ## tree_table 생성 및 update
            self.tree_scroll_y = Scrollbar(self.frame, orient="vertical")
            self.tree_scroll_y.pack(side=RIGHT, fill=Y)
            self.tree_scroll_x = Scrollbar(self.frame, orient="horizontal")
            self.tree_scroll_x.pack(side=BOTTOM, fill=X)

            self.my_tree = ttk.Treeview(self.frame, height=self.treeline, yscrollcommand=self.tree_scroll_y.set,
                                        xscrollcommand=self.tree_scroll_x.set, selectmode="extended")

            self.tree_scroll_y.config(command=self.my_tree.yview)
            self.tree_scroll_x.config(command=self.my_tree.xview)

            self.my_tree["column"] = list(self.df.columns)
            self.my_tree["show"] = "headings"

            # Loop thru column list for headers
            for column in self.my_tree["column"]:
                self.my_tree.column(column, width=90, minwidth=90)
                self.my_tree.heading(column, text=column)

            self.my_tree.tag_configure('oddrow', background="lightblue")
            self.my_tree.tag_configure('evenrow', background="white")

            ## event update시, func_click_item 수행.
            # self.my_tree.bind('<ButtonRelease-1>', self.click_item)


            self.my_tree.pack(padx=20, pady=20, side='left')


            # Put data in treeview
            df_rows = self.df.round(3)
            df_rows = df_rows.to_numpy().tolist()

            # Add new data to treeview
            count = 0
            for row in df_rows:
                if count % 2 == 0:
                    self.my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('evenrow',))
                else:
                    self.my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
                count += 1

            return self.my_tree

        except:
            print("Error: tree_update")
