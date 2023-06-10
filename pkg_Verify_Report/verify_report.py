
class Verify_Report(object):
    def __init__(self ,):
        super().__init__()
        self.initialize()


    def initialize(self):
        global sel_cnt
        sel_cnt = 0

        window_verify = tkinter.Toplevel()
        window_verify.title(f"{database}" + ' / Verify Report')
        window_verify.geometry("1850x1000")
        # window_verify.resizable(False, False)

        self.frame1 = Frame(window_verify, relief="solid", bd=2)
        self.frame1.pack(side="top", fill="both", expand=True)
        self.frame2 = Frame(window_verify, relief="solid", bd=2)
        self.frame2.pack(side="bottom", fill="both", expand=True)


        label_probename = Label(self.frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(self.frame1, value=list_probe, height=0, state='readonly')
        self.combo_probename.place(x=115, y=5)
        self.combo_probename.bind('<<ComboboxSelected>>', self.fn_sel_update)

        btn_view = Button(self.frame1, width=15, height=2, text='Select & Load', command=self.fn_load_cond)
        btn_view.place(x=350, y=5)


        ## [meas_station_setup] load. / initial data update from SQL[measSSId]
        connect = SQL(command = 5)
        self.df = connect.fn_sql_get()

        sel_cnt += 1
        Viewer.fn_tree_update(self, df=self.df, frame=self.frame2, treeline=30)

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


        window_verify.mainloop()


    def fn_sel_update(self, event):

        global selected_probeId, sel_cnt
        selected_probeId = str(list_probeIds[self.combo_probename.current()])[1:-1]

        ## SQL class 객체 생성.
        connect = SQL(command = 6)
        self.df = connect.fn_sql_get()

        sel_cnt += 1
        Viewer.fn_tree_update(self, df=self.df, frame=self.frame2, treeline=30)


    def fn_load_cond(self):
        ## SQL class 객체 생성.
        connect = SQL(command = 7)
        self.df = connect.fn_sql_get()


        DataUsable_list = []
        SSRId_list = []
        reportTerm_1_list = []
        XP_value_1_list = []
        reportValue_1_list = []
        Difference_1_list = []
        Ambient_Temp_1_list = []

        # params = self.df['DataUsable'], self.df['SSRId'], self.df['reportTerm_1'], self.df['XP_Value_1'], self.df['reportValue_1'], self.df['Difference_1'], self.df['Ambient_Temp_1']
        for usable, id, term, xp, value, diff, ambi in zip(self.df['DataUsable'], self.df['SSRId'], self.df['reportTerm_1'], self.df['XP_Value_1'], self.df['reportValue_1'], self.df['Difference_1'], self.df['Ambient_Temp_1']):
            if usable == 'No':
                DataUsable_list.append('No')
                SSRId_list.append('NULL')
                reportTerm_1_list.append('NULL')
                XP_value_1_list.append('NULL')
                reportValue_1_list.append('NULL')
                Difference_1_list.append('NULL')
                Ambient_Temp_1_list.append('NULL')
            else:
                DataUsable_list.append(usable)
                SSRId_list.append(id)
                reportTerm_1_list.append(term)
                XP_value_1_list.append(round(xp, 2))
                reportValue_1_list.append(round(value, 2))
                Difference_1_list.append(round(diff, 2))
                Ambient_Temp_1_list.append(round(ambi, 2))

        ## drop table for param
        self.df.drop \
            (['DataUsable', 'SSRId', 'reportTerm_1', 'XP_Value_1', 'reportValue_1', 'Difference_1', 'Ambient_Temp_1'], axis=1, inplace=True)

        ## update list_values
        self.df['DataUsable'] = DataUsable_list
        self.df['SSRId'] = SSRId_list
        self.df['reportTerm_1'] = reportTerm_1_list
        self.df['XP_Value_1'] = XP_value_1_list
        self.df['reportValue_1'] = reportValue_1_list
        self.df['Difference_1'] = Difference_1_list
        self.df['Ambient_Temp_1'] = Ambient_Temp_1_list

        ## 중복 제거
        self.df = self.df.drop_duplicates(keep='first')

        ShowTable.fn_show_table(selected_DBtable='WCS & SSR_table', df=self.df)


    def fn_max_cond(self):
        pass
