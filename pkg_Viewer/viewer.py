import os
import configparser

import tkinter as tk
from tkinter import *
from tkinter import ttk

from pkg_Viewer.select_table import SelectTable


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

        config_path = os.path.join("pkg_login", "../AOP_config.cfg")
        config = configparser.ConfigParser()
        config.read(config_path)
        server_table_M3 = config["server table"]["M3 server table"]
        list_M3_table = server_table_M3.split(',')


        window_view = tk.Toplevel()
        window_view.title(f"{self.database}" + ' / Viewer')
        window_view.geometry("1800x1100")
        # window_view.resizable(False, False)

        frame1 = Frame(window_view, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)
        self.frame2 = Frame(window_view, relief="solid", bd=2)
        self.frame2.pack(side="bottom", fill="both", expand=True)


        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(frame1, value=self.list_probe, height=0, state='readonly')
        self.combo_probename.place(x=115, y=5)

        label_DB_table = Label(frame1, text='SQL Table Name')
        label_DB_table.place(x=5, y=25)
        self.combo_DBtable = ttk.Combobox(frame1, value=list_M3_table, height=0, state='readonly')
        self.combo_DBtable.place(x=115, y=25)

        btn_view = Button(frame1, width=15, height=2, text='Select Table', command=self._get_sequence)
        btn_view.place(x=350, y=5)

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

        window_view.mainloop()


    def _get_sequence(self):
        selected_probeinfo = self.combo_probename.get().replace(" ", "")        ## 공백 없애기 " " --> ""
        idx = selected_probeinfo.find("|")
        selected_probeId = selected_probeinfo[idx+1:]
        selected_DBtable = self.combo_DBtable.get()

        select_table = SelectTable(frame_down=self.frame2, probeId=selected_probeId, DBTable=selected_DBtable)
