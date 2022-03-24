import pymssql
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import ttk
from functools import partial
import configparser
import warnings

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# warnings.simplefilter(action='ignore', category=FutureWarning)

## SQL데이터 DataFrame을 이용하여 Treeview에 기록하여 출력.
def func_show_table(selected_DBtable, df, extra):
    n_root = Tk()
    n_root.title(f"{database}  //  {selected_DBtable}")
    n_root.geometry("1000x800")

    frame1 = Frame(n_root, relief="solid", bd=2)
    frame1.pack(side="top", fill="both", expand=True, pady=10)


    my_tree = ttk.Treeview(frame1)

    # scrollbars
    vsb = Scrollbar(n_root, orient="vertical", command=my_tree.yview)
    vsb.place(relx=0.978, rely=0.175, relheight=0.713, relwidth=0.020)
    hsb = Scrollbar(n_root, orient="horizontal", command=my_tree.xview)
    hsb.place(relx=0.014, rely=0.875, relheight=0.020, relwidth=0.965)

    my_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    my_tree["column"] = list(df.columns)
    my_tree["show"] = "headings"

    # Loop thru column list for headers
    for column in my_tree["column"]:
        my_tree.column(column, width=80, minwidth=80)
        my_tree.heading(column, text=column)

    # Put data in treeview
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert("", "end", values=row)

    my_tree.pack()

    if extra != NONE:
        frame2 = Frame(n_root, relief="solid", bd=2)
        frame2.pack(side="bottom", fill="both", expand=True, pady=10)

        my_tree_extra = ttk.Treeview(frame2)
        my_tree_extra["column"] = list(extra.columns)
        my_tree_extra["show"] = "headings"

        # Loop thru column list for headers
        for column in my_tree_extra["column"]:
            my_tree_extra.column(column, width=150, minwidth=100)
            my_tree_extra.heading(column, text=column)

        # Put data in treeview
        df_rows = extra.to_numpy().tolist()
        for row in df_rows:
            my_tree_extra.insert("", "end", values=row)

        my_tree_extra.pack()

    # n_root.mainloop()
    return ()


