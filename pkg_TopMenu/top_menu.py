import tkinter as tk
from tkinter import *
import pandas as pd


from pkg_SQL.database import SQL

class TopMenu:

    """
    Menu 선택을 위한 window
    1) meas_generation
    2) viewer
    3) TxSummary
    4) Verify_Report
    5) Machine_Learning

    """

    def __init__(self, server, ID, password, database):
        self.server = server
        self.ID = ID
        self.password = password
        self.database = database

        self.window_menu = tk.Toplevel()
        self.window_menu.title(f"{self.database}" + ' / Menu')
        self.window_menu.geometry("440x300")
        self.window_menu.resizable(False, False)
        #
        # btn_gen = Button(self.window_menu, width=30, height=3, text='MeasSetGeneration', command=meas_generation)
        # btn_gen.grid(row=0, column=0)
        #
        # btn_sum = Button(self.window_menu, width=30, height=3, text='SQL Viewer', command=Viewer)
        # btn_sum.grid(row=0, column=1)
        #
        # btn_tx_sum = Button(self.window_menu, width=30, height=3, text='Tx Summary', command=TxSumm)
        # btn_tx_sum.grid(row=1, column=0)
        #
        # btn_ML = Button(self.window_menu, width=30, height=3, text='Verification Report', command=Verify_Report)
        # btn_ML.grid(row=1, column=1)
        #
        # btn_ML = Button(self.window_menu, width=30, height=3, text='Machine Learning', command=Machine_Learning)
        # btn_ML.grid(row=2, column=0)

    def load_probeinfo(self):

        ## SQL class 객체 생성.
        connect = SQL(server_address=self.server, server_id=self.ID, password=self.password, database=self.database, command=1)
        df = connect.fn_sql_get()
        df_probeIds = df[['probeId']]
        print(df_probeIds)


        list_probeIds = df_probeIds.values.tolist()
        ## ProbeID and ProbeName를 list로 변환.
        list_probeinfor = df.values.tolist()
        numprobe = len(list_probeinfor)

        list_probenames = list(zip(*list_probeinfor))[0]
        list_probe = list()

        # Probelist를 probeName + probeId 생성
        for i in range(numprobe):
            list_probe.append('  |  '.join(map(str, list_probeinfor[i])))


if __name__ == '__main__':
    menu_window = tk.Tk()
    app_menu = TopMenu(menu_window)

    menu_window.mainloop()