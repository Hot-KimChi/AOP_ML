import tkinter as tk
from tkinter import *
from tkinter import ttk

import pandas as pd

from pkg_SQL.database import SQL
from pkg_Viewer.update_table import DataTable
from pkg_Viewer.select_param import SelectParam
from pkg_Verify_Report.verify_query import verify_query
from pkg_MeasSetGen.data_inout import DataOut


class Verify_Report:
    """
    verify step same as initial viewer
    1) For initial case, same as viewer.py
        - need to update(panel part)
        - Combo-box sequence changed.
    2) For selected item, SQL query execute.
    """
    def __init__(self, database, list_probe):

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


        label_filter = Label(self.frame1, text='filter Column')
        label_filter.place(x=280, y=5)

        combo_list_columns = ttk.Combobox(self.frame1, height=0, state='readonly')
        combo_list_columns.place(x=360, y=5)

        label_sel_data = Label(self.frame1, text='Selection')
        label_sel_data.place(x=280, y=25)

        self.combo_sel_datas = ttk.Combobox(self.frame1, height=0, state='readonly')
        self.combo_sel_datas.place(x=360, y=25)

        btn_view = Button(self.frame1, width=15, height=2, text='Verify Report', command=self.execute_query)
        btn_view.place(x=600, y=5)

        ## initial data update from SQL[measSSId]
        connect = SQL(command=5)
        self.df = connect.sql_get()

        self.table_cnt += 1
        self.table = DataTable(df=self.df, frame=self.frame1, table_cnt=self.table_cnt)
        self.my_tree, self.tree_scroll_y, self.tree_scroll_x = self.table.update_treeview()


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


    def execute_query(self):

        print(self.table.str_sel_param, self.table.probeId)

        # MI case
        MI_case = verify_query('reportValue_1', self.table.str_sel_param, 'MI', self.table.probeId)
        df_MI = MI_case.parsing()

        # Ispta.3 case
        Ispta_case = verify_query('reportValue_2', self.table.str_sel_param, 'MI', self.table.probeId)
        df_Ispta = Ispta_case.parsing()

        # MI dataframe merge with Ispta.3 dataframe

        # Temperature case
        Temp_case = verify_query('reportValue_1', self.table.str_sel_param, 'Temp', self.table.probeId)
        df_Temp = Temp_case.parsing()

        dataout = DataOut(case=1, database=self.database, df1=df_MI, df2=df_Ispta, df3=df_Temp)
        dataout.make_dir()
        dataout.save_excel()