def func_machine_learning(selected_ML, data, target):
    try:

        train_input, test_input, train_target, test_target = train_test_split(data, target, test_size=0.2)

        ## Random Forest 훈련하기.
        if selected_ML == 'RandomForestRegressor':

            from sklearn.ensemble import RandomForestRegressor
            rf = RandomForestRegressor(n_jobs=-1)
            scores = cross_validate(rf, train_input, train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            print('Random Forest - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
            print('Random Forest - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            rf.fit(train_input, train_target)
            print('Random Forest - Test R^2:', np.round_(rf.score(test_input, test_target), 3))
            prediction = np.round_(rf.predict(test_input), 2)


        ## LinearRegression 훈련하기.
        elif selected_ML == 'LinearRegression':

            ## PolynomialFeatures 훈련.
            from sklearn.preprocessing import PolynomialFeatures
            poly = PolynomialFeatures(degree=5, include_bias=False)
            poly.fit(train_input)
            train_poly = poly.transform(train_input)
            test_poly = poly.transform(test_input)
            print(train_poly.shape)

            from sklearn.linear_model import LinearRegression
            lr = LinearRegression()
            scores = cross_validate(lr, train_poly, train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            print('선형회귀 & polynomialFeatures - Train R^2 :', np.round_(np.mean(scores['train_score']), 3))
            print('선형회귀 & polynomialFeatures - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            lr.fit(train_poly, train_target)
            print('선형회귀 & polynomialFeatures - Test R^2:', np.round_(lr.score(test_poly, test_target), 3))
            prediction = np.round_(lr.predict(test_poly), 2)


        ## StandardScaler 적용 with linear regression
        elif selected_ML == ' StandardScaler with linear regression':

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

            from sklearn.linear_model import LinearRegression
            lr = LinearRegression()
            scores = cross_validate(lr, train_scaled, train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            print('선형회귀 & poly & scaling - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
            print('선형회귀 & poly & scaling - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            lr.fit(train_scaled, train_target)
            print('선형회귀 & poly & scaling - Test R^2:', np.round_(lr.score(test_scaled, test_target), 3))
            prediction = np.round_(lr.predict(test_scaled), 2)


        ## Ridge regularization(L2 regularization)
        elif selected_ML == ' Ridge regularization(L2 regularization)':

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

            from sklearn.linear_model import Ridge
            ridge = Ridge(alpha=100)
            scores = cross_validate(ridge, train_scaled, train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            print('릿지 회귀 - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
            print('릿지 회귀 - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            ridge.fit(train_scaled, train_target)
            print('릿지 회귀 - Test R^2:', np.round_(ridge.score(test_scaled, test_target), 3))
            prediction = ridge.predict(test_scaled)

            ## L2 하이퍼파라미터 찾기
            import matplotlib.pyplot as plt
            train_score = []
            test_score = []

            alpha_list = [0.001, 0.01, 0.1, 1, 10, 100]
            for alpha in alpha_list:
                # 릿지모델 생성 & 훈련
                ridge = Ridge(alpha=alpha)
                ridge.fit(train_scaled, train_target)
                # 훈련점수 & 테스트점수
                train_score.append(ridge.score(train_scaled, train_target))
                test_score.append(ridge.score(test_scaled, test_target))

            plt.plot(np.log10(alpha_list), train_score)
            plt.plot(np.log10(alpha_list), test_score)
            plt.xlabel('alpha')
            plt.ylabel('R^2')
            plt.show()

        mae = mean_absolute_error(test_target, prediction)
        print('|(타깃 - 예측값)|:', mae)
        print()

        Diff = np.round_(prediction - test_target, 2)
        Diff_per = np.round_((test_target - prediction) / test_target * 100, 1)

        bad = 0
        good = 0
        print()
        df = pd.DataFrame(columns=['index', 'target', 'expect', 'Diff', 'Diff(%)'])
        failed_condition = pd.DataFrame(
            columns=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle',
                     'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                     'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm'])

        for i in range(len(Diff)):
            if Diff[i] > abs(2):
                bad = bad + 1
                df = df.append(pd.DataFrame([[i, test_target[i], prediction[i], Diff[i], Diff_per[i]]],
                                            columns=['index', 'target', 'expect', 'Diff', 'Diff(%)']),
                               ignore_index=True)
                df_sort_values = df.sort_values(by=df.columns[3], ascending=True)
                df_sort_values = df_sort_values.reset_index(drop=True)

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

        print(df_sort_values)
        print()
        print('bad:', bad)
        print('good:', good)
        func_show_table("failed_condition", df=failed_condition if len(failed_condition) > 0 else NONE, extra=NONE)


    except():
        print("Error: Machine_Learning")



    # DB 서버 주소 # 데이터 베이스 이름 # 접속 유저명 # 접속 유저 패스워드

# def sql_main(server, username, passwd, database):
#     try:
#         ## 데이터 SQL에서 가지고 오기.
#         def view_table():
#             try:
#                 selected_probeId = str(list_probeId[combo_probename.current()])[1:-1]
#                 selected_DBtable = combo_DBtable.get()
#
#                 conn = pymssql.connect(server, username, passwd, database)
#                 query = f'''
#                         SELECT * FROM
#                         (
#                         SELECT a.[measSetId]
#                         ,a.[probeId]
#                         ,a.[beamstyleIndex]
#                         ,a.[txFrequencyHz]
#                         ,a.[focusRangeCm]
#                         ,a.[numTxElements]
#                         ,a.[txpgWaveformStyle]
#                         ,a.[numTxCycles]
#                         ,a.[elevAperIndex]
#                         ,a.[IsTxAperModulationEn]
#                         ,d.[probeName]
#                         ,d.[probePitchCm]
#                         ,d.[probeRadiusCm]
#                         ,d.[probeElevAperCm0]
#                         ,d.[probeElevFocusRangCm]
#                         ,b.[measResId]
#                         ,b.[zt]
#                         ,ROW_NUMBER() over (partition by a.measSetId order by b.measResId desc) as RankNo
#                         FROM meas_setting AS a
#                         LEFT JOIN meas_res_summary AS b
#                             ON a.[measSetId] = b.[measSetId]
#                         LEFT JOIN meas_station_setup AS c
#                             ON b.[measSSId] = c.[measSSId]
#                         LEFT JOIN probe_geo AS d
#                             ON a.[probeId] = d.[probeId]
#                         where b.[isDataUsable] ='yes' and c.[measPurpose] like '%Beamstyle%' and b.[errorDataLog] = ''
#                         ) T
#                         where RankNo = 1
#                         order by 1
#                         '''
#
#                 ## SQL에서 읽어온 데이터를 DataFrame으로 변환하여 df로 집어넣기 / 데이터프레임에서 probeId만 추출.
#                 Raw_data = pd.read_sql(sql=query, con=conn)
#                 # show_table(Raw_data, database, selected_DBtable)
#
#                 print(Raw_data.head())
#                 print(Raw_data.info())
#
#                 print(Raw_data['probeName'].value_counts(dropna=False))
#                 AOP_data = Raw_data.dropna()
#                 print(AOP_data.head())
#                 print(AOP_data.info())
#
#                 data = AOP_data[['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles',
#                                  'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
#                                  'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm']].to_numpy()
#                 target = AOP_data['zt'].to_numpy()
#
#                 machine_learning(combo_ML.get(), data, target)
#
#             except():
#                 print("Error: view_table")
#
#         root_SQL = Tk()
#         root_SQL.title(f"{database}")
#         root_SQL.geometry("600x600")
#
#         # MS-SQL 접속
#         conn = pymssql.connect(server, username, passwd, database)
#
#         query = '''
#         SELECT probeName, probeId FROM probe_geo
#         order by probeName, probeId
#         '''
#
#         ## SQL에서 읽어온 데이터를 DataFrame으로 변환하여 df로 집어넣기 / 데이터프레임에서 probeId만 추출.
#         df = pd.read_sql(sql=query, con=conn)
#         df_probeId = df[['probeId']]
#         list_probeId = df_probeId.values.tolist()
#
#         list_probeinfor = df.values.tolist()
#         numprobe = len(list_probeinfor)
#         list_probe = list()
#         # Probelist를 probeName + probeId 생성
#         for i in range(numprobe):
#             list_probe.append('  |  '.join(map(str, list_probeinfor[i])))
#
#         label_probename = Label(root_SQL, text='Probe Name')
#         label_probename.place(x=10, y=50)
#
#         # probe list를 combo-Box 만들어서 데이터베이스만들기
#         combo_probename = ttk.Combobox(root_SQL, value=list_probe, height=0, state='readonly')
#         # combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
#         # combo_probename.current(0)
#         # combo-Box 의 위치
#         combo_probename.place(x=120, y=50)
#
#         label_DB_table = Label(root_SQL, text='SQL Table Name')
#         label_DB_table.place(x=320, y=50)
#
#         # combo-Box 만들어서 table 선택하기 만들기.
#         combo_DBtable = ttk.Combobox(root_SQL, value=list_M3_table, height=0, state='readonly')
#         # combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
#         # combo_DBtable.current(0)
#         # combo_DBtable.bind("<<ComboboxSelected>>", print(combo_DBtable.get()))
#         # combo-Box 의 위치
#         combo_DBtable.place(x=420, y=50)
#
#         label_ML = Label(root_SQL, text='Machine Learning')
#         label_ML.place(x=10, y=20)
#         combo_ML = ttk.Combobox(root_SQL, value=list_ML, width=35, height=0, state='readonly')
#         combo_ML.place(x=120, y=20)
#
#         btn_view = Button(root_SQL, width=10, text='View Table', command=view_table)
#         btn_view.place(x=450, y=10)
#
#         conn.close()
#
#
#     except():
#         print("Error: SQL_main")

def func_sql_get(server_address, ID, password, database, command):
    try:
        conn = pymssql.connect(server_address, ID, password, database)

        if command > 5:
            query = "f'''" + command + "'''"

        elif command == 0:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeName LIKE '%{selected_probename}%'
                ORDER BY 1
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                '''

        elif command == 1:
            query = '''
            SELECT probeName, probeId FROM probe_geo 
            order by probeName, probeId
            '''

        elif command == 2:
            if selected_DBtable == 'SSR_table':
                sel_SSId = combo_SSId.get()
                sel_probesn = combo_probesn.get()

                if len(sel_SSId) > 0 and len(sel_probesn) > 0:
                    query = f'''
                    SELECT * FROM {selected_DBtable} WHERE probeName LIKE '%{selected_probename}%' and measSSId = {sel_SSId} and probeSn = {sel_probesn}
                    ORDER BY 1
                    '''

                elif len(sel_SSId) > 0 and len(sel_probesn) == 0:
                    query = f'''
                    SELECT * FROM {selected_DBtable} WHERE probeName LIKE '%{selected_probename}%' and measSSId = {sel_SSId}
                    ORDER BY 1
                    '''

                elif len(sel_SSId) == 0 and len(sel_probesn) > 0:
                    query = f'''
                    SELECT * FROM {selected_DBtable} WHERE probeName LIKE '%{selected_probename}%' and probeSn = {sel_probesn}
                    ORDER BY 1
                    '''

                else:
                    query = f'''
                    SELECT * FROM {selected_DBtable} WHERE probeName LIKE '%{selected_probename}%'
                    ORDER BY 1
                    '''

            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                '''

        Raw_data = pd.read_sql(sql=query, con=conn)

        return Raw_data
        conn.close()

    except:
        print("Error: func_sql_get")


## Login 버튼누를 경우, listbox에 있는 database로 접속.
## root 제목 DB 변경 --> SQL 접속
def func_viewer_database():
    try:
        def func_1st_load():
            try:
                global selected_probeId, selected_DBtable, selected_probename, combo_SSId, combo_probesn
                selected_probeId = str(list_probeIds[combo_probename.current()])[1:-1]
                selected_probename = str(list_probenames[combo_probename.current()])
                selected_DBtable = combo_DBtable.get()

                df = func_sql_get(server_address, ID, password, database, 0)

                if selected_DBtable == 'SSR_table':
                    measSSId = str(df['measSSId'].unique())[1:-1]
                    probeSN = str(df['probeSn'].unique())[1:-1]

                    label_SSId = Label(frame2, text='SSId')
                    label_SSId.place(x=5, y=5)
                    combo_SSId = ttk.Combobox(frame2, value=measSSId, height=0, state='readonly')
                    combo_SSId.place(x=115, y=5)

                    label_probesn = Label(frame2, text='probeSN')
                    label_probesn.place(x=5, y=25)
                    combo_probesn = ttk.Combobox(frame2, value=probeSN, height=0, state='readonly')
                    combo_probesn.place(x=115, y=25)
                else:
                    NONE

            except():
                print("Error: func_1st_load")


        def func_selected_infor():
            try:
                global selected_probeId, selected_DBtable, selected_probename
                selected_probeId = str(list_probeIds[combo_probename.current()])[1:-1]
                selected_probename = str(list_probenames[combo_probename.current()])
                selected_DBtable = combo_DBtable.get()

                df = func_sql_get(server_address, ID, password, database, 2)
                func_show_table(selected_DBtable, df, extra=NONE)

            except():
                print("Error: func_selected_infor")


        root_view = Tk()
        root_view.title(f"{database}" + ' / Viewer')
        root_view.geometry("420x400")
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

        btn_view = Button(frame1, width=15, height=2, text='Load from SQL', command=func_1st_load)
        btn_view.place(x=290, y=5)

        btn_view = Button(frame2, width=15, height=2, text='View Table', command=func_selected_infor)
        btn_view.place(x=290, y=5)

        root_view.mainloop()

    except:
        print("Error: func_viewer_database")


def func_measset_gen():
    try:
        def func_preprocessML():
            try:
                conn = pymssql.connect(server_address, ID, password, database)

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

                data = AOP_data[['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles',
                                 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                 'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm']].to_numpy()
                target = AOP_data['zt'].to_numpy()

                func_machine_learning(combo_ML.get(), data, target)

            except:
                print("Error: func_preprocessML")


        def func_create_data():
            try:
                from tkinter import filedialog
                filename = filedialog.askopenfilename(initialdir='.txt')
                df_UEdata = pd.read_csv(filename, sep='\t', encoding='cp949')
                df_first = df_UEdata.iloc[:, [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]                                        ## BeamStyle, TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE

                ########################
                ## B & M mode process ##
                df_B_mode = df_first.loc[(df_first['BeamStyleIndex'] == 0) | (df_first['BeamStyleIndex'] == 1)]         # df_sort_B = df_B_mode.sort_values(by=[df_B_mode.columns[0], df_B_mode.columns[1], df_B_mode.columns[2], df_B_mode.columns[5], df_B_mode.columns[3]], ascending=True)
                # B_num = df_sort_B['TxFocusLocCm'].nunique()
                df_M_mode = df_first.loc[(df_first['BeamStyleIndex'] == 15) | (df_first['BeamStyleIndex'] == 20)]       # df_sort_M = df_M_mode.sort_values(by=[df_M_mode.columns[0], df_M_mode.columns[1], df_M_mode.columns[2], df_M_mode.columns[5], df_M_mode.columns[3]], ascending=True)

                df = pd.concat([df_B_mode, df_M_mode])                                                                  ## 2개 데이터프레임 합치기
                df = df.reset_index(drop=True)                                                                          ## 데이터프레임 index reset
                df = df.drop_duplicates()                                                                               ## 중복된 데이터 삭제.

                refer_data = df.groupby(by=['BeamStyleIndex', 'SysTxFreqIndex', 'IsTxChannelModulationEn', 'TxpgWaveformStyle', 'ProbeNumTxCycles'], as_index=False).count()
                select_data = refer_data.iloc[:, [0, 1, 2, 3, 4, 5]]
                select_data = select_data.sort_values(by=[select_data.columns[1], select_data.columns[2], select_data.columns[3], select_data.columns[4], select_data.columns[0]], ascending=True)

                col = list(df.columns)[1:10]                                                                            ## 데이터프레임 columns name 추출('SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'IsPresetCpaEn', 'CpaDelayOffsetClk', 'TxPulseRle')
                df_grp = df.groupby(col)                                                                                ## columns name으로 정렬(TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE)
                df_dic = df_grp.groups                                                                                  ## groupby 객체의 groups 변수 --> 딕셔너리형태로 키값과 인덱스로 구성.
                idx = [x[0] for x in df_dic.values() if len(x) == 1]

                func_show_table(selected_DBtable='Summary: B & M', df=select_data, extra=NONE if len(df.reindex(idx)) == 0 else df.reindex(idx))

                BM_Not_same_cnt = len(df.reindex(idx))
                print('B&M not same Count:', BM_Not_same_cnt)

                ########################
                ## C & D mode process ##
                df_C_mode = df_first.loc[df_first['BeamStyleIndex'] == 5]
                df_D_mode = df_first.loc[df_first['BeamStyleIndex'] == 10]

                df = pd.concat([df_C_mode, df_D_mode])
                df = df.reset_index(drop=True)
                df = df.drop_duplicates()

                refer_data = df.groupby(by=['BeamStyleIndex', 'SysTxFreqIndex', 'IsTxChannelModulationEn', 'TxpgWaveformStyle', 'ProbeNumTxCycles'], as_index=False).count()
                select_data = refer_data.iloc[:, [0, 1, 2, 3, 4, 5]]

                select_data = select_data.sort_values(by=[select_data.columns[1], select_data.columns[2], select_data.columns[3], select_data.columns[4], select_data.columns[0]], ascending=True)

                col = list(df.columns)[1:11]
                df_grp = df.groupby(col)
                df_dic = df_grp.groups
                idx = [x[0] for x in df_dic.values() if len(x) == 1]

                # func_show_table(selected_DBtable='Summary: C & D', df=select_data, extra=NONE if len(df.reindex(idx)) == 0 else df.reindex(idx))

                CD_Not_same_cnt = len(df.reindex(idx))
                print('C&D not same Count:', CD_Not_same_cnt)

                if BM_Not_same_cnt == 0 and CD_Not_same_cnt == 0:

                    # SettingWithCopyWarning 해결 / 복사본만 수정할 것인지 혹은 원본도 수정할 것인지 알 수 없어 경고
                    df_B_mode_update = df_B_mode.copy()
                    df_B_mode_update['bsIndexTrace'] = np.where(df_B_mode_update['BeamStyleIndex'] == 0, '15', '20')
                    df_C_mode_update = df_C_mode.copy()
                    df_C_mode_update['bsInDexTrace'] = [10]

                    df_merge = pd.concat([df_B_mode_update, df_C_mode_update])
                    print(df_merge)
                    same_cond = 1

                elif BM_Not_same_cnt == 0 and CD_Not_same_cnt > 0:
                    df_B_mode_update, df_C_mode_update, df_D_mode_update = df_B_mode.copy(), df_C_mode.copy(), df_D_mode.copy()
                    df_B_mode_update['bsIndexTrace'] = np.where(df_B_mode_update['BeamStyleIndex'] == 0, '15', '20')
                    df_C_mode_update['bsIndexTrace'] = 0
                    df_D_mode_update['bsIndexTrace'] = 0

                    df_merge = pd.concat([df_B_mode_update, df_C_mode_update, df_D_mode_update])
                    print(df_merge)

                    same_cond = 2

                elif BM_Not_same_cnt > 0 and CD_Not_same_cnt == 0:
                    B_bsIndexTrace = 0
                    D_bsIndexTrace = 10
                    df_merge = pd.concat([df_B_mode, df_C_mode, df_M_mode])
                    same_cond = 3

                else:
                    B_bsIndexTrace = 0
                    D_bsIndexTrace = 0
                    df_merge = pd.concat([df_B_mode, df_C_mode, df_D_mode, df_M_mode])
                    same_cond = 4

                print(same_cond)
                # probeId,
                #
                # maxTxVoltageVolt
                # ceilTxVoltageVolt
                # profTxVoltageVolt
                # totalVoltagePt
                # numMeasVoltage
                # elevAperIndex
                # zStartDistCm = 0.5
                # zMeasNum
                # dumpSwVersion
                # DTxFreqIndex
                # VTxIndex
                # SysPulserSelA

                func_show_table(selected_DBtable='meas_setting', df=df_merge, extra=NONE)
                func_preprocessML()

            except:
                print("Error: func_create_data")

        root_gen = Tk()
        root_gen.title(f"{database}" + ' / MeasSet_generation')
        root_gen.geometry("590x200")
        root_gen.resizable(False, False)

        frame1 = Frame(root_gen, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)

        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        combo_probename = ttk.Combobox(frame1, value=list_probe, height=0, state='readonly')
        combo_probename.place(x=5, y=25)

        label_ML = Label(frame1, text='Machine Learning')
        label_ML.place(x=185, y=5)
        combo_ML = ttk.Combobox(frame1, value=list_ML, width=35, height=0, state='readonly')
        combo_ML.place(x=185, y=25)

        btn_load = Button(frame1, width=15, height=2, text='Select & Load', command=func_create_data)
        btn_load.place(x=460, y=5)

        root_gen.mainloop()

    except:
        print("Error: measset_gen")


def tx_sum():
    try:
        print("see")
    except:
        print("Error: Tx_Summary")


def func_main():
    try:
        global database, list_probeIds, list_probe, list_probenames
        database = combo_login.get()

        root_main = Tk()
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


        # btn_ML = Button(root_main, width=30, height=3, text='Machine Learning', command=sql_main(server_address, ID, password, database))
        # btn_ML.grid(row=1, column=0)

        root_main.mainloop()

    except:
        print("Error: main")


##################################################
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