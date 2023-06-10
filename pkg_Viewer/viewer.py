
class Viewer(object):
    def __init__(self):
        super().__init__()
        self.initialize()


    def initialize(self):
        global sel_cnt
        sel_cnt = 0

        window_view = tkinter.Toplevel()
        window_view.title(f"{database}" + ' / Viewer')
        window_view.geometry("1800x1100")
        # window_view.resizable(False, False)

        frame1 = Frame(window_view, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)
        self.frame2 = Frame(window_view, relief="solid", bd=2)
        self.frame2.pack(side="bottom", fill="both", expand=True)


        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(frame1, value=list_probe, height=0, state='readonly')
        self.combo_probename.place(x=115, y=5)

        label_DB_table = Label(frame1, text='SQL Table Name')
        label_DB_table.place(x=5, y=25)
        self.combo_DBtable = ttk.Combobox(frame1, value=list_M3_table, height=0, state='readonly')
        self.combo_DBtable.place(x=115, y=25)

        btn_view = Button(frame1, width=15, height=2, text='Select Table', command=self._fn_viewer_sequence)
        btn_view.place(x=350, y=5)

        # if combo_DBtable == 'SSR_table':
        #     combo_list = ttk.Combobox(frame2, value=df.columns, height=0, state='readonly')
        #     combo_list.place(x=115, y=5)
        #     # combo_probename = ttk.Combobox(frame2, value=list_probe, height=0, state='readonly')
        #     # combo_probename.place(x=115, y=5)

        # Add some style
        style = ttk.Style()
        # Pick a theme
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

        window_view.mainloop()


    def _fn_viewer_sequence(self):
        self.fn_select_table()
        self.fn_update_table()


    def fn_select_table(self):

        global selected_probeId, selected_DBtable, selected_probename, sel_cnt  # , combo_SSId, combo_probesn
        sel_cnt += 1
        selected_probeId = str(list_probeIds[self.combo_probename.current()])[1:-1]
        selected_probename = str(list_probenames[self.combo_probename.current()])
        selected_DBtable = self.combo_DBtable.get()

        ## selected_probeId에 선택 & 선택된 DBtable에서 데이터 가져오기.
        connect = SQL(command = 0)                  ## SQL class 객체 생성.
        self.df = connect.fn_sql_get()


    def fn_update_table(self):

        list_params = self.df.columns.values.tolist()

        ''' 선택된 columns을 combobox형태로 생성 & binding event통해 선택 시, func_on_selected 실행.'''
        label_filter = Label(self.frame2, text='filter Column')
        label_filter.place(x=5, y=5)

        combo_list_columns = ttk.Combobox(self.frame2, value=list_params, height=0, state='readonly')
        combo_list_columns.place(x=115, y=5)
        combo_list_columns.bind('<<ComboboxSelected>>', self.fn_on_selected)

        btn_view = Button(self.frame2, width=15, height=2, text='Select & Detail', command=self.fn_detail_table)
        btn_view.place(x=350, y=5)

        self.fn_tree_update(df=self.df, frame=self.frame2)


    def fn_tree_update(self, df=None, selected_input=None, frame=None, treeline=20):
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


    def fn_sel_update(self, event):
        global sel_data
        sel_data = self.combo_sel_datas.get()

        ## SQL class 객체 생성.
        connect = SQL(command = 3)
        self.df = connect.fn_sql_get()

        self.fn_tree_update(df=self.df, selected_input=sel_data, frame=self.frame2)


    def fn_on_selected(self, event):
        global selected_param
        # parameter 중 한개를 선정하게 되면 filter 기능.
        selected_param = event.widget.get()
        list_datas = self.df[f'{selected_param}'].values.tolist()
        # list에서 unique한 데이터를 추출하기 위해 set으로 변경하여 고유값으로 변경 후, 다시 list로 변경.
        set_datas = set(list_datas)
        filtered_datas = list(set_datas)

        label_sel_data = Label(self.frame2, text='Selection')
        label_sel_data.place(x=5, y=25)

        self.combo_sel_datas = ttk.Combobox(self.frame2, value=filtered_datas, height=0, state='readonly')
        self.combo_sel_datas.place(x=115, y=25)
        self.combo_sel_datas.bind('<<ComboboxSelected>>', self.fn_sel_update)


    def fn_detail_table(self):
        connect = SQL(command = 2)                  ## SQL class 객체 생성.
        self.df = connect.fn_sql_get()
        ShowTable.fn_show_table(selected_DBtable, df=self.df)
