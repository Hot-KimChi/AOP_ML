import os
import configparser

import tkinter as tk                    
from tkinter import *
from tkinter import ttk

from pkg_Viewer.select_param import SelectParam


class Viewer:
    """
    SQL Viewer 버튼이 눌렸을 경우, 해당 클래스가 실행.
    1) Probe Name 선택 후
    2) SQL Table Name 을 선택하고 난 이후 Select Table 버튼 누름.
    - SSR_table을 선택했을 경우, measSSID table을 먼저 선택하게끔 설정.
    """

    def __init__(self, database, list_probe):

        self.database = database
        self.list_probe = list_probe
        self.table_cnt = 0

        config_path = os.path.join(r".\backend\AOP_config.cfg")
        config = configparser.ConfigParser()
        config.read(config_path)
        server_table_M3 = config["server table"]["M3 server table"]
        list_M3_table = server_table_M3.split(',')


        window_view = tk.Toplevel()
        window_view.title(f"{self.database}" + ' / Viewer')
        window_view.geometry("1800x700")
        # window_view.resizable(False, False)

        self.frame1 = Frame(window_view, relief="solid", bd=2)
        self.frame1.pack(side="top", fill="both", expand=True)

        label_probename = Label(self.frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(self.frame1, value=self.list_probe, height=0, state='readonly')
        self.combo_probename.place(x=110, y=5)

        label_DB_table = Label(self.frame1, text='SQL Table Name')
        label_DB_table.place(x=5, y=25)
        self.combo_DBtable = ttk.Combobox(self.frame1, value=list_M3_table, height=0, state='readonly')
        self.combo_DBtable.place(x=110, y=25)
        self.combo_DBtable.bind('<<ComboboxSelected>>', self._get_sequence)

        label_filter = Label(self.frame1, text='filter Column')
        label_filter.place(x=280, y=5)

        combo_list_columns = ttk.Combobox(self.frame1, height=0, state='readonly')
        combo_list_columns.place(x=360, y=5)

        label_sel_data = Label(self.frame1, text='Selection')
        label_sel_data.place(x=280, y=25)

        self.combo_sel_datas = ttk.Combobox(self.frame1, height=0, state='readonly')
        self.combo_sel_datas.place(x=360, y=25)

        window_view.mainloop()


    def _get_sequence(self, event):
        selected_probeinfo = self.combo_probename.get().replace(" ", "")        ## 공백 없애기 " " --> ""
        idx = selected_probeinfo.find("|")
        selected_probeId = selected_probeinfo[idx+1:]
        selected_DBtable = self.combo_DBtable.get()

        self.table_cnt += 1

        selparam = SelectParam(frame=self.frame1, probeId=selected_probeId, DBTable=selected_DBtable,
                               table_cnt=self.table_cnt)
        self.table, self.table_cnt, self.my_tree, self.tree_scroll_y, self.tree_scroll_x = selparam.select_param()