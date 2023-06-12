import tkinter
from tkinter import *
from tkinter import ttk


class TopMain:

    """
    Menu 선택을 위한 Windows
    1) meas
    2) viewer

    """

    def __init__(self):



    def fn_Menu(self):
        global list_probeIds, list_probe, list_probenames


        window_Menu = tkinter.Toplevel()
        window_Menu.title(f"{database}" + ' / Menu')
        window_Menu.geometry("440x300")
        window_Menu.resizable(False, False)

        ## SQL class 객체 생성.
        connect = SQL(server_address=server, server_id, password, database comman d =1,  )
        df = connect.fn_sql_get()
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


        btn_gen = Button(window_Menu, width=30, height=3, text='MeasSetGeneration', command=meas_generation)
        btn_gen.grid(row=0, column=0)

        btn_sum = Button(window_Menu, width=30, height=3, text='SQL Viewer', command=Viewer)
        btn_sum.grid(row=0, column=1)

        btn_tx_sum = Button(window_Menu, width=30, height=3, text='Tx Summary', command=TxSumm)
        btn_tx_sum.grid(row=1, column=0)

        btn_ML = Button(window_Menu, width=30, height=3, text='Verification Report', command=Verify_Report)
        btn_ML.grid(row=1, column=1)

        btn_ML = Button(window_Menu, width=30, height=3, text='Machine Learning', command=Machine_Learning)
        btn_ML.grid(row=2, column=0)

        window_Menu.mainloop()