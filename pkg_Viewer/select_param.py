from tkinter import *
from tkinter import ttk

from pkg_SQL.database import SQL
from pkg_Table.showTable import ShowTable
from pkg_Viewer.update_table import DataTable


class SelectParam:
    """
    선택한 parameters(probeID, DB_table)를 기반으로 MS-SQL 데이터 load
    """
    def __init__(self, frame, probeId, DBTable):
        self.frame1 = frame
        self.probeId = probeId
        self.DBTable = DBTable


        ## selected_probeId에 선택 & 선택된 DBtable에서 데이터 가져오기.
        ## SQL class 객체 생성.
        connect = SQL(command=0, selected_DBtable=self.DBTable, selected_probeId=self.probeId)
        self.df = connect.sql_get()
        self.sel_cnt = 0

        self.select_param()


    def select_param(self):

        list_params = self.df.columns.values.tolist()

        ''' 선택된 columns을 combobox형태로 생성 & binding event통해 선택 시, func_on_selected 실행.'''
        label_filter = Label(self.frame1, text='filter Column')
        label_filter.place(x=280, y=5)

        combo_list_columns = ttk.Combobox(self.frame1, value=list_params, height=0, state='readonly')
        combo_list_columns.place(x=360, y=5)
        combo_list_columns.bind('<<ComboboxSelected>>', self.on_selected)

        label_sel_data = Label(self.frame1, text='Selection')
        label_sel_data.place(x=280, y=25)

        ## 빈 Combobox show-up / 선택 시, parameter 데이터 업데이트
        self.combo_sel_datas = ttk.Combobox(self.frame1, height=0, state='readonly')
        self.combo_sel_datas.place(x=360, y=25)
        #
        # btn_view = Button(self.frame_down, width=15, height=2, text='Select & Detail', command=self.detail_table)
        # btn_view.place(x=350, y=5)

        # table = DataTable(df=self.df, frame=self.frame_down, sel_cnt=self.sel_cnt)
        # table.update_treeview()


    def on_selected(self, event):

        # parameter 중 데이터 load하여 user가 filter된 데이터를 선정하게 되면 sel_update binding.
        self.selected_param = event.widget.get()
        list_datas = self.df[f'{self.selected_param}'].values.tolist()

        # list에서 unique한 데이터를 추출하기 위해 set으로 변경하여 고유값으로 변경 후, 다시 list로 변경.
        set_datas = set(list_datas)
        filtered_datas = list(set_datas)

        self.combo_sel_datas = ttk.Combobox(self.frame1, value=filtered_datas, height=0, state='readonly')
        self.combo_sel_datas.place(x=360, y=25)
        self.combo_sel_datas.bind('<<ComboboxSelected>>', self.sel_update)


    def sel_update(self, event):

        self.sel_cnt = self.sel_cnt + 1
        sel_data = self.combo_sel_datas.get()

        ## SQL class 객체 생성.
        connect = SQL(command=3, selected_probeId=self.probeId, selected_param=self.selected_param, sel_data=sel_data,
                      selected_DBtable=self.DBTable)
        self.df = connect.sql_get()



        global my_tree, scroll_y, scroll_x
        if self.sel_cnt == 1:
            ## 초기 Treeview 생성 시,
            table = DataTable(df=self.df, selected_input=sel_data, frame=self.frame1, sel_cnt=self.sel_cnt)
            my_tree, scroll_y, scroll_x = table.update_treeview()
        else:
            ## 2번째 Treeview 생성 시, 초기 Treeview 삭제 필요.
            table = DataTable(df=self.df, selected_input=sel_data, frame=self.frame1, sel_cnt=self.sel_cnt,
                              my_tree=my_tree, tree_scroll_x=scroll_x, tree_scroll_y=scroll_y)
            my_tree, scroll_y, scroll_x = table.update_treeview()
