import os
import tkinter as tk
from tkinter import *

from pkg_SQL.database import SQL
from pkg_MeasSetGen.meas_generation import MeasSetGen
from pkg_Viewer.viewer import Viewer
from pkg_Verify_Report.verify_report import Verify_Report


class TopMenu:

    """
    Menu 선택을 위한 window
    1) meas_generation
    2) viewer
    3) TxSummary
    4) Verify_Report
    5) Machine_Learning

    """

    def __init__(self):

        self.database = os.environ["DATABASE"]

        self.window = tk.Toplevel()
        self.window.title(f"{self.database}" + ' / Menu')
        self.window.geometry("440x300")
        self.window.resizable(False, False)
        
        # 고정 폭 글꼴 설정
        self.window.option_add('*Font', 'Consolas 10')

        btn_gen = Button(self.window, width=30, height=3, text='MeasSetGeneration',
                         command=lambda: MeasSetGen(self.database, self.list_probe))
        btn_gen.grid(row=0, column=0)

        btn_sum = Button(self.window, width=30, height=3, text='SQL Viewer',
                         command=lambda: Viewer(self.database, self.list_probe))
        btn_sum.grid(row=0, column=1)

        # verification step
        btn_verify = Button(self.window, width=30, height=3, text='Verification Report',
                            command=lambda: Verify_Report(self.database, self.list_probe))
        btn_verify.grid(row=1, column=0)

        # 확인
        # btn_tx_sum = Button(self.window, width=30, height=3, text='Tx Summary', command=TxSumm)
        # btn_tx_sum.grid(row=1, column=0)


        # btn_ML = Button(self.window, width=30, height=3, text='Machine Learning', command=Machine_Learning)
        # btn_ML.grid(row=2, column=0)

        self.load_probeinfo()


    def load_probeinfo(self):

        ## SQL class 객체 생성.
        connect = SQL(command=1)
        df = connect.sql_get()
        df_probeIds = df[['probeId']]
        list_probeIds = df_probeIds.values.flatten().tolist()  # flatten을 사용하여 1차원 리스트로 변환
        list_probeinfor = df.values.tolist()

        numprobe = len(list_probeinfor)

        list_probenames = [row[0] for row in list_probeinfor]
        self.list_probe = []

        # Probelist를 probeName + probeId 생성
        for probename, probeid in zip(list_probenames, list_probeIds):
            formatted_probe = self.format_probe_string(str(probename), str(probeid))
            self.list_probe.append(formatted_probe)

        return self.list_probe
        

    def format_probe_string(self, probename, probeid):

        # '|'의 위치 계산 (전체 길이의 중앙)
        pipe_position = 11

        # probename 왼쪽 정렬, '|' 중앙, probeid 오른쪽 정렬
        formatted_string = f"{probename:<{pipe_position}}|{'':2}{probeid}"

        return formatted_string


if __name__ == '__main__':
    menu_window = tk.Tk()
    app_menu = TopMenu(menu_window)

    menu_window.mainloop()
