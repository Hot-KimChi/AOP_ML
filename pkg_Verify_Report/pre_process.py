import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pandas as pd

from pkg_SQL.database import SQL
from pkg_Table.treeview_update import DataTable
from pkg_Viewer.select_param import SelectParam
from pkg_Verify_Report.execute_query_report import Execute_Query_Report
from pkg_MeasSetGen.data_inout import DataOut


class PreProcess:
    """
    pre-process for the selection of Tx summary data
    """

    def __init__(self, database, selected_probename, selected_probeId, SW):
        self.database = database
        self.selected_probename = selected_probename
        self.selected_probeId = selected_probeId
        self.SW = SW

        self.init_color = "SystemButtonFace"
        self.current_color = self.init_color
        self.btn_all_flg = 0

        self._get_sequence()


    def _get_sequence(self):

        self.panel_config()


    def panel_config(self):

        window_detail = tk.Toplevel()
        window_detail.title(f"{self.database}" + ' / Detail Table')
        window_detail.geometry("1800x700")
        # window_verify.resizable(False, False)

        self.frame1 = Frame(window_detail, relief="solid", bd=2)
        self.frame1.pack(side="top", fill="both", expand=True)

        self.btn_all = Button(self.frame1, width=15, height=2, text='Choose Condition', bg=self.init_color, command=self.all_button_click)
        self.btn_all.place(x=15, y=5)

        btn_read = Button(self.frame1, width=15, height=2, text='To SQL', command=self.data_parser)
        btn_read.place(x=150, y=5)

        self.Tx_summ_process()

        window_detail.mainloop()


    def all_button_click(self):

        if self.btn_all_flg == 0:
            new_color = "blue"
            new_text = "All_Selected"
            new_text_color = "white"
            self.btn_all_flg = 1
            self.table.select_all_rows()
        else:
            new_color = "SystemButtonFace"
            new_text = "Choose Condition"
            new_text_color = "black"
            self.btn_all_flg = 0
            self.table.deselect_all_rows()

        self.btn_all.configure(bg=new_color, fg=new_text_color, text=new_text)


    def Tx_summ_process(self):
        try:

            # 파일 대화 상자를 통해 CSV 파일 선택
            filename = filedialog.askopenfilename(initialdir='.')
            if not filename:
                print("파일이 선택되지 않았습니다.")
                return

            data = pd.read_csv(filename, delimiter='\t')

            data['ProbeName'] = self.selected_probename
            data['ProbeID'] = self.selected_probeId
            data['Software_version'] = self.SW
            data['CurrentState'] = data['Mode']
            data['IsProcessed'] = 1
            data['IsLatest'] = 1

            # RLE data re-write
            list_rle = []
            for wf, rle in zip(data['TxpgWaveformStyle'], data['RLE']):
                if wf != 0:
                    list_rle.append(-1)
                elif wf == 0:
                    list_rle.append(rle)
            data['RLE'] = list_rle

            # Dual_mode를 mode lenth로 update
            dual_mode = []
            for mode in data['Mode']:
                dual_mode.append(len(mode)-1)
            data['Dual_Mode'] = dual_mode


            if data.empty:
                print("데이터가 비어있습니다.")
                return

            ## 해당 데이터 다른 table에 띄우기
            self.table = DataTable(df=data, frame=self.frame1)
            self.my_tree, self.tree_scroll_y, self.tree_scroll_x = self.table.update_treeview()

            self.data = data

        except Exception as e:
            print(f"Error: {e}")


    def data_parser(self):
        
        if self.btn_all_flg == 1:
            selected_data = self.data
        else:
            selected_param = [int(x) for x in self.table.str_sel_param.strip('()').split(',')]
            print(selected_param, type(selected_param))
         
            # 조건 설정: 'No' 열의 값이 원하는 값들 중 하나여야 함
            row_no = self.data['No'].isin(selected_param)
            selected_data = self.data[row_no]
        
        #데이터베이스 연결
        IsLastest_connect = SQL(command=9, selected_probeId=self.selected_probeId)
        IsLastest_connect.sql_parse()
        
        connect = SQL(command=10, data=selected_data)
        connect.sql_parse()
        