import tkinter as tk
from tkinter import *
from tkinter import ttk

from pkg_SQL.database import SQL
from pkg_Viewer.update_table import DataTable
from pkg_Viewer.select_param import SelectParam


class Verify_Report:
    """"
    """
    def __init__(self, database, list_probe):

        self.sel_cnt = 0

        self.database = database
        self.list_probe = list_probe

        window_verify = tk.Toplevel()
        window_verify.title(f"{self.database}" + ' / Verify Report')
        window_verify.geometry("1850x1000")
        # window_verify.resizable(False, False)

        self.frame1 = Frame(window_verify, relief="solid", bd=2)
        self.frame1.pack(side="top", fill="both", expand=True)


        label_probename = Label(self.frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(self.frame1, value=self.list_probe, height=0, state='readonly')
        self.combo_probename.place(x=110, y=5)
        self.combo_probename.bind('<<ComboboxSelected>>', self._get_sequence)

        #
        # btn_view = Button(self.frame1, width=15, height=2, text='Select & Load', command=self.load_cond)
        # btn_view.place(x=350, y=5)


        ## [meas_station_setup] load. / initial data update from SQL[measSSId]
        connect = SQL(command=5)
        self.df = connect.sql_get()

        self.sel_cnt += 1
        datatable = DataTable(df=self.df, frame=self.frame1, sel_cnt=self.sel_cnt)
        datatable.update_treeview()


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

        select_table = SelectParam(frame=self.frame1, probeId=selected_probeId, DBTable='meas_station_setup',
                                   sel_cnt=self.sel_cnt)


        global my_tree, scroll_y, scroll_x

        if self.sel_cnt == 1:
            ## 초기 Treeview 생성 시,
            table = DataTable(df=self.df, selected_input=self.sel_data, frame=self.frame1, sel_cnt=self.sel_cnt)
            my_tree, scroll_y, scroll_x = table.update_treeview()
        else:
            ## 2번째 Treeview 생성 시, 초기 Treeview 삭제 필요.
            table = DataTable(df=self.df, selected_input=self.sel_data, frame=self.frame1, sel_cnt=self.sel_cnt,
                              my_tree=my_tree, tree_scroll_x=scroll_x, tree_scroll_y=scroll_y)
            my_tree, scroll_y, scroll_x = table.update_treeview()








    # def sel_update(self, event):
    #     selected_probeinfo = self.combo_probename.get().replace(" ", "")  ## 공백 없애기 " " --> ""
    #     idx = selected_probeinfo.find("|")
    #     selected_probeId = selected_probeinfo[idx + 1:]
    #
    #
    #     ## SQL class 객체 생성.
    #     connect = SQL(command = 6)
    #     self.df = connect.sql_get()
    #
    #     sel_cnt += 1
    #
    #     datatable = DataTable(df=self.df, frame=self.frame1, sel_cnt=sel_cnt)
    #     Viewer.fn_tree_update(self, df=self.df, frame=self.frame2, treeline=30)
    #
    #
    # def load_cond(self):
    #     ## SQL class 객체 생성.
    #     connect = SQL(command = 7)
    #     self.df = connect.fn_sql_get()
    #
    #
    #     DataUsable_list = []
    #     SSRId_list = []
    #     reportTerm_1_list = []
    #     XP_value_1_list = []
    #     reportValue_1_list = []
    #     Difference_1_list = []
    #     Ambient_Temp_1_list = []
    #
    #     # params = self.df['DataUsable'], self.df['SSRId'], self.df['reportTerm_1'], self.df['XP_Value_1'], self.df['reportValue_1'], self.df['Difference_1'], self.df['Ambient_Temp_1']
    #     for usable, id, term, xp, value, diff, ambi in zip(self.df['DataUsable'], self.df['SSRId'], self.df['reportTerm_1'], self.df['XP_Value_1'], self.df['reportValue_1'], self.df['Difference_1'], self.df['Ambient_Temp_1']):
    #         if usable == 'No':
    #             DataUsable_list.append('No')
    #             SSRId_list.append('NULL')
    #             reportTerm_1_list.append('NULL')
    #             XP_value_1_list.append('NULL')
    #             reportValue_1_list.append('NULL')
    #             Difference_1_list.append('NULL')
    #             Ambient_Temp_1_list.append('NULL')
    #         else:
    #             DataUsable_list.append(usable)
    #             SSRId_list.append(id)
    #             reportTerm_1_list.append(term)
    #             XP_value_1_list.append(round(xp, 2))
    #             reportValue_1_list.append(round(value, 2))
    #             Difference_1_list.append(round(diff, 2))
    #             Ambient_Temp_1_list.append(round(ambi, 2))
    #
    #     ## drop table for param
    #     self.df.drop \
    #         (['DataUsable', 'SSRId', 'reportTerm_1', 'XP_Value_1', 'reportValue_1', 'Difference_1', 'Ambient_Temp_1'], axis=1, inplace=True)
    #
    #     ## update list_values
    #     self.df['DataUsable'] = DataUsable_list
    #     self.df['SSRId'] = SSRId_list
    #     self.df['reportTerm_1'] = reportTerm_1_list
    #     self.df['XP_Value_1'] = XP_value_1_list
    #     self.df['reportValue_1'] = reportValue_1_list
    #     self.df['Difference_1'] = Difference_1_list
    #     self.df['Ambient_Temp_1'] = Ambient_Temp_1_list
    #
    #     ## 중복 제거
    #     self.df = self.df.drop_duplicates(keep='first')
    #
    #     ShowTable.fn_show_table(selected_DBtable='WCS & SSR_table', df=self.df)
    #
    #
    # def fn_max_cond(self):
    #     pass
