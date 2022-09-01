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

def func_freqidx2Hz(idx):
    try:
        frequencyTable = [1000000,
                          1111100,
                          1250000,
                          1333300,
                          1428600,
                          1538500,
                          1666700,
                          1818200,
                          2000000,
                          2222200,
                          2500000,
                          2666700,
                          2857100,
                          3076900,
                          3333300,
                          3636400,
                          3809500,
                          4000000,
                          4210500,
                          4444400,
                          4705900,
                          5000000,
                          5333300,
                          5714300,
                          6153800,
                          6666700,
                          7272700,
                          8000000,
                          8888900,
                          10000000,
                          11428600,
                          13333333,
                          16000000,
                          20000000,
                          26666667,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600,
                          11428600]
        FreqIndex = idx
        freqHz = frequencyTable[FreqIndex]

        return freqHz

    except:
        print("Error: func_freqidx2Hz")


## SQL데이터 DataFrame을 이용하여 Treeview에 기록하여 출력.
def func_show_table(selected_DBtable, df=None, extra=None):
    try:
        n_root = tkinter.Toplevel()
        n_root.title(f"{database}  //  {selected_DBtable}")
        n_root.geometry("1720x1000")

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

        # Create Treeview Frame
        frame1 = Frame(n_root)
        frame1.pack(pady=20)


        tree_scroll_y = Scrollbar(frame1, orient="vertical")
        tree_scroll_y.pack(side=RIGHT, fill=Y)
        tree_scroll_x = Scrollbar(frame1, orient="horizontal")
        tree_scroll_x.pack(side=BOTTOM, fill=X)

        my_tree = ttk.Treeview(frame1, style="Treeview", height=20, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, selectmode="extended")
        # Pack to the screen
        my_tree.pack()

        tree_scroll_y.config(command=my_tree.yview)
        tree_scroll_x.config(command=my_tree.xview)

        my_tree["column"] = list(df.columns)
        my_tree["show"] = "headings"

        # Loop thru column list for headers
        for column in my_tree["column"]:
            my_tree.column(column, width=110, minwidth=110)
            my_tree.heading(column, text=column)

        my_tree.tag_configure('oddrow', background="lightblue")
        my_tree.tag_configure('evenrow', background="white")

        # Put data in treeview
        df_rows = df.round(3)
        df_rows = df_rows.to_numpy().tolist()


        global count
        count = 0
        for row in df_rows:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
            count += 1


        if (extra is not None):
            frame2 = Frame(n_root, relief="solid", bd=2)
            frame2.pack(side="bottom", fill="both", expand=True, pady=10)

            my_tree_extra = ttk.Treeview(frame2)

            my_tree_extra["column"] = list(extra.columns)
            my_tree_extra["show"] = "headings"

            # Loop thru column list for headers
            for column in my_tree_extra["column"]:
                my_tree_extra.column(column, width=110, minwidth=110)
                my_tree_extra.heading(column, text=column)

            # Put data in treeview
            df_rows = extra.to_numpy().tolist()
            for row in df_rows:
                my_tree_extra.insert("", "end", values=row)

            my_tree_extra.pack(pady=20)

        # n_root.mainloop()

    except():
        print('func_show_table')


