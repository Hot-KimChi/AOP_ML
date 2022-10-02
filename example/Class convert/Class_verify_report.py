import os
import tkinter
import pymssql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk
from functools import partial
import configparser
import warnings
warnings.filterwarnings("ignore")

from tkinter import filedialog
import joblib

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# warnings.simplefilter(action='ignore', category=FutureWarning)


## 머신러닝 클래스 생성.
class verify_report():

    ## 속성 생성
    def __init__(self):

        self.root_ML = tkinter.Toplevel()
        self.root_ML.title(f"{database}" + ' / Machine Learning')
        self.root_ML.geometry("410x200")
        self.root_ML.resizable(False, False)

        self.frame1 = Frame(self.root_ML, relief="solid", bd=2)
        self.frame1.pack(side="top", fill="both", expand=True)

        self.label_ML = Label(self.frame1, text='Machine Learning')
        self.label_ML.place(x=5, y=5)
        self.combo_ML = ttk.Combobox(self.frame1, value=list_ML, width=35, height=0, state='readonly')
        self.combo_ML.place(x=5, y=25)

        self.btn_load = Button(self.frame1, width=15, height=2, text='Select & Train', command=self.func_preprocessML)
        self.btn_load.place(x=280, y=5)

        self.root_ML.mainloop()


    def func_verify_report():
        try:

            def
            ## summary report 역시 multy selection 진행.
            ## selected_probeId

            root_verify = tkinter.Toplevel()
            root_verify.title(f"{database}" + ' / Verify_Report')
            root_verify.geometry("1720x1000")
            root_verify.resizable(False, False)

            frame1 = Frame(root_verify, relief="solid", bd=2)
            frame1.pack(side="top", fill="both", expand=True)
            frame2 = Frame(root_verify, relief="solid", bd=2)
            frame2.pack(side="bottom", fill="both", expand=True)

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
            style.map('Treeview',
                      background=[('selected', '#347083')])

            root_verify.mainloop()


            # ## measSSId에서 데이터 multy selection 후 아래 실행.
            #
            # conn = pymssql.connect(server_address, ID, password, database)
            # cursor = conn.cursor()
            #
            # query = f'''
            #
            # SELECT * FROM
            # (
            # SELECT TOP (100) PERCENT
            #     dbo.Tx_summary.Num, dbo.Tx_summary.ProbeName, dbo.Tx_summary.Software_version, dbo.Tx_summary.Exam, dbo.Tx_summary.CurrentState,dbo.Tx_summary.BeamStyleIndex,
            #     dbo.Tx_summary.TxFrequency, dbo.Tx_summary.ElevAperIndex, dbo.Tx_summary.NumTxCycles, dbo.WCS.NumTxCycles AS WCS_Cycle, dbo.Tx_summary.TxpgWaveformStyle,
            #     dbo.Tx_summary.TxChannelModulationEn, dbo.Tx_summary.Compounding, dbo.SSR_table.WCSId, dbo.SSR_table.SSRId, dbo.SSR_table.reportTerm_1, dbo.SSR_table.XP_Value_1,
            #     dbo.SSR_table.reportValue_1, dbo.SSR_table.Difference_1, dbo.SSR_table.Ambient_Temp_1, dbo.SSR_table.reportTerm_2, dbo.SSR_table.XP_Value_2, dbo.SSR_table.reportValue_2,
            #     dbo.SSR_table.Difference_2, ROW_NUMBER() over (partition by num order by reportvalue_1 desc) as RankNo, dbo.meas_res_summary.isDataUsable
            #
            # FROM dbo.Tx_summary
            #
            # LEFT OUTER JOIN dbo.WCS
            #     ON dbo.Tx_summary.ProbeID = dbo.WCS.probeId AND dbo.Tx_summary.BeamStyleIndex = dbo.WCS.Mode AND dbo.Tx_summary.TxFreqIndex = dbo.WCS.TxFrequencyIndex AND
            #     dbo.Tx_summary.ElevAperIndex = dbo.WCS.ElevAperIndex AND dbo.Tx_summary.TxpgWaveformStyle = dbo.WCS.WaveformStyle AND
            #     dbo.Tx_summary.TxChannelModulationEn = dbo.WCS.ChModulationEn AND dbo.Tx_summary.CurrentState = dbo.WCS.CurrentState
            # LEFT OUTER JOIN dbo.meas_res_summary
            #     ON dbo.WCS.wcsID = dbo.meas_res_summary.VerifyID
            # LEFT OUTER JOIN dbo.SSR_table
            #     ON dbo.WCS.wcsID = dbo.SSR_table.WCSId AND dbo.SSR_table.measSSId IN (896, 902, 905, 906)
            #
            # --where reportTerm_1 = 'MI' or reportTerm_1 IS NULL
            # --where reportTerm_2 = 'Ispta.3'
            # where isDataUsable = 'yes' AND reportTerm_1 = 'MI' or reportTerm_1 IS NULL
            # ) T
            # where RankNo = 1 and ProbeName = 'P8'
            # order by num
            #
            # '''
            #
            # Raw_data = pd.read_sql(sql=query, con=conn)
            # print(Raw_data)
            #
            # return Raw_data
            # conn.close()

        except():
            print("Error: func_verify_report")


## Login 버튼누를 경우, func_main 실행 listbox에 있는 database로 접속.
def func_main():
    try:
        global database, list_probeIds, list_probe, list_probenames
        database = combo_login.get()

        root_main = tkinter.Toplevel()
        root_main.title(f"{database}" + ' / main')
        root_main.geometry("440x300")
        root_main.resizable(False, False)


        df = func_sql_get(server_address, ID, password, database, 1)
        df_probeIds = df[['probeId']]

        list_probeIds = df_probeIds.values.tolist()
        ## ProbeID and ProbeName를 list로 변환.
        list_probeinfor = df.values.tolist()
        numprobe = len(list_probeinfor)

        list_probenames = list(zip(*list_probeinfor))[0]
        list_probe = list()

        # Probelist를 probeName + probeId 생성
        for i in range(numprobe):
            list_probe.append('  |  '.join(map(str, list_probeinfor[i])))
        btn_ML = Button(root_main, width=30, height=3, text='Verification Report', command=func_verify_report)
        btn_ML.grid(row=0, column=0)

        root_main.mainloop()

    except:
        print("Error: main")


# verify_report main flow
if __name__ == '__main__':
    ### config 파일에서 Database information read   ###
    config = configparser.ConfigParser()
    config.read('AOP_config.cfg')

    server_address = config["server address"]["address"]
    databases = config["database"]["name"]
    ID = config["username"]["ID"]
    password = config["password"]["PW"]
    server_table_M3 = config["server table"]["M3 server table"]
    Machine_Learning = config["Machine Learning"]["Model"]

    list_database = databases.split(',')
    list_M3_table = server_table_M3.split(',')
    list_ML = Machine_Learning.split(',')

    ## Start tk 만들기.
    root = Tk()
    root.title("DB 선택")
    root.geometry("280x150")
    root.resizable(False, False)

    label1 = Label(root, text='데이터베이스를 선택하세요')
    label1.place(x=10, y=10)

    # combo-Box 만들어서 데이터베이스만들기
    combo_login = ttk.Combobox(root, value=list_database)
    # combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
    combo_login.current(0)
    # combo-Box 의 위치
    combo_login.place(x=10, y=30)
    # login_combo.pack(pady=20)

    btn_login = Button(root, width=10, height=2, text='Login', command=func_main)
    btn_login.place(x=180, y=10)

    root.mainloop()