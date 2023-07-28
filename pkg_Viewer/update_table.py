from tkinter import *
from tkinter import ttk


def tree_update(df=None, selected_input=None, frame=None, treeline=20):
    try:
        ## tree table안에 있는 데이터를 선택해서 제일 앞에 있는 데이터를 (x1, x2, x3) 형태로 변수 update.
        def fn_click_item(event):
            ## multiple selection
            global str_sel_param
            selectedItem = self.my_tree.selection()

            # 딕셔너리의 값 중에서 제일 앞에 있는 element 값 추출. ex) measSSId 추출.
            # sel_param_click = my_tree.item(selectedItem).get('values')[0]
            sel_param_click = []
            for i in selectedItem:
                sel_param_click.append(self.my_tree.item(i).get('values')[0])
            str_sel_param = '(' + ','.join(str(x) for x in sel_param_click) + ')'


        # frame_list =[]
        # frame_list = frame


        ## select_count가 1번 이상일 경우, tree_table reset.
        if sel_cnt == 1 and selected_input == None:
            pass

        else:
            self.my_tree.destroy()
            self.tree_scroll_y.destroy()
            self.tree_scroll_x.destroy()


        ## tree_table 생성 및 update
        self.tree_scroll_y = Scrollbar(frame, orient="vertical")
        self.tree_scroll_y.pack(side=RIGHT, fill=Y)
        self.tree_scroll_x = Scrollbar(frame, orient="horizontal")
        self.tree_scroll_x.pack(side=BOTTOM, fill=X)

        self.my_tree = ttk.Treeview(frame, height=treeline, yscrollcommand=self.tree_scroll_y.set,
                                    xscrollcommand=self.tree_scroll_x.set, selectmode="extended")
        self.my_tree.pack(padx=20, pady=20, side='left')


        ## event update시, func_click_item 수행.
        self.my_tree.bind('<ButtonRelease-1>', fn_click_item)

        self.tree_scroll_y.config(command=self.my_tree.yview)
        self.tree_scroll_x.config(command=self.my_tree.xview)

        self.my_tree["column"] = list(df.columns)
        self.my_tree["show"] = "headings"

        # Loop thru column list for headers
        for column in self.my_tree["column"]:
            self.my_tree.column(column, width=100, minwidth=100)
            self.my_tree.heading(column, text=column)

        self.my_tree.tag_configure('oddrow', background="lightblue")
        self.my_tree.tag_configure('evenrow', background="white")

        # Put data in treeview
        df_rows = df.round(3)
        df_rows = df_rows.to_numpy().tolist()

        global count
        count = 0
        for row in df_rows:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=row,
                                    tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
            count += 1

        return self.my_tree

    except:
        print("Error: fn_tree_update")



