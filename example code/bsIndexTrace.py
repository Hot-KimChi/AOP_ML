import tkinter
from tkinter import filedialog
import pandas as pd
from tkinter import *
from tkinter import ttk

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def func_show_table(df):
    try:
        n_root = Tk()
        n_root.title("bsIndexTrace")
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

        n_root.mainloop()
    except:
        print('error: show table')


def func_create_data():
    try:
        filename = filedialog.askopenfilename(initialdir='.txt')
        df_UEdata = pd.read_csv(filename, sep='\t', encoding='cp949')
        ## BeamStyle, TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE
        df_first = df_UEdata.iloc[:, [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]

        ########################
        ## B & M mode process ##
        df_B_mode = df_first.loc[(df_first['BeamStyleIndex'] == 0) | (df_first['BeamStyleIndex'] == 1)]
        df_M_mode = df_first.loc[(df_first['BeamStyleIndex'] == 15) | (df_first['BeamStyleIndex'] == 20)]
        df_C_mode = df_first.loc[df_first['BeamStyleIndex'] == 5]
        df_D_mode = df_first.loc[df_first['BeamStyleIndex'] == 10]

        df = pd.concat([df_B_mode, df_M_mode, df_C_mode, df_D_mode])        ## 2개 데이터프레임 합치기
        df = df.reset_index(drop=True)                                      ## 데이터프레임 index reset
        df = df.fillna(0)                                                   ## 데이터 Null --> [0]으로 변환.(데이터의 정렬, groupby등)

        list_params = ['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 'TxPulseRle', 'TxFocusLocCm', 'NumTxElements']
        ## groupby로 중복 count.
        dup_count = df.groupby(by=list_params, as_index=False).count()


        ##  duplicated parameter check. => dup = df.duplicated(['SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'TxPulseRle'], keep='first')
        dup = df.drop_duplicates(list_params)
        sort_dup = dup.sort_values(by=list_params, ascending=True).reset_index()

        ## bsIndexTrace list만들어서 2개 DataFrame에서 zip으로 for문.
        bsIndexTrace = []
        for beam, cnt in zip(sort_dup['BeamStyleIndex'], dup_count['BeamStyleIndex']):
            if beam == 0 and cnt == 2:
                bsIndexTrace.append(15)
            elif beam == 1 and cnt == 2:
                bsIndexTrace.append(20)
            elif beam == 5 and cnt == 2:
                bsIndexTrace.append(10)
            else:
                bsIndexTrace.append(0)
        sort_dup['bsIndexTrace'] = bsIndexTrace
        print(sort_dup)

        ## function: calc_profTxVoltage 구현
        def func_profvolt():
            try:
                max, ceil, totalp, nump = 90, 90, 15, 10

                list_profTxVoltageVolt = []
                for i in range(nump):
                    list_profTxVoltageVolt.append(round((min(max, ceil)) ** ((totalp-1-i)/(totalp-1)), 2))
                profTxVoltageVolt = list_profTxVoltageVolt[2]
                print(max, ceil, totalp, profTxVoltageVolt)

            except():
                print('error: func_profvolt')


        ## function: calc zMeasNum 구현
        def func_zMeasNum():
            try:
                zStartDistCm = 0.5
                zMeasNum = []
                for focus in sort_dup['TxFocusLocCm']:
                    if(focus <= 3):
                        zMeasNum.append((5-zStartDistCm)*10)
                    elif(focus <= 6):
                        zMeasNum.append((8 - zStartDistCm) * 10)
                    elif(focus <= 9):
                        zMeasNum.append((12 - zStartDistCm) * 10)
                    else:
                        zMeasNum.append((14 - zStartDistCm) * 10)
                sort_dup['zMeasNum'] = zMeasNum
                print(sort_dup)


            except():
                print('error: func_zMeasNum')

        func_profvolt()
        func_zMeasNum()


        ## 데이터프레임 columns name 추출('SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'IsPresetCpaEn', 'CpaDelayOffsetClk', 'TxPulseRle')
        col = list(df.columns)[1:10]
        df_grp = df.groupby(['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 'TxPulseRle']).size().reset_index().rename(columns={0:'bsIdxTrace_Count'})
        df_grp = df_grp.sort_values(by=['IsTxChannelModulationEn', 'ProbeNumTxCycles', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'TxPulseRle'], ascending=True).reset_index()
        df_grp['index'] = df_grp.index
        print(df_grp)

        func_show_table(df=df_grp)

    except():
        print('error: create data')

if __name__ == '__main__':
    func_create_data()




    ## 아래 code 내것으로 만들기.
    # df_dic = df_grp.groups  ## groupby 객체의 groups 변수 --> 딕셔너리형태로 키값과 인덱스로 구성.
    # print(df_dic.keys())
    # idx = [x[0] for x in df_dic.values() if len(x) == 1]
    # df = df.reindex(idx) if len(df.reindex(idx).index) > 0 else None

    # # df_dup['bsIndexTrace'] = [15 if data == False else 0 for data in df_dup['Dup']]
    #
    # print(df_dup)

    # count = df_dup[['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 'BeamStyleIndex']].value_counts(sort=False).reset_index().rename(columns={0:'count'})
    # print(count)
    # print(count.index)
    #
    ##  End
    ##  ----------------------------

    # df_dup = pd.concat([df, dup], axis=1)
    # df_dup.rename(columns={0:'Dup'}, inplace=True)
    # df_dup = df_dup.sort_values(by=[df_dup.columns[6], df_dup.columns[1], df_dup.columns[2], df_dup.columns[5],
    #                 df_dup.columns[9], df_dup.columns[0], df_dup.columns[3], df_dup.columns[4]], ascending=True)
    # print(df_dup)


########################
                # ## B & M mode process ##
                # # df_sort_B = df_B_mode.sort_values(by=[df_B_mode.columns[0], df_B_mode.columns[1], df_B_mode.columns[2], df_B_mode.columns[5], df_B_mode.columns[3]], ascending=True)
                # df_B_mode = df_first.loc[(df_first['BeamStyleIndex'] == 0) | (df_first['BeamStyleIndex'] == 1)]
                # # B_num = df_sort_B['TxFocusLocCm'].nunique()
                # # df_sort_M = df_M_mode.sort_values(by=[df_M_mode.columns[0], df_M_mode.columns[1], df_M_mode.columns[2], df_M_mode.columns[5], df_M_mode.columns[3]], ascending=True)
                # df_M_mode = df_first.loc[(df_first['BeamStyleIndex'] == 15) | (df_first['BeamStyleIndex'] == 20)]
                #
                # df = pd.concat([df_B_mode, df_M_mode])      ## 2개 데이터프레임 합치기
                # df = df.reset_index(drop=True)              ## 데이터프레임 index reset
                # df = df.drop_duplicates()                   ## 중복된 데이터 삭제.
                #
                # refer_data = df.groupby(
                #     by=['BeamStyleIndex', 'SysTxFreqIndex', 'IsTxChannelModulationEn', 'TxpgWaveformStyle',
                #         'ProbeNumTxCycles'],
                #     as_index=False).count()
                # select_data = refer_data.iloc[:, [0, 1, 2, 3, 4, 5]]
                # select_data = select_data.sort_values(
                #     by=[select_data.columns[1], select_data.columns[2], select_data.columns[3], select_data.columns[4],
                #         select_data.columns[0]], ascending=True)
                #
                # ## 데이터프레임 columns name 추출('SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'IsPresetCpaEn', 'CpaDelayOffsetClk', 'TxPulseRle')
                # col = list(df.columns)[1:10]
                # ## columns name으로 정렬(TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE)
                # df_grp = df.groupby(col)
                # df_dic = df_grp.groups  ## groupby 객체의 groups 변수 --> 딕셔너리형태로 키값과 인덱스로 구성.
                # idx = [x[0] for x in df_dic.values() if len(x) == 1]
                #
                # func_show_table(selected_DBtable='Summary: B & M', df=select_data,
                #                 extra=df.reindex(idx) if len(df.reindex(idx).index) > 0 else None)
                #
                # BM_Not_same_cnt = len(df.reindex(idx))
                # print('B&M not same Count:', BM_Not_same_cnt)
                #
                # ########################
                # ## C & D mode process ##
                # df_C_mode = df_first.loc[df_first['BeamStyleIndex'] == 5]
                # df_D_mode = df_first.loc[df_first['BeamStyleIndex'] == 10]
                #
                # df = pd.concat([df_C_mode, df_D_mode])
                # df = df.reset_index(drop=True)
                # df = df.drop_duplicates()
                #
                # refer_data = df.groupby(
                #     by=['BeamStyleIndex', 'SysTxFreqIndex', 'IsTxChannelModulationEn', 'TxpgWaveformStyle',
                #         'ProbeNumTxCycles'],
                #     as_index=False).count()
                # select_data = refer_data.iloc[:, [0, 1, 2, 3, 4, 5]]
                #
                # select_data = select_data.sort_values(
                #     by=[select_data.columns[1], select_data.columns[2], select_data.columns[3], select_data.columns[4],
                #         select_data.columns[0]], ascending=True)
                #
                # col = list(df.columns)[1:11]
                # df_grp = df.groupby(col)
                # df_dic = df_grp.groups
                # idx = [x[0] for x in df_dic.values() if len(x) == 1]
                #
                # ## FutureWarning: elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison return op(a, b)
                # func_show_table(selected_DBtable='Summary: C & D', df=select_data,
                #                 extra=df.reindex(idx) if len(df.reindex(idx).index) > 0 else None)
                #
                # CD_Not_same_cnt = len(df.reindex(idx))
                # print('C&D not same Count:', CD_Not_same_cnt)