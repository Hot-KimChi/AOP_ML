from tkinter import *
from tkinter import ttk


class DataTable:

    ## 클래스 멤버 변수로 선언
    str_sel_param = ""
    probeId = ""

    def __init__(self, df=None, selected_input=None, frame=None, table_cnt=None,
                 my_tree=None, tree_scroll_y=None, tree_scroll_x=None):
        super().__init__()
        self.df = df
        self.selected_input = selected_input
        self.frame = frame
        self.treeline = 20
        self.my_tree = my_tree
        self.tree_scroll_y = tree_scroll_y
        self.tree_scroll_x = tree_scroll_x


    def setup_style(self):

        # Add some style / Pick a theme
        style = ttk.Style()
        style.theme_use("default")

        # Configure our treeview colors
        style.configure("Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#D3D3D3"
                        )
        # Change selected color
        style.map('Treeview', background=[('selected', '#347083')])


    def click_item(self, event):
        ## multiple selection
        # global str_sel_param
        selectedItem = self.my_tree.selection()

        # 딕셔너리의 값 중에서 제일 앞에 있는 element 값 추출. ex) measSSId 추출.
        # sel_param_click = my_tree.item(selectedItem).get('values')[0]
        sel_param_click = []
        probeID_click = []
        for i in selectedItem:
            sel_param_click.append(self.my_tree.item(i).get('values')[0])
            probeID_click.append(self.my_tree.item(i).get('values')[9])
        self.str_sel_param = '(' + ','.join(str(x) for x in sel_param_click) + ')'
        self.probeId = probeID_click[0]

        print(self.str_sel_param)

        return self.str_sel_param, self.probeId

    def select_all_rows(self):
        # Select all rows in the Treeview
        self.my_tree.selection_set(self.my_tree.get_children())
        # Change the background color of all selected rows
        for i in self.my_tree.selection():
            self.my_tree.item(i, tags=('selected_row',))



    def deselect_all_rows(self):
        # Treeview에서 모든 행 선택 해제
        for i in self.my_tree.selection():
            self.my_tree.selection_remove(i)
            # 행의 태그 'selected_row'가 존재하면 배경 색상을 변경합니다
            if 'selected_row' in self.my_tree.item(i, 'tags'):
                self.my_tree.item(i, tags=())  # 'selected_row' 태그 제거
                # 원래의 배경 색상을 복원합니다
                original_background_color = 'lightblue' if int(i) % 2 == 0 else 'white'
                print(i)
                tags = ('evenrow',) if int(i) % 2 == 0 else ('oddrow',)
                self.my_tree.item(i, tags=tags)
                self.my_tree.item(i, {'tags': tags, 'values': self.my_tree.item(i, 'values'), 'text': "", 'open': 0,
                                      'background': original_background_color})


    def update_treeview(self):
        # # Destroy the previous tree and scrollbars, if any
        if self.my_tree:
            self.my_tree.destroy()
            self.tree_scroll_y.destroy()
            self.tree_scroll_x.destroy()

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

        ## setup_Treeview style
        self.setup_style()

        # Add a tag for all selected rows
        self.my_tree.tag_configure('selected_row', background='#347083', foreground='white')

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
