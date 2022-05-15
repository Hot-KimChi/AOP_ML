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
        # df_sort_B = df_B_mode.sort_values(by=[df_B_mode.columns[0], df_B_mode.columns[1], df_B_mode.columns[2], df_B_mode.columns[5], df_B_mode.columns[3]], ascending=True)
        df_B_mode = df_first.loc[(df_first['BeamStyleIndex'] == 0) | (df_first['BeamStyleIndex'] == 1)]
        # B_num = df_sort_B['TxFocusLocCm'].nunique()
        # df_sort_M = df_M_mode.sort_values(by=[df_M_mode.columns[0], df_M_mode.columns[1], df_M_mode.columns[2], df_M_mode.columns[5], df_M_mode.columns[3]], ascending=True)
        df_M_mode = df_first.loc[(df_first['BeamStyleIndex'] == 15) | (df_first['BeamStyleIndex'] == 20)]

        df = pd.concat([df_B_mode, df_M_mode])      ## 2개 데이터프레임 합치기
        df = df.reset_index(drop=True)              ## 데이터프레임 index reset

        ##  ----------------------------
        ##  duplicated parameter check.
        #
        # dup = df.duplicated(['SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'TxPulseRle'], keep='first')
        # df_dup = pd.concat([df, dup], axis=1)
        # df_dup.rename(columns={0:'Dup'}, inplace=True)
        # df_dup = df_dup.sort_values(by=[df_dup.columns[6], df_dup.columns[1], df_dup.columns[2], df_dup.columns[5],
        #                 df_dup.columns[9], df_dup.columns[0], df_dup.columns[3], df_dup.columns[4]], ascending=True)
        # print(df_dup)
        # count = df_dup[['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 'BeamStyleIndex']].value_counts(sort=False)
        # print(count)
        # print(count.index)
        #
        ##  End
        ##  ----------------------------


        ## 데이터프레임 columns name 추출('SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'IsPresetCpaEn', 'CpaDelayOffsetClk', 'TxPulseRle')
        col = list(df.columns)[1:10]
        ## columns name으로 정렬(TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE)
        df_grp = df.groupby(['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 'TxPulseRle']).size().reset_index().rename(columns={0:'count'})
        print(type(df_grp))
        print(df_grp)

        # df_dic = df_grp.groups  ## groupby 객체의 groups 변수 --> 딕셔너리형태로 키값과 인덱스로 구성.
        # print(df_dic.keys())
        # idx = [x[0] for x in df_dic.values() if len(x) == 1]
        # df = df.reindex(idx) if len(df.reindex(idx).index) > 0 else None

        # func_show_table(df=df_dup)
        func_show_table(df=df_grp)

    except:
        print('error: create data')


if __name__ == '__main__':
    func_create_data()