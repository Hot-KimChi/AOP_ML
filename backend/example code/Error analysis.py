import tkinter

import pandas as pd
import numpy as np
import pymssql
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import seaborn as sns
from functools import partial


## SQL데이터 DataFrame을 이용하여 Treeview에 기록하여 출력.
def func_show_table(selected_DBtable=None, df=None, extra=None):
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
              background=[('selected', 'black')])

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

    n_root.mainloop()




## SQL 데이터 가져오기
server_address = 'kr001s1804srv'
ID = 'sel02776'
password = '1qaz!QAZ'
database = 'Griffin_r01'


conn = pymssql.connect(server_address, ID, password, database)

sel_measSSId = 895
query = f'''
                        SELECT * FROM
                        (
                        SELECT a.[wcsID] 
                        ,a.[mode]
                        ,a.[probeId]
                        ,a.[ScanRangeCM]
                        ,a.[Voltage]
                        ,a.[TxFrequencyHz]
                        ,a.[FocusRangeCm]
                        ,a.[WaveformStyle]
                        ,a.[NumTxCycles]
                        ,a.[NumTxElements]
                        ,a.[ChModulationEn]
                        ,b.[reportTerm_1]
                        ,b.[XP_Value_1]
                        ,b.[reportValue_1]
                        ,b.[Difference_1]
                        ,b.[Ambient_Temp_1]
                        ,b.[reportdate]

                        ,d.[probeName]
                        ,d.[probePitchCm]
                        ,d.[probeRadiusCm]
                        ,d.[probeElevAperCm0]
                        ,d.[probeElevFocusRangCm]
                        ,d.[probeDescription]
--                         ,b.[measResId]
--                         ,b.[zt]
                        ,ROW_NUMBER() over (partition by a.wcsID order by b.SSRId desc) as RankNo
                        FROM WCS AS a
                        LEFT JOIN SSR_table AS b
                            ON a.[wcsID] = b.[WCSId]
--                         LEFT JOIN meas_station_setup AS c
--                             ON b.[measSSId] = c.[measSSId]
                        LEFT JOIN probe_geo AS d
                            ON a.[probeId] = d.[probeId]
                        where b.[reportTerm_1] like '%temp%' and b.[measSSID] = {sel_measSSId}
                        ) T
--                         b.[measSSId] = 987 or 
                        where RankNo = 1
                        order by 1
                        '''

Raw_data = pd.read_sql(sql=query, con=conn)
print(Raw_data['probeName'].value_counts(dropna=False))
AOP_data = Raw_data.dropna()

sns.catplot(data=AOP_data, x='ScanRangeCM', y='Difference_1', aspect=4)
sns.catplot(data=AOP_data, x='NumTxElements', y='Difference_1', aspect=4)
sns.catplot(data=AOP_data, x='Voltage', y='Difference_1', aspect=4)
sns.catplot(data=AOP_data, x='TxFrequencyHz', y='Difference_1', aspect=4)
sns.catplot(data=AOP_data, x='reportdate', y='Difference_1', aspect=4)

plt.show()


## Start tk 만들기.
root = Tk()
root.title("DB 선택")
root.geometry("280x150")
root.resizable(False, False)

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

label1 = Label(root, text='데이터베이스를 선택하세요')
label1.place(x=10, y=10)

btn_login = Button(root, width=10, height=2, text='Login', command=partial(func_show_table, '12', df=AOP_data))
btn_login.place(x=180, y=10)



root.mainloop()

# func_show_table('Error', df=AOP_data)