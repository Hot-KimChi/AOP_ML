import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd

from pkg_SQL.database import SQL
from pkg_Table.treeview_update import DataTable
from pkg_Viewer.select_param import SelectParam
from pkg_Verify_Report.execute_query_report import Execute_Query_Report
from pkg_Verify_Report.pre_process import PreProcess
from pkg_MeasSetGen.data_inout import DataOut


class Verify_Report():
    """
    verify step same as initial viewer
    1) For initial case, same as viewer.py
        - need to update(panel part)
        - Combo-box sequence changed.
    2) For selected item, SQL query execute.
    """
    def __init__(self, database, list_probe):
        # super().__init__(database, list_probe)
        self.table_cnt = 0

        self.database = database
        self.list_probe = list_probe

        window_verify = tk.Toplevel()
        window_verify.title(f"{self.database}" + ' / Verify Report')
        window_verify.geometry("1600x700")
        # window_verify.resizable(False, False)

        self.frame1 = Frame(window_verify, relief="solid", bd=2)
        self.frame1.pack(side="top", fill="both", expand=True)

        label_probename = Label(self.frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(self.frame1, value=self.list_probe, height=0, state='readonly')
        self.combo_probename.place(x=110, y=5)
        self.combo_probename.bind('<<ComboboxSelected>>', self._get_sequence)

        label_SW = Label(self.frame1, text='Software Version')
        label_SW.place(x=5, y=25)
        self.entry_SW = Entry(self.frame1, width=20, bg='light blue')
        self.entry_SW.place(x=110, y=25)

        label_filter = Label(self.frame1, text='filter Column')
        label_filter.place(x=280, y=5)
        combo_list_columns = ttk.Combobox(self.frame1, height=0, state='readonly')
        combo_list_columns.place(x=360, y=5)

        label_sel_data = Label(self.frame1, text='Selection')
        label_sel_data.place(x=280, y=25)
        self.combo_sel_datas = ttk.Combobox(self.frame1, height=0, state='readonly')
        self.combo_sel_datas.place(x=360, y=25)

        btn_read = Button(self.frame1, width=15, height=2, text='Load Summary File', command=self.load_Txsumm)
        btn_read.place(x=550, y=5)

        btn_view = Button(self.frame1, width=15, height=2, text='Verify Report', command=self.execute_report)
        btn_view.place(x=700, y=5)

        ## initial data update from SQL[measSSId]
        connect = SQL(command=5)
        self.df = connect.sql_get()

        self.table_cnt += 1
        self.table = DataTable(df=self.df, frame=self.frame1, table_cnt=self.table_cnt)
        self.my_tree, self.tree_scroll_y, self.tree_scroll_x = self.table.update_treeview()

        window_verify.mainloop()


    def _get_sequence(self, event):

        selected_probeinfo = self.combo_probename.get().replace(" ", "")        ## 공백 없애기 " " --> ""
        idx = selected_probeinfo.find("|")
        selected_probeId = selected_probeinfo[idx+1:]

        if self.my_tree:
            self.my_tree.destroy()
            self.tree_scroll_y.destroy()
            self.tree_scroll_x.destroy()
            self.table_cnt = 0

        self.table_cnt += 1
        selparam = SelectParam(self.frame1, probeId=selected_probeId, DBTable='meas_station_setup',
                               table_cnt=self.table_cnt)
        self.table, self.table_cnt, self.my_tree, self.tree_scroll_y, self.tree_scroll_x = selparam.select_param()


    def load_Txsumm(self):

        selected_probeinfo = self.combo_probename.get().replace(" ", "")  ## 공백 없애기 " " --> ""
        idx = selected_probeinfo.find("|")
        selected_probeId = selected_probeinfo[idx + 1:]
        selected_probename = selected_probeinfo[:idx]
        SW = self.entry_SW.get()

        PreProcess(self.database, selected_probeId, selected_probename, SW)


    def execute_report(self):

        print(self.table.str_sel_param, self.table.probeId)

        # MI case
        MI_case = Execute_Query_Report('reportValue_1', self.table.str_sel_param, 'MI', self.table.probeId)
        df_MI = MI_case.parsing()

        # Ispta.3 case
        Ispta_case = Execute_Query_Report('reportValue_2', self.table.str_sel_param, 'MI', self.table.probeId)
        df_Ispta = Ispta_case.parsing()

        # MI dataframe merge with Ispta.3 dataframe
        MI_column_by_index = df_MI.iloc[:, 0:22]  # 0부터 시작하는 인덱스

        Ispta_column_by_index_Id = df_Ispta.iloc[:, 16:18]
        Ispta_column_by_index_value = df_Ispta.iloc[:, 23:27]
        df_intensity = pd.concat([MI_column_by_index, Ispta_column_by_index_Id, Ispta_column_by_index_value], axis=1)

        # Temperature case
        Temp_case = Execute_Query_Report('reportValue_1', self.table.str_sel_param, 'Temp', self.table.probeId)
        df_Temp = Temp_case.parsing()

        dataout = DataOut(case=1, database=self.database, df1=df_intensity, df2=df_Temp)
        dataout.make_dir()
        dataout.save_excel()