## SQL 데이터베이스에 접속하여 데이터 load.
def func_sql_get(server_address, ID, password, database, command):
    try:
        conn = pymssql.connect(server_address, ID, password, database)

        if command > 5:
            query = "f'''" + command + "'''"

        elif command == 0:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM meas_station_setup WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''

        elif command == 1:
            query = '''
            SELECT probeName, probeId FROM probe_geo 
            order by probeName, probeId
            '''
        elif command == 2:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE measSSId = {sel_param_click}
                ORDER BY measSSId, 1
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''

        elif command == 3:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM meas_station_setup WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
                ORDER BY 1
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
                ORDER BY 1
                '''

        elif command == 4:
            query = f'''
            SELECT [probePitchCm], [probeRadiusCm], [probeElevAperCm0], [probeElevFocusRangCm] FROM probe_geo WHERE probeid = {selected_probeId}
            ORDER BY 1
            '''


        Raw_data = pd.read_sql(sql=query, con=conn)

        return Raw_data
        conn.close()

    except:
        print("Error: func_sql_get")


## root 제목 DB 변경 --> SQL 접속
def func_viewer_database():
    try:
        global iteration
        iteration = 0

        def func_1st_load():
            try:

                def func_tree_update(df=None, selected_input=None):
                    try:

                        def func_click_item(event):
                            global sel_param_click
                            selectedItem = my_tree.focus()
                            # 딕셔너리의 값 중에서 제일 앞에 있는 element 값 추출. ex) measSSId 추출.
                            sel_param_click = my_tree.item(selectedItem).get('values')[0]


                        # tree_scroll_y = Scrollbar(frame2, orient="vertical")
                        # tree_scroll_y.pack(side=RIGHT, fill=Y)
                        # tree_scroll_x = Scrollbar(frame2, orient="horizontal")
                        # tree_scroll_x.pack(side=BOTTOM, fill=X)

                        if iteration == 1 and selected_input == None:
                            global my_tree, tree_scroll_y, tree_scroll_x
                            tree_scroll_y = Scrollbar(frame2, orient="vertical")
                            tree_scroll_y.pack(side=RIGHT, fill=Y)
                            tree_scroll_x = Scrollbar(frame2, orient="horizontal")
                            tree_scroll_x.pack(side=BOTTOM, fill=X)

                            my_tree = ttk.Treeview(frame2, height=20, yscrollcommand=tree_scroll_y.set,
                                                   xscrollcommand=tree_scroll_x.set, selectmode="extended")
                            my_tree.pack(padx=20, pady=20, side='left')
                        else:
                            my_tree.destroy()
                            tree_scroll_y.destroy()
                            tree_scroll_x.destroy()

                            tree_scroll_y = Scrollbar(frame2, orient="vertical")
                            tree_scroll_y.pack(side=RIGHT, fill=Y)
                            tree_scroll_x = Scrollbar(frame2, orient="horizontal")
                            tree_scroll_x.pack(side=BOTTOM, fill=X)

                            my_tree = ttk.Treeview(frame2, height=20, yscrollcommand=tree_scroll_y.set,
                                                   xscrollcommand=tree_scroll_x.set, selectmode="extended")
                            my_tree.pack(padx=20, pady=20, side='left')
                            # for i in my_tree.get_children():
                            #     my_tree.delete(i)


                        # event update시, func_click_item 수행.
                        my_tree.bind('<ButtonRelease-1>', func_click_item)

                        tree_scroll_y.config(command=my_tree.yview)
                        tree_scroll_x.config(command=my_tree.xview)

                        my_tree["column"] = list(df.columns)
                        my_tree["show"] = "headings"

                        # Loop thru column list for headers
                        for column in my_tree["column"]:
                            my_tree.column(column, width=100, minwidth=100)
                            my_tree.heading(column, text=column)

                        my_tree.tag_configure('oddrow', background="lightblue")
                        my_tree.tag_configure('evenrow', background="white")

                        # Put data in treeview
                        df_rows = df.round(3)
                        df_rows = df_rows.to_numpy().tolist()

                        global count
                        count = 0
                        for row in df_rows:
                            if count % 2 == 0:
                                my_tree.insert(parent='', index='end', iid=count, text="", values=row,
                                               tags=('evenrow',))
                            else:
                                my_tree.insert(parent='', index='end', iid=count, text="", values=row, tags=('oddrow',))
                            count += 1

                    except():
                        print("Error: func_tree_update")


                global selected_probeId, selected_DBtable, selected_probename, iteration   #, combo_SSId, combo_probesn

                iteration += 1
                selected_probeId = str(list_probeIds[combo_probename.current()])[1:-1]
                selected_probename = str(list_probenames[combo_probename.current()])
                selected_DBtable = combo_DBtable.get()

                df = func_sql_get(server_address, ID, password, database, 0)

                ''' 선택한 table treeview update'''
                func_tree_update(df)

                ''' parameter list from SQL table '''
                list_params = df.columns.values.tolist()

                ''' SQL DB에서 받은 데이터의 선택된 column(ex: meas_person_name)에서 선택된 datas(HIS, others)를 추출하는 algorithm'''
                def func_on_selected(event):

                    def func_sel_update(event):
                        global sel_data
                        sel_data = combo_sel_datas.get()
                        table = func_sql_get(server_address, ID, password, database, 3)
                        func_tree_update(df=table, selected_input=sel_data)

                    global selected_param
                    # parameter 중 한개를 선정하게 되면 filter 기능.
                    selected_param = event.widget.get()
                    list_datas = df[f'{selected_param}'].values.tolist()
                    # list에서 unique한 데이터를 추출하기 위해 set으로 변경하여 고유값으로 변경 후, 다시 list로 변경.
                    set_datas = set(list_datas)
                    filtered_datas = list(set_datas)

                    label_sel_data = Label(frame2, text='Selection')
                    label_sel_data.place(x=5, y=25)

                    combo_sel_datas = ttk.Combobox(frame2, value=filtered_datas, height=0, state='readonly')
                    combo_sel_datas.place(x=115, y=25)
                    combo_sel_datas.bind('<<ComboboxSelected>>', func_sel_update)


                    # btn_filter = Button(frame2, width=15, height=2, text='filter', command=func_tree_update)
                    # btn_filter.place(x=380, y=5)


                ''' 선택된 columns을 combobox형태로 생성 & binding event통해 선택 시, func_on_selected 실행.'''
                label_filter = Label(frame2, text='filter Column')
                label_filter.place(x=5, y=5)

                combo_list_columns = ttk.Combobox(frame2, value=list_params, height=0, state='readonly')
                combo_list_columns.place(x=115, y=5)
                combo_list_columns.bind('<<ComboboxSelected>>', func_on_selected)


                    # measSSId = str(df['measSSId'].sort_values().unique())[1:-1]
                    # probeSN = str(df['probeSn'].sort_values().unique())[1:-1]
                    #
                    # label_SSId = Label(frame2, text='SSId')
                    # label_SSId.place(x=5, y=5)
                    # combo_SSId = ttk.Combobox(frame2, value=measSSId, height=0) #, state='readonly')
                    # combo_SSId.place(x=115, y=5)
                    #
                    # label_probesn = Label(frame2, text='probeSN')
                    # label_probesn.place(x=5, y=25)
                    # combo_probesn = ttk.Combobox(frame2, value=probeSN, height=0) #, state='readonly')
                    # combo_probesn.place(x=115, y=25)


                btn_view = Button(frame2, width=15, height=2, text='Select & View', command=func_select_view)
                btn_view.place(x=350, y=5)


            except():
                print("Error: func_1st_load")


        def func_select_view():
            try:
                global selected_probeId, selected_DBtable, selected_probename
                selected_probeId = str(list_probeIds[combo_probename.current()])[1:-1]
                selected_probename = str(list_probenames[combo_probename.current()])
                selected_DBtable = combo_DBtable.get()

                df = func_sql_get(server_address, ID, password, database, 2)
                func_show_table(selected_DBtable, df=df)

            except():
                print("Error: func_select_view")


        root_view = tkinter.Toplevel()
        root_view.title(f"{database}" + ' / Viewer')
        root_view.geometry("1720x800")
        root_view.resizable(False, False)

        frame1 = Frame(root_view, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)
        frame2 = Frame(root_view, relief="solid", bd=2)
        frame2.pack(side="bottom", fill="both", expand=True)

        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        combo_probename = ttk.Combobox(frame1, value=list_probe, height=0, state='readonly')
        combo_probename.place(x=115, y=5)

        label_DB_table = Label(frame1, text='SQL Table Name')
        label_DB_table.place(x=5, y=25)
        combo_DBtable = ttk.Combobox(frame1, value=list_M3_table, height=0, state='readonly')
        combo_DBtable.place(x=115, y=25)

        btn_view = Button(frame1, width=15, height=2, text='Detail from SQL', command=func_1st_load)
        btn_view.place(x=350, y=5)

        # if combo_DBtable == 'SSR_table':
        #     combo_list = ttk.Combobox(frame2, value=df.columns, height=0, state='readonly')
        #     combo_list.place(x=115, y=5)
        #     # combo_probename = ttk.Combobox(frame2, value=list_probe, height=0, state='readonly')
        #     # combo_probename.place(x=115, y=5)


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


        root_view.mainloop()

    except:
        print("Error: func_viewer_database")


def func_measset_gen():
    try:
        def func_create_data():
            try:
                filename = filedialog.askopenfilename(initialdir='.txt')
                df_UEdata = pd.read_csv(filename, sep='\t', encoding='cp949')
                ## BeamStyle, TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE, VTxIndex, elevAperIndex, SysPulserSelA
                df_first = df_UEdata.iloc[:, [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 16, 17, 15]]

                ########################
                ## B & M mode process ##
                # df_sort_B = df_B_mode.sort_values(by=[df_B_mode.columns[0], df_B_mode.columns[1], df_B_mode.columns[2], df_B_mode.columns[5], df_B_mode.columns[3]], ascending=True)
                # B_num = df_sort_B['TxFocusLocCm'].nunique()

                df_B_mode = df_first.loc[(df_first['BeamStyleIndex'] == 0) | (df_first['BeamStyleIndex'] == 1)]
                df_M_mode = df_first.loc[(df_first['BeamStyleIndex'] == 15) | (df_first['BeamStyleIndex'] == 20)]
                df_C_mode = df_first.loc[df_first['BeamStyleIndex'] == 5]
                df_D_mode = df_first.loc[df_first['BeamStyleIndex'] == 10]

                df = pd.concat([df_B_mode, df_M_mode, df_C_mode, df_D_mode])                                            ## 2개 데이터프레임 합치기
                df = df.reset_index(drop=True)                                                                          ## 데이터프레임 index reset
                df = df.fillna(0)                                                                                       ## 데이터 Null --> [0]으로 변환(데이터의 정렬, groupby null 값 문제 발생)

                list_params =['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 'TxPulseRle', 'TxFocusLocCm', 'NumTxElements']
                dup_count = df.groupby(by=list_params, as_index=False).count()                                          ## groupby로 중복 count.


                ##  duplicated parameter check. => dup = df.duplicated(['SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'TxPulseRle'], keep='first')
                ##  중복된 parameter가 있을 경우, 제거하기.
                drop_dup = df.drop_duplicates(list_params)
                sort_dup = drop_dup.sort_values(by=list_params, ascending=True).reset_index()


                ## bsIndexTrace list만들어서 2개 DataFrame에서 zip으로 for문.
                bsIndexTrace = []
                for beam, cnt in zip(sort_dup['BeamStyleIndex'], dup_count['BeamStyleIndex']):
                    if beam == 0 and cnt >= 2:
                        bsIndexTrace.append(15)
                    elif beam == 1 and cnt >= 2:
                        bsIndexTrace.append(20)
                    elif beam == 5 and cnt >= 2:
                        bsIndexTrace.append(10)
                    else:
                        bsIndexTrace.append(0)
                sort_dup['bsIndexTrace'] = bsIndexTrace


                ## FrequencyIndex to FrequencyHz
                n = 0
                FrequencyHz = []
                for i in sort_dup['SysTxFreqIndex'].values:
                    FrequencyHz.insert(n, func_freqidx2Hz(i))
                    n += 1
                sort_dup['TxFrequencyHz'] = FrequencyHz


                ## Calc_cycle for RLE code
                def func_cnt_cycle():

                    list_cycle = []
                    for i in range(len(sort_dup['TxpgWaveformStyle'])):

                        if sort_dup['TxpgWaveformStyle'][i] == 0:
                            rle = sort_dup['TxPulseRle'].str.split(":")[i]
                            list_flt = list(map(float, rle))
                            ## 아래 code도 가능.
                            ## floatList = [float(x) for x in list_option]
                            abs_value = np.abs(list_flt)

                            calc = []
                            for value in abs_value:
                                if 1 < value:
                                    calc.append(round(value - 1, 4))
                                else:
                                    calc.append(value)
                            cycle = round(sum(calc), 2)
                            list_cycle.append(cycle)

                        else:
                            cycle = sort_dup['ProbeNumTxCycles'][i]
                            list_cycle.append(cycle)

                    return list_cycle

                list_cycle = func_cnt_cycle()


                ##  input parameter define.
                global selected_probeId
                selected_probeId = str(list_probeIds[combo_probename.current()])[1:-1]
                selected_probename = str(list_probenames[combo_probename.current()])


                sort_dup['probeId'] = selected_probeId
                sort_dup['maxTxVoltageVolt'] = box_MaxVolt.get()
                sort_dup['ceilTxVoltageVolt'] = box_CeilVolt.get()
                sort_dup['totalVoltagePt'] = box_TotalVoltpt.get()
                sort_dup['numMeasVoltage'] = box_NumMeasVolt.get()
                sort_dup['ProbeNumTxCycles'] = list_cycle
                sort_dup['zStartDistCm'] = 0.5
                sort_dup['DTxFreqIndex'] = 0
                sort_dup['dumpSwVersion'] = box_DumpSW.get()
                sort_dup['measSetComments'] = f'Beamstyle_{selected_probename}_Intensity'



                ## function: calc_profTxVoltage 구현
                def func_calc_profvolt():
                    try:
                        profTxVoltageVolt = []
                        for str_maxV, str_ceilV, str_totalpt in zip(sort_dup['maxTxVoltageVolt'].values, sort_dup['ceilTxVoltageVolt'].values, sort_dup['totalVoltagePt'].values):
                            idx = 2
                            ## tkinter에서 넘어오는 데이터 string.
                            maxV = float(str_maxV)
                            ceilV = float(str_ceilV)
                            totalpt = int(str_totalpt)

                            profTxVoltageVolt.append(round((min(maxV, ceilV)) ** ((totalpt-1-idx)/(totalpt-1)), 2))
                        sort_dup['profTxVoltageVolt'] = profTxVoltageVolt

                    except():
                        print('error: func_profvolt')


                ## function: calc zMeasNum 구현
                def func_zMeasNum():
                    try:
                        zStartDistCm = 0.5
                        zMeasNum = []
                        for focus in sort_dup['TxFocusLocCm']:
                            if (focus <= 3):
                                zMeasNum.append((5 - zStartDistCm) * 10)
                            elif (focus <= 6):
                                zMeasNum.append((8 - zStartDistCm) * 10)
                            elif (focus <= 9):
                                zMeasNum.append((12 - zStartDistCm) * 10)
                            else:
                                zMeasNum.append((14 - zStartDistCm) * 10)
                        sort_dup['zMeasNum'] = zMeasNum

                    except():
                        print('error: func_zMeaNum')


                func_calc_profvolt()
                func_zMeasNum()


                ## sorting data
                sort_dup = sort_dup.sort_values(by=[sort_dup.columns[1], sort_dup.columns[2], sort_dup.columns[7], sort_dup.columns[3], sort_dup.columns[6], sort_dup.columns[4]], ascending=True)

                ## predict by Machine Learning model.
                ## load modeling by pickle file.
                loaded_model = joblib.load('Model/RandomForest_v1_python37.pkl')

                ## take parameters for ML from measSet_gen file.
                est_params = sort_dup[['TxFrequencyHz', 'TxFocusLocCm', 'NumTxElements', 'TxpgWaveformStyle',
                                        'ProbeNumTxCycles', 'elevAperIndex', 'IsTxChannelModulationEn']]
                est_geo = func_sql_get(server_address, ID, password, database, 4)

                est_params[['probePitchCm']] = est_geo['probePitchCm']
                est_params[['probeRadiusCm']] = est_geo['probeRadiusCm']
                est_params[['probeElevAperCm0']] = est_geo['probeElevAperCm0']
                est_params[['probeElevFocusRangCm']] = est_geo['probeElevFocusRangCm']


                zt_est = loaded_model.predict(est_params)
                df_zt_est = pd.DataFrame(zt_est, columns=['zt_est'])

                sort_dup['zt_est'] = round(df_zt_est, 1)


                ## replace the location of data.
                sorting_lists = ['measSetComments', 'probeId', 'BeamStyleIndex', 'bsIndexTrace', 'TxFrequencyHz',
                                     'TxFocusLocCm', 'maxTxVoltageVolt', 'ceilTxVoltageVolt', 'profTxVoltageVolt',
                                     'totalVoltagePt', 'numMeasVoltage', 'NumTxElements', 'TxpgWaveformStyle',
                                     'ProbeNumTxCycles', 'elevAperIndex', 'zStartDistCm', 'zMeasNum',
                                     'IsTxChannelModulationEn', 'dumpSwVersion', 'DTxFreqIndex', 'VTxIndex',
                                     'IsPresetCpaEn', 'TxPulseRle', 'SystemPulserSel', 'CpaDelayOffsetClk', 'zt_est']
                df_intensity = sort_dup[sorting_lists]


                ## Power condition and Temperature condition 생성.
                ## 필요없는 column 삭제.
                df_drop = sort_dup.drop(columns=['TxFocusLocCm', 'NumTxElements'])

                ## 중복된 데이터의 삭제.
                list_params = ['BeamStyleIndex', 'IsTxChannelModulationEn', 'TxFrequencyHz', 'TxpgWaveformStyle',
                               'ProbeNumTxCycles', 'TxPulseRle']
                df_drop_ORG = df_drop.drop_duplicates(list_params)

                # def func_cnt_cycle():
                #
                #     list_rle = []
                #     for wf in df_drop_ORG['TxpgWaveformStyle']:
                #         if wf == 0:
                #             list_rle.append(df_drop_ORG['TxPulseRle'].split(":"))
                #
                #         else:
                #             list_rle.append(0)
                #     print(list_rle)
                #
                # func_cnt_cycle()
                df_power = df_drop_ORG
                df_temperature = df_drop_ORG


                df_temperature['measSetComments'] = f'Beamstyle_{selected_probename}_Temperature'
                df_temperature['TxFocusLocCm'] = sort_dup['TxFocusLocCm'].max()
                df_temperature['NumTxElements'] = sort_dup['NumTxElements'].max()
                df_temperature['zt_est'] = 0
                df_temperature = df_temperature[sorting_lists]


                df_power['measSetComments'] = f'Beamstyle_{selected_probename}_Power'
                df_power['TxFocusLocCm'] = sort_dup['TxFocusLocCm'].max()
                df_power[['NumTxElements']] = int(round(1 / est_geo['probePitchCm']))
                df_power['zt_est'] = 0
                df_power = df_power[sorting_lists]


                df_merge = pd.concat([df_intensity, df_temperature, df_power])
                print(df_merge)


                func_show_table(selected_DBtable='meas_setting', df=df_merge)
                LUT_count = box_DumpSW.get()

                newpath = f'./{database}'
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                df_merge.to_csv(f'./{database}/meas_setting_{selected_probename}_{LUT_count}.csv', header=True, index=False)

                return df_merge

            except:
                print("Error: func_create_data")


        def func_insert_data():
            try:
                filename = filedialog.askopenfilename(initialdir='.txt')
                data = pd.read_csv(filename)
                df = pd.DataFrame(data)

                conn = pymssql.connect(server_address, ID, password, database)
                cursor = conn.cursor()

                for row in df.itertuples():
                    query = '''
                            INSERT INTO meas_setting (
                                       [measSetComments]
                                      ,[probeId]
                                      ,[beamstyleIndex]
                                      ,[bsIndexTrace]
                                      ,[txFrequencyHz]
                                      ,[focusRangeCm]
                                      ,[maxTxVoltageVolt]
                                      ,[ceilTxVoltageVolt]
                                      ,[profTxVoltageVolt]
                                      ,[totalVoltagePt]
                                      ,[numMeasVoltage]
                                      ,[numTxElements]
                                      ,[txpgWaveformStyle]
                                      ,[numTxCycles]
                                      ,[elevAperIndex]
                                      ,[zStartDistCm]
                                      ,[zMeasNum]
                                      ,[IsTxAperModulationEn]
                                      ,[dumpSwVersion]
                                      ,[DTxFreqIndex]
                                      ,[VTxIndex]
                                      ,[IsCPAEn]
                                      ,[TxPulseRleA]
                                      ,[SysPulserSelA]
                                      ,[CpaDelayOffsetClkA]
                                      )
                                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                    '''

                    cursor.execute(query, (row.measSetComments, row.probeId, row.BeamStyleIndex, row.bsIndexTrace,
                                           row.TxFrequencyHz, row.TxFocusLocCm, row.maxTxVoltageVolt,
                                           row.ceilTxVoltageVolt,
                                           row.profTxVoltageVolt, row.totalVoltagePt, row.numMeasVoltage,
                                           row.NumTxElements,
                                           row.TxpgWaveformStyle, row.ProbeNumTxCycles, row.elevAperIndex,
                                           row.zStartDistCm,
                                           row.zMeasNum, row.IsTxChannelModulationEn, row.dumpSwVersion,
                                           row.DTxFreqIndex,
                                           row.VTxIndex, row.IsPresetCpaEn, row.TxPulseRle, row.SystemPulserSel,
                                           row.CpaDelayOffsetClk)
                                   )

                conn.commit()
                conn.close()

            except():
                print('error: func_insert_data')


        root_gen = tkinter.Toplevel()
        root_gen.title(f"{database}" + ' / MeasSet_generation')
        root_gen.geometry("600x200")
        root_gen.resizable(False, False)

        frame1 = Frame(root_gen, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)

        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        combo_probename = ttk.Combobox(frame1, value=list_probe, height=0, state='readonly')
        combo_probename.place(x=5, y=25)

        btn_load = Button(frame1, width=15, height=2, text='Select & Load', command=func_create_data)
        btn_load.place(x=185, y=5)

        btn_insert = Button(frame1, width=15, height=2, text='To MS-SQL', command=func_insert_data)
        btn_insert.place(x=325, y=5)

        frame2 = Frame(root_gen, relief="solid", bd=2)
        frame2.pack(side="bottom", fill="both", expand=True)

        #Labels
        label_DumpSW = Label(frame2, text="[dumpSwVersion]")
        label_DumpSW.grid(row=0, column=0)

        label_MaxVolt = Label(frame2, text="[maxTxVoltageVolt]")
        label_MaxVolt.grid(row=2, column=0)

        label_CeilVolt = Label(frame2, text="[ceilTxVoltageVolt]")
        label_CeilVolt.grid(row=2, column=1)

        label_TotalVoltpt = Label(frame2, text="[totalVoltagePt]")
        label_TotalVoltpt.grid(row=2, column=2)

        label_NumMeasVolt = Label(frame2, text="[numMeasVoltage]")
        label_NumMeasVolt.grid(row=2, column=3)

        #Entry boxes
        box_DumpSW = Entry(frame2, justify='center')
        box_DumpSW.grid(row=1, column=0)

        box_MaxVolt = Entry(frame2, justify='center')
        box_MaxVolt.grid(row=3, column=0)

        box_CeilVolt = Entry(frame2, justify='center')
        box_CeilVolt.grid(row=3, column=1)

        box_TotalVoltpt = Entry(frame2, justify='center')
        box_TotalVoltpt.grid(row=3, column=2)

        box_NumMeasVolt = Entry(frame2, justify='center')
        box_NumMeasVolt.grid(row=3, column=3)

        root_gen.mainloop()

    except:
        print("Error: measset_gen")


def func_tx_sum():
    try:
        filename = filedialog.askopenfilename(initialdir='.txt')
        df_UE_Tx_sum = pd.read_csv(filename, sep='\t', encoding='cp949')
        ## mode, BeamStyle, TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE
        df_first = df_UE_Tx_sum.iloc[:, [2, 4, 5, 6, 7, 8, 9, 10]]

        df = df_first.drop_duplicates()
        df_D_mode = df.loc[(df['BeamStyleIndex'] == 10) & (df['ProbeNumTxCycles'] == 4)]
        df_Others_mode = df.loc[df['BeamStyleIndex'] != 10]

        df_D_mode = df_D_mode.drop_duplicates(['Mode', 'BeamStyleIndex', 'TxFreqIndex', 'TxFrequency', 'ProbeNumElevAper', 'TxpgWaveformStyle', 'TxChannelModulationEn'])
        df_Others_mode = df_Others_mode.drop_duplicates()
        df_final_mode = pd.concat([df_Others_mode, df_D_mode])                                                          ## 2개 데이터프레임 합치기
        df_final_mode = df_final_mode.reset_index(drop=True)                                                            ## 데이터프레임 index reset
        df_final_mode = df_final_mode.sort_values(
            by=[df_final_mode.columns[0], df_final_mode.columns[1], df_final_mode.columns[2], df_final_mode.columns[4],
                df_final_mode.columns[6]], ascending=True)

        func_show_table('Tx_summary', df_final_mode)


    except:
        print("Error: Tx_Summary")


def func_machine_learning():
    try:
        def func_modelML(selected_ML, data, target):
            try:
                def func_feature_import():
                    try:
                        df_import = pd.DataFrame()
                        df_import = df_import.append(pd.DataFrame([np.round((model.feature_importances_) * 100, 2)],
                                                                  columns=['txFrequencyHz', 'focusRangeCm',
                                                                           'numTxElements',
                                                                           'txpgWaveformStyle',
                                                                           'numTxCycles', 'elevAperIndex',
                                                                           'IsTxAperModulationEn', 'probePitchCm',
                                                                           'probeRadiusCm', 'probeElevAperCm0',
                                                                           'probeElevFocusRangCm']), ignore_index=True)

                        func_show_table(f'{selected_ML}', df=df_import)

                        importances = model.feature_importances_
                        indices = np.argsort(importances)[::-1]
                        x = np.arange(len(importances))

                        import matplotlib.pyplot as plt
                        plt.title('Feature Importance')
                        plt.bar(x, importances[indices], align='center')
                        labels = df_import.columns

                        plt.xticks(x, labels[indices], rotation=90)
                        plt.xlim([-1, len(importances)])
                        plt.tight_layout()
                        plt.show()

                    except():
                        print('func_feature_import')


                train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2)

                ## 왼쪽 공백 삭제
                selected_ML = selected_ML.lstrip()

                ## Random Forest 훈련하기.
                if selected_ML == 'RandomForestRegressor':
                    from sklearn.ensemble import RandomForestRegressor
                    from sklearn.model_selection import GridSearchCV
                    from sklearn.model_selection import RandomizedSearchCV
                    from scipy.stats import uniform, randint


                    ## hyperparameter 세팅 시, 진행.
                    # n_estimators = randint(20, 100)                 ## number of trees in the random forest
                    # max_features = ['auto', 'sqrt']                 ## number of features in consideration at every split
                    # max_depth = [int(x) for x in
                    #              np.linspace(10, 120, num=12)]      ## maximum number of levels allowed in each decision tree
                    # min_samples_split = [2, 6, 10]                  ## minimum sample number to split a node
                    # # min_samples_leaf = [1, 3, 4]                  ## minimum sample number that can be stored in a leaf node
                    # # bootstrap = [True, False]                     ## method used to sample data points
                    #
                    # random_grid = {'n_estimators': n_estimators,
                    #                'max_features': max_features,
                    #                'max_depth': max_depth,
                    #                'min_samples_split': min_samples_split}
                    #
                    #                # 'min_samples_leaf': min_samples_leaf,
                    #                # 'bootstrap': bootstrap}
                    ## RandomizedSearchCV에서 fit이 완료.
                    # rf = RandomForestRegressor()
                    # model = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,
                    #                             n_iter = 300, cv = 5, verbose=2, n_jobs = -1)


                    # After hyperparameter value find, adapt these ones.
                    model = RandomForestRegressor(max_depth=40, max_features='sqrt', min_samples_split=2, n_estimators=90, n_jobs=-1)


                ## Gradient Boosting
                elif selected_ML == 'Gradient_Boosting':
                    from sklearn.ensemble import GradientBoostingRegressor
                    model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.2)


                ## Histogram-based Gradient Boosting
                elif selected_ML == 'Histogram-based Gradient Boosting':
                    from sklearn.experimental import enable_hist_gradient_boosting
                    from sklearn.ensemble import HistGradientBoostingRegressor
                    model = HistGradientBoostingRegressor()


                elif selected_ML == 'XGBoost':
                    from xgboost import XGBRegressor
                    model = XGBRegressor(tree_method='hist')


                ## VotingRegressor 훈련하기
                ## Need to update....
                elif selected_ML == 'VotingRegressor':
                    from sklearn.ensemble import VotingRegressor
                    from sklearn.linear_model import Ridge
                    from sklearn.ensemble import RandomForestRegressor
                    from sklearn.neighbors import KNeighborsRegressor

                    from sklearn.pipeline import make_pipeline

                    from sklearn.preprocessing import PolynomialFeatures
                    poly = PolynomialFeatures(degree=5, include_bias=False)
                    poly.fit(train_input)
                    train_poly = poly.transform(train_input)
                    test_poly = poly.transform(test_input)

                    from sklearn.preprocessing import StandardScaler
                    ss = StandardScaler()
                    ss.fit(train_poly)
                    train_scaled = ss.transform(train_poly)
                    test_scaled = ss.transform(test_poly)


                    model1 = Ridge(alpha=0.1)
                    model2 = RandomForestRegressor(n_jobs=-1)
                    model3 = KNeighborsRegressor()

                    model = VotingRegressor(estimators=[('ridge', model1), ('random', model2), ('neigh', model3)])


                ## LinearRegression 훈련하기.
                elif selected_ML == 'LinearRegression':

                    from sklearn.preprocessing import StandardScaler
                    ss = StandardScaler()
                    ss.fit(train_input)
                    train_scaled = ss.transform(train_input)
                    test_scaled = ss.transform(test_input)

                    from sklearn.linear_model import LinearRegression
                    model = LinearRegression()


                    ## PolynomialFeatures 데이터를 train_input / test_input에 넣어서 아래 common에 입력
                    train_input = train_scaled
                    test_input = test_scaled


                ## StandardScaler 적용 with linear regression
                elif selected_ML == 'PolynomialFeatures with linear regression':

                    from sklearn.preprocessing import PolynomialFeatures
                    poly = PolynomialFeatures(degree=3, include_bias=False)
                    poly.fit(train_input)
                    train_poly = poly.transform(train_input)
                    test_poly = poly.transform(test_input)

                    from sklearn.preprocessing import StandardScaler
                    ss = StandardScaler()
                    ss.fit(train_poly)
                    train_scaled = ss.transform(train_poly)
                    test_scaled = ss.transform(test_poly)

                    from sklearn.linear_model import LinearRegression
                    model = LinearRegression()

                    ## PolynomialFeatures 데이터를 train_input / test_input에 넣어서 아래 common에 입력
                    train_input = train_scaled
                    test_input = test_scaled


                ## Ridge regularization(L2 regularization)
                elif selected_ML == 'Ridge regularization(L2 regularization)':

                    from sklearn.preprocessing import PolynomialFeatures
                    poly = PolynomialFeatures(degree=3, include_bias=False)
                    poly.fit(train_input)
                    train_poly = poly.transform(train_input)
                    test_poly = poly.transform(test_input)

                    from sklearn.preprocessing import StandardScaler
                    ss = StandardScaler()
                    ss.fit(train_poly)
                    train_scaled = ss.transform(train_poly)
                    test_scaled = ss.transform(test_poly)

                    from sklearn.linear_model import Ridge
                    model = Ridge(alpha=0.1)

                    ## PolynomialFeatures 데이터를 train_input / test_input에 넣어서 아래 common에 입력
                    train_input = train_scaled
                    test_input = test_scaled


                    ## L2 하이퍼파라미터 찾기
                    train_score = []
                    test_score = []

                    alpha_list = [0.001, 0.01, 0.1, 1, 10, 100]
                    import matplotlib.pyplot as plt
                    for alpha in alpha_list:
                        # 릿지모델 생성 & 훈련
                        model = Ridge(alpha=alpha)
                        model.fit(train_scaled, train_target)
                        # 훈련점수 & 테스트점수
                        train_score.append(model.score(train_scaled, train_target))
                        test_score.append(model.score(test_scaled, test_target))

                    plt.plot(np.log10(alpha_list), train_score)
                    plt.plot(np.log10(alpha_list), test_score)
                    plt.xlabel('alpha')
                    plt.ylabel('R^2')
                    plt.show()


                elif selected_ML == 'DecisionTreeRegressor(scaled data)':

                    from sklearn.tree import DecisionTreeRegressor
                    model = DecisionTreeRegressor(max_depth=10, random_state=42)

                    from sklearn.preprocessing import StandardScaler
                    ss = StandardScaler()
                    ss.fit(train_input)
                    train_scaled = ss.transform(train_input)
                    test_scaled = ss.transform(test_input)

                    model.fit(train_scaled, train_target)

                    scores = cross_validate(model, train_scaled, train_target, return_train_score=True, n_jobs=-1)
                    print()
                    print(scores)
                    print('결정트리 - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
                    print('결정트리 - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

                    # dt.fit(train_scaled, train_target)
                    print('결정트리 - Test R^2:', np.round_(model.score(test_scaled, test_target), 3))
                    prediction = model.predict(test_scaled)

                    df_import = pd.DataFrame()
                    df_import = df_import.append(pd.DataFrame([np.round((model.feature_importances_) * 100, 2)],
                                                              columns=['txFrequencyHz', 'focusRangeCm', 'numTxElements',
                                                                       'txpgWaveformStyle',
                                                                       'numTxCycles', 'elevAperIndex',
                                                                       'IsTxAperModulationEn', 'probePitchCm',
                                                                       'probeRadiusCm', 'probeElevAperCm0',
                                                                       'probeElevFocusRangCm']), ignore_index=True)

                    func_show_table('DecisionTreeRegressor', df=df_import)

                    ## plot_tree 이용하여 어떤 트리가 생성되었는지 확인.
                    import matplotlib.pyplot as plt
                    from sklearn.tree import plot_tree
                    plt.figure(figsize=(10, 7))
                    plot_tree(model, max_depth=2, filled=True,
                              feature_names=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle',
                                             'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                             'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm'])
                    plt.show()


                elif selected_ML == 'DecisionTreeRegressor(No scaled data)':

                    from sklearn.tree import DecisionTreeRegressor
                    model = DecisionTreeRegressor(max_depth=10, random_state=42)
                    model.fit(train_input, train_target)

                    func_feature_import()

                    ## plot_tree 이용하여 어떤 트리가 생성되었는지 확인.
                    import matplotlib.pyplot as plt
                    from sklearn.tree import plot_tree
                    plt.figure(figsize=(10, 7))
                    plot_tree(model, max_depth=1, filled=True,
                              feature_names=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle',
                                             'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                             'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm'])
                    plt.show()


                elif selected_ML == 'DL_DNN':
                    import tensorflow as tf
                    from tensorflow import keras

                    from sklearn.preprocessing import StandardScaler
                    ss = StandardScaler()
                    ss.fit(train_input)
                    train_scaled = ss.transform(train_input)
                    test_scaled = ss.transform(test_input)


                    def func_build_model():
                        dense1 = keras.layers.Dense(100, activation='relu', input_shape=(11,), name='hidden')
                        dense2 = keras.layers.Dense(10, activation='relu')
                        dense3 = keras.layers.Dense(1)

                        model = keras.Sequential([dense1, dense2, dense3])

                        optimizer = tf.keras.optimizers.RMSprop(0.001)

                        model.compile(loss='mse',
                                      optimizer=optimizer,
                                      metrics=['mae', 'mse'])
                        return model

                    model = func_build_model()
                    print(model.summary())

                    example_batch = train_scaled[:10]
                    example_result = model.predict(example_batch)
                    print('example_batch 형태:', example_batch.shape)


                    import matplotlib.pyplot as plt

                    def plot_history(history):
                        hist = pd.DataFrame(history.history)
                        hist['epoch'] = history.epoch

                        plt.figure(figsize=(8, 12))

                        plt.subplot(2, 1, 1)
                        plt.xlabel('Epoch')
                        plt.ylabel('Mean Abs Error [Cm]')
                        plt.plot(hist['epoch'], hist['mae'],
                                 label='Train Error')
                        plt.plot(hist['epoch'], hist['val_mae'],
                                 label='Val Error')
                        plt.ylim([0, 1.25])
                        plt.legend()

                        plt.subplot(2, 1, 2)
                        plt.xlabel('Epoch')
                        plt.ylabel('Mean Square Error [$Cm^2$]')
                        plt.plot(hist['epoch'], hist['mse'],
                                 label='Train Error')
                        plt.plot(hist['epoch'], hist['val_mse'],
                                 label='Val Error')
                        plt.ylim([0, 2])
                        plt.legend()
                        plt.show()

                    ## 모델 훈련.
                    ## 에포크가 끝날 때마다 점(.)을 출력해 훈련 진행 과정을 표시합니다
                    class PrintDot(keras.callbacks.Callback):
                        def on_epoch_end(self, epoch, logs):
                            if epoch % 100 == 0: print('')
                            print('.', end='')

                    EPOCHS = 1000

                    model = func_build_model()

                    # patience 매개변수는 성능 향상을 체크할 에포크 횟수입니다
                    early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
                    history = model.fit(train_scaled, train_target, epochs=EPOCHS, validation_split=0.2, verbose=0,
                                        callbacks=[early_stop, PrintDot()])

                    hist = pd.DataFrame(history.history)
                    hist['epoch'] = history.epoch
                    print(hist.tail())

                    plot_history(history)

                    loss, mae, mse = model.evaluate(test_scaled, test_target, verbose=2)
                    print("테스트 세트의 평균 절대 오차: {:5.2f} Cm".format(mae))


                    ## 테스트 세트에 있는 샘플을 사용해 zt 값을 예측하여 비교하기.
                    test_predictions = model.predict(test_scaled).flatten()
                    print(test_predictions)
                    print(test_target)

                    import matplotlib.pyplot as plt
                    plt.scatter(test_target, test_predictions)

                    plt.xlabel('True Values [Cm]')
                    plt.ylabel('Predictions [Cm]')
                    plt.axis('equal')
                    plt.axis('square')
                    plt.xlim([0, plt.xlim()[1]])
                    plt.ylim([0, plt.ylim()[1]])
                    _ = plt.plot([-100, 100], [-100, 100])
                    plt.show()


                    ## 오차의 분표확인.
                    error = test_predictions - test_target
                    plt.hist(error, bins=25)
                    plt.xlabel('Prediction Error [Cm]')
                    _ = plt.ylabel('Count')
                    plt.show()


                elif selected_ML == 'DNN_HonGong':
                    import tensorflow as tf
                    from tensorflow import keras
                    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

                    # train_target 분포 확인.
                    import seaborn as sns
                    import matplotlib.pyplot as plt
                    plt.title('Distport for zt')
                    sns.distplot(train_target)
                    plt.show()

                    from sklearn.preprocessing import StandardScaler
                    ss = StandardScaler()
                    ss.fit(train_input)
                    train_scaled = ss.transform(train_input)
                    test_scaled = ss.transform(test_input)

                    def model_fn(a_layer=None):
                        model = keras.Sequential()
                        model.add(keras.layers.Flatten(input_shape=(11,), name='input'))
                        model.add(keras.layers.Dense(100, activation='relu', name='hidden1'))
                        model.add(keras.layers.Dense(10, activation='relu', name='hidden2'))

                        ## add layer algorithm
                        if a_layer:
                            model.add(a_layer)

                        model.add(keras.layers.Dense(1, name='output'))

                        return model


                    ## To build model fn
                    ## To prevent overfitting for ML algorithm(method: dropout)
                    # model = model_fn(keras.layers.Dropout(0.3))
                    model = model_fn()
                    print(model.summary())

                    rmsprop = keras.optimizers.RMSprop(0.001)
                    model.compile(optimizer=rmsprop, loss='mse', metrics=['mae', 'mse'])

                    checkpoint_cb = keras.callbacks.ModelCheckpoint('best-model.h5')
                    early_stopping_cb = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
                    history = model.fit(train_scaled, train_target, epochs=1000, validation_split=0.2, callbacks=[checkpoint_cb, early_stopping_cb])

                    print()
                    print('#Num of early_stopping:', early_stopping_cb.stopped_epoch)

                    hist = pd.DataFrame(history.history)
                    hist['epoch'] = history.epoch
                    print(hist.tail())


                    import matplotlib.pyplot as plt
                    plt.plot(history.history['loss'])
                    plt.plot(history.history['val_loss'])
                    plt.xlabel('epoch')
                    plt.ylabel('loss')
                    plt.legend(['train', 'val'])
                    plt.show()

                    plt.plot(history.history['mae'])
                    plt.plot(history.history['val_mae'])
                    plt.xlabel('epoch')
                    plt.ylabel('mae')
                    plt.legend(['train', 'val'])
                    plt.show()


                    import numpy as np
                    model = keras.models.load_model('best-model.h5')
                    print()
                    print('<Test evaluate>')
                    loss, mae, mse = model.evaluate(test_scaled, test_target, verbose=2)
                    print('Test evaluate:', model.evaluate(test_scaled, test_target))
                    print("테스트 세트의 평균 절대 오차: {:5.2f} Cm".format(mae))


                    prediction = model.predict(test_scaled).flatten()


                    import numpy as np
                    prediction = np.around(prediction, 2)
                    # prediction = {:.2f}.format(prediction)
                    df = pd.DataFrame(prediction, test_target)
                    print('[csv 파일 추출 완료]')
                    df.to_csv('test_est.csv')

                    import matplotlib.pyplot as plt
                    plt.scatter(test_target, prediction)
                    plt.xlabel('True Values [Cm]')
                    plt.ylabel('Predictions [Cm]')
                    plt.axis('equal')
                    plt.axis('square')
                    plt.xlim([0, plt.xlim()[1]])
                    plt.ylim([0, plt.ylim()[1]])
                    _ = plt.plot([-10, 10], [-10, 10])
                    plt.show()

                    ## 오차의 분표확인.
                    Error = prediction - test_target
                    plt.hist(Error, bins=25)
                    plt.xlabel('Prediction Error [Cm]')
                    _ = plt.ylabel('Count')
                    plt.show()


                if "DNN" in selected_ML:
                    pass

                else:
                    ## modeling file 저장 장소.
                    newpath = './Model'
                    if not os.path.exists(newpath):
                        os.makedirs(newpath)
                    joblib.dump(model, f'Model/{selected_ML}_v1_python37.pkl')


                    scores = cross_validate(model, train_input, train_target, return_train_score=True, n_jobs=-1)
                    print()
                    print(scores)
                    import numpy as np
                    print(f'{selected_ML} - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
                    print(f'{selected_ML} - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

                    model.fit(train_input, train_target)
                    print(f'{selected_ML} - Test R^2:', np.round_(model.score(test_input, test_target), 3))
                    prediction = np.round_(model.predict(test_input), 2)

                    if selected_ML == 'RandomForestRegressor':
                        func_feature_import()
                    else:
                        pass


                mae = mean_absolute_error(test_target, prediction)
                print('|(타깃 - 예측값)|:', mae)

                Diff = np.round_(prediction - test_target, 2)
                Diff_per = np.round_((test_target - prediction) / test_target * 100, 1)


                bad = 0
                good = 0
                print()

                df_bad = pd.DataFrame()
                failed_condition = pd.DataFrame()

                df = pd.DataFrame()
                pass_condition = pd.DataFrame()


                # df_test_input = pd.DataFrame(test_input, columns=['txFrequencyHz',
                #                                                                          'focusRangeCm',
                #                                                                          'numTxElements',
                #                                                                          'txpgWaveformStyle',
                #                                                                          'numTxCycles',
                #                                                                          'elevAperIndex',
                #                                                                          'IsTxAperModulationEn',
                #                                                                          'probePitchCm',
                #                                                                          'probeRadiusCm',
                #                                                                          'probeElevAperCm0',
                #                                                                          'probeElevFocusRangCm'])
                #
                # func_show_table('test_input', df=df_test_input)

                for i in range(len(Diff)):
                    if abs(Diff[i]) > 1:
                        bad = bad + 1

                        df_bad = df_bad.append(pd.DataFrame([[i, test_target[i], prediction[i], Diff[i], Diff_per[i]]],
                                                            columns=['index', '측정값(Cm)', '예측값(Cm)', 'Diff(Cm)', 'Diff(%)']),
                                               ignore_index=True)
                        # df_bad_sort_values = df_bad.sort_values(by=df_bad.columns[3], ascending=True)
                        # df_bad_sort_values = df_bad_sort_values.reset_index(drop=True)

                        failed_condition = failed_condition.append(pd.DataFrame([test_input[i]],
                                                                                columns=['txFrequencyHz',
                                                                                         'focusRangeCm',
                                                                                         'numTxElements',
                                                                                         'txpgWaveformStyle',
                                                                                         'numTxCycles',
                                                                                         'elevAperIndex',
                                                                                         'IsTxAperModulationEn',
                                                                                         'probePitchCm',
                                                                                         'probeRadiusCm',
                                                                                         'probeElevAperCm0',
                                                                                         'probeElevFocusRangCm']),
                                                                   ignore_index=True)


                    else:
                        good = good + 1

                        df = df.append(pd.DataFrame([[i, test_target[i], prediction[i], Diff[i], Diff_per[i]]],
                                                    columns=['index', 'target', 'expect', 'Diff(Cm)', 'Diff(%)']),
                                       ignore_index=True)
                        # df_sort_values = df.sort_values(by=df.columns[3], ascending=True)
                        # df_sort_values = df_sort_values.reset_index(drop=True)

                        pass_condition = pass_condition.append(pd.DataFrame([test_input[i]],
                                                                            columns=['txFrequencyHz',
                                                                                     'focusRangeCm',
                                                                                     'numTxElements',
                                                                                     'txpgWaveformStyle',
                                                                                     'numTxCycles',
                                                                                     'elevAperIndex',
                                                                                     'IsTxAperModulationEn',
                                                                                     'probePitchCm',
                                                                                     'probeRadiusCm',
                                                                                     'probeElevAperCm0',
                                                                                     'probeElevFocusRangCm']),
                                                               ignore_index=True)

                print()
                print('bad:', bad)
                print('good:', good)

                merge_bad_inner = pd.concat([df_bad, failed_condition], axis=1)
                merge_good_inner = pd.concat([df, pass_condition], axis=1)

                ## failed condition show-up
                func_show_table("failed_condition",
                                df=merge_bad_inner if len(merge_bad_inner.index) > 0 else None)

                func_show_table("pass_condition",
                                df=merge_good_inner if len(merge_good_inner.index) > 0 else None)

            except():
                print('error: func_modelML')


        def func_preprocessML():
            try:
                print(list_database)

                ## K2, Juniper, NX3, NX2 and FROSK
                for i in list_database:
                    print(i)
                    conn = pymssql.connect(server_address, ID, password, database=i)

                    query = f'''
                                     SELECT * FROM
                                     (
                                     SELECT a.[measSetId]
                                     ,a.[probeId]
                                     ,a.[beamstyleIndex]
                                     ,a.[txFrequencyHz]
                                     ,a.[focusRangeCm]
                                     ,a.[numTxElements]
                                     ,a.[txpgWaveformStyle]
                                     ,a.[numTxCycles]
                                     ,a.[elevAperIndex]
                                     ,a.[IsTxAperModulationEn]
                                     ,d.[probeName]
                                     ,d.[probePitchCm]
                                     ,d.[probeRadiusCm]
                                     ,d.[probeElevAperCm0]
                                     ,d.[probeElevFocusRangCm]
        --                              ,d.[probeElevFocusRangCm1]
                                     ,b.[measResId]
                                     ,b.[zt]
                                     ,ROW_NUMBER() over (partition by a.measSetId order by b.measResId desc) as RankNo
                                     FROM meas_setting AS a
                                     LEFT JOIN meas_res_summary AS b
                                         ON a.[measSetId] = b.[measSetId]
                                     LEFT JOIN meas_station_setup AS c
                                         ON b.[measSSId] = c.[measSSId]
                                     LEFT JOIN probe_geo AS d
                                         ON a.[probeId] = d.[probeId]
                                     where b.[isDataUsable] ='yes' and c.[measPurpose] like '%Beamstyle%' and b.[errorDataLog] = ''
                                     ) T
                                     where RankNo = 1
                                     order by 1
                                     '''

                    Raw_data = pd.read_sql(sql=query, con=conn)
                    print(Raw_data['probeName'].value_counts(dropna=False))
                    AOP_data = Raw_data.dropna()
                    AOP_data = AOP_data.append(AOP_data, ignore_index=True)

                # AOP_data.to_csv('AOP_data.csv')

                data = AOP_data[['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles',
                                 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                 'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm']].to_numpy()
                target = AOP_data['zt'].to_numpy()

                # Machine Learning
                func_modelML(combo_ML.get(), data, target)

            except:
                print("Error: func_preprocessML")


        root_ML = tkinter.Toplevel()
        root_ML.title(f"{database}" + ' / Machine Learning')
        root_ML.geometry("410x200")
        root_ML.resizable(False, False)

        frame1 = Frame(root_ML, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)

        label_ML = Label(frame1, text='Machine Learning')
        label_ML.place(x=5, y=5)
        combo_ML = ttk.Combobox(frame1, value=list_ML, width=35, height=0, state='readonly')
        combo_ML.place(x=5, y=25)

        btn_load = Button(frame1, width=15, height=2, text='Select & Train', command=func_preprocessML)
        btn_load.place(x=280, y=5)

        root_ML.mainloop()


    except():
        print("Error: Machine_Learning")


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


        btn_gen = Button(root_main, width=30, height=3, text='MeasSetGeneration', command=func_measset_gen)
        btn_gen.grid(row=0, column=0)

        btn_sum = Button(root_main, width=30, height=3, text='SQL Viewer', command=func_viewer_database)
        btn_sum.grid(row=0, column=1)

        btn_tx_sum = Button(root_main, width=30, height=3, text='Tx Summary', command=func_tx_sum)
        btn_tx_sum.grid(row=1, column=0)

        btn_ML = Button(root_main, width=30, height=3, text='Machine Learning', command=func_machine_learning)
        btn_ML.grid(row=1, column=1)

        root_main.mainloop()

    except:
        print("Error: main")


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