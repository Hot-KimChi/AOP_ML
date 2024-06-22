import os
import tkinter as tk
from tkinter import ttk
from pkg_SQL.database import SQL
from pkg_MeasSetGen.meas_generation import MeasSetGen
from pkg_Viewer.viewer import Viewer
from pkg_Verify_Report.verify_report import Verify_Report
from pkg_MachineLearning.machine_learning import Machine_Learning


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
        self.window.title(f"{self.database} / Menu")
        self.window.geometry("440x300")
        self.window.resizable(False, False)

        # 고정 폭 글꼴 설정
        self.window.option_add("*Font", "Consolas 10")

        # 버튼 설정
        buttons_info = [
            ("MeasSetGeneration", lambda: MeasSetGen(self.database, self.list_probe)),
            ("SQL Viewer", lambda: Viewer(self.database, self.list_probe)),
            (
                "Verification Report",
                lambda: Verify_Report(self.database, self.list_probe),
            ),
            ("Machine Learning", lambda: Machine_Learning(self.database)),
        ]

        # 버튼 배치
        for i, (text, command) in enumerate(buttons_info):
            row = i // 2
            col = i % 2
            btn = tk.Button(self.window, width=30, height=3, text=text, command=command)
            btn.grid(row=row, column=col)

        self.load_probeinfo()

    def load_probeinfo(self):
        # SQL class 객체 생성.
        connect = SQL(command=1)
        df = connect.sql_get()
        list_probeinfor = df.values.tolist()
        self.list_probe = [
            self.format_probe_string(str(row[0]), str(row[1]))
            for row in list_probeinfor
        ]
        return self.list_probe

    def format_probe_string(self, probename, probeid):
        # '|'의 위치 계산 (전체 길이의 중앙)
        pipe_position = 11
        # probename 왼쪽 정렬, '|' 중앙, probeid 오른쪽 정렬
        formatted_string = f"{probename:<{pipe_position}}|{'':2}{probeid}"
        return formatted_string


if __name__ == "__main__":
    menu_window = tk.Tk()
    app_menu = TopMenu(menu_window)
    menu_window.mainloop()
