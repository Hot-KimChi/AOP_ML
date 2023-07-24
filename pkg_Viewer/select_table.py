
class Select_Table:
    """
    선택한 parameters(probeID, DB_table)를 기반으로 MS-SQL 데이터 load
    """
    def __init__(self, list_probe):
        self.list_probe = list_probe


    def select_table(self):
        ## selected_probeId에 선택 & 선택된 DBtable에서 데이터 가져오기.
        connect = SQL(command = 0)                  ## SQL class 객체 생성.
        self.df = connect.fn_sql_get()

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
