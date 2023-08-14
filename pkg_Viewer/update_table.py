from tkinter import *
from tkinter import ttk


class DataTable:
    def __init__(self, df=None, selected_input=None, frame=None, sel_cnt=0,
                 my_tree=None, tree_scroll_y=None, tree_scroll_x=None):
        super().__init__()
        self.df = df
        self.selected_input = selected_input
        self.frame = frame
        self.treeline = 20
        self.sel_cnt = sel_cnt
        self.my_tree = my_tree
        self.tree_scroll_y = tree_scroll_y
        self.tree_scroll_x = tree_scroll_x


    def click_item(self, event):
        ## multiple selection
        # global str_sel_param
        selectedItem = self.my_tree.selection()

        # 딕셔너리의 값 중에서 제일 앞에 있는 element 값 추출. ex) measSSId 추출.
        # sel_param_click = my_tree.item(selectedItem).get('values')[0]
        sel_param_click = []
        for i in selectedItem:
            sel_param_click.append(self.my_tree.item(i).get('values')[0])
        str_sel_param = '(' + ','.join(str(x) for x in sel_param_click) + ')'
        print(str_sel_param)

        return str_sel_param


    def update_treeview(self):

        # # Destroy the previous tree and scrollbars, if any
        if self.my_tree or self.sel_cnt > 1:
            self.my_tree.destroy()
            self.tree_scroll_y.destroy()
            self.tree_scroll_x.destroy()
            print('삭제')


        # Initialize the my_tree variable
        ## tree_table 생성 및 update
        self.tree_scroll_y = Scrollbar(self.frame, orient="vertical")
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x = Scrollbar(self.frame, orient="horizontal")
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)

        self.my_tree = ttk.Treeview(self.frame, height=self.treeline, yscrollcommand=self.tree_scroll_y.set,
                                    xscrollcommand=self.tree_scroll_x.set, selectmode="extended")

        self.my_tree.pack(padx=20, pady=20, side='left')

        ## event update시, func_click_item 수행.
        self.my_tree.bind('<ButtonRelease-1>', self.click_item)

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


        # Put data in treeview
        df_rows = self.df.round(3)
        df_rows = df_rows.to_numpy().tolist()

        # Add new data to treeview
        global count
        count = 0
        for row in df_rows:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
            count += 1

        return self.my_tree, self.tree_scroll_y, self.tree_scroll_x


    # def detail_table(self):
    #     connect = SQL(command=2)  ## SQL class 객체 생성.
    #     self.df = connect.sql_get()
    #     ShowTable.fn_show_table(selected_DBtable, df=self.df)


