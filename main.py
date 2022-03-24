import pymssql
import pandas as pd
from tkinter import *
from tkinter import ttk
import configparser

## SQL데이터 DataFrame을 이용하여 Treeview에 기록하여 출력.
def show_table(df, database, selected_DBtable):
    root1 = Tk()
    root1.title(f"{database}  //  {selected_DBtable}")
    root1.geometry("1800x800")

    my_tree = ttk.Treeview(root1)

    my_tree["column"] = list(df.columns)
    my_tree["show"] = "headings"

    # scrollbars
    vsb = Scrollbar(root1, orient="vertical", command=my_tree.yview)
    vsb.place(relx=0.978, rely=0.175, relheight=0.713, relwidth=0.020)

    hsb = Scrollbar(root1, orient="horizontal", command=my_tree.xview)
    hsb.place(relx=0.014, rely=0.875, relheight=0.020, relwidth=0.965)

    my_tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Loop thru column list for headers
    for column in my_tree["column"]:
        my_tree.column(column, width=110, minwidth=50)
        my_tree.heading(column, text=column)

    # Put data in treeview
    df_rows = df.to_numpy().tolist()
    for row in df_rows:
        my_tree.insert("", "end", values=row)

    my_tree.pack()
    root1.mainloop()


# DB 서버 주소 # 데이터 베이스 이름 # 접속 유저명 # 접속 유저 패스워드
def sql_main(server, username, passwd, database):
    try:
        def view_table():
            try:
                selected_probeId = str(list_probeId[probe_combo.current()])[1:-1]
                selected_DBtable = DBtable_combo.get()

                conn = pymssql.connect(server, username, passwd, database)
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
                        where b.[isDataUsable] ='yes' and b.[errorDataLog] = '' and b.[zt] != -1  
                        ) T
                        where RankNo = 1
                        order by 1
                        '''
                # c.[measPurpose] like '%Beamstyle%' and

                ## SQL에서 읽어온 데이터를 DataFrame으로 변환하여 df로 집어넣기 / 데이터프레임에서 probeId만 추출.
                Raw_data = pd.read_sql(sql=query, con=conn)
                # show_table(Raw_data, database, selected_DBtable)

                print(Raw_data.head())
                print(Raw_data.info())

                print(Raw_data['probeName'].value_counts(dropna=False))
                AOP_data = Raw_data.dropna()
                print(AOP_data.head())
                print(AOP_data.info())

                data = AOP_data[['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                 'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm']].to_numpy()
                target = AOP_data['zt'].to_numpy()


                from sklearn.model_selection import train_test_split
                train_input, test_input, train_target, test_target = train_test_split(data, target)


                ## PolynomialFeatures 훈련.
                from sklearn.preprocessing import PolynomialFeatures
                poly = PolynomialFeatures(degree=5, include_bias=False)
                poly.fit(train_input)
                train_poly = poly.transform(train_input)
                test_poly = poly.transform(test_input)
                print(train_poly.shape)
                print()

                from sklearn.linear_model import LinearRegression
                lr = LinearRegression()
                lr.fit(train_poly, train_target)

                from sklearn.model_selection import cross_validate
                scores = cross_validate(lr, train_poly, train_target)
                print(scores)
                import numpy as np
                print('선형회귀 & polynomialFeatures - Train R^2 :', lr.score(train_poly, train_target))
                print('선형회귀 & polynomialFeatures - Train_validation R^2:', np.mean(scores['test_score']))
                print('선형회귀 & polynomialFeatures - Test R^2:', lr.score(test_poly, test_target))

                from sklearn.metrics import mean_absolute_error
                test_prediction = lr.predict(test_poly)
                mae = mean_absolute_error(test_target, test_prediction)
                print('|(타깃 - 예측값)|:', mae)
                print()


                ## StandardScaler 적용 with linear regression
                from sklearn.preprocessing import StandardScaler
                ss = StandardScaler()
                ss.fit(train_poly)
                train_scaled = ss.transform(train_poly)
                test_scaled = ss.transform(test_poly)

                lr.fit(train_scaled, train_target)
                scores = cross_validate(lr, train_scaled, train_target)
                print(scores)
                print('선형회귀 & poly & scaling - Train R^2:', lr.score(train_scaled, train_target))
                print('선형회귀 & poly & scaling - Train_validation R^2:', np.mean(scores['test_score']))
                print('선형회귀 & poly & scaling - Test R^2:', lr.score(test_scaled, test_target))

                from sklearn.metrics import mean_absolute_error
                test_prediction = lr.predict(test_scaled)
                mae = mean_absolute_error(test_target, test_prediction)
                print('|(타깃 - 예측값)|:', mae)
                print()


                ## Ridge regularization(L2 regularization)
                from sklearn.linear_model import Ridge
                ridge = Ridge(alpha=100)
                ridge.fit(train_scaled, train_target)
                scores = cross_validate(ridge, train_scaled, train_target)
                print(scores)
                print('릿지 회귀 Train R^2:', ridge.score(train_scaled, train_target))
                print('릿지 회귀 Train_validation R^2:', np.mean(scores['test_score']))
                print('릿지 회귀 Test R^2:', ridge.score(test_scaled, test_target))

                from sklearn.metrics import mean_absolute_error
                test_prediction = ridge.predict(test_scaled)
                mae = mean_absolute_error(test_target, test_prediction)
                print('|(타깃 - 예측값)|:', mae)
                print()

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


                ## Lasso regularization(L1 regularization)
                # from sklearn.linear_model import Lasso
                # lasso = Lasso(alpha=0.001, max_iter=10000)
                # lasso.fit(train_scaled, train_target)
                # scores = cross_validate(lasso, train_scaled, train_target)
                # print(scores)
                # print('라쏘 회귀 Train R^2:', np.round_((lasso.score(train_scaled, train_target)), 2))
                # print('라쏘 회귀 Train_validation R^2:', np.round_(np.mean(scores['test_score']), 2))
                # print('라쏘 회귀 Test R^2:', np.round_(lasso.score(test_scaled, test_target), 2))
                #
                # from sklearn.metrics import mean_absolute_error
                # test_prediction = lasso.predict(test_scaled)
                # mae = mean_absolute_error(test_target, test_prediction)
                # print('|(타깃 - 예측값)|:', mae)
                # print("사용한 특성의 수: {}".format(np.sum(lasso.coef_ != 0)))
                # print()
                #
                # train_score = []
                # test_score = []
                #
                # alpha_list = [0.001, 0.01, 0.1, 1, 10, 100]
                # for alpha in alpha_list:
                #     # 릿지모델 생성 & 훈련
                #     lasso = Lasso(alpha=alpha, max_iter=10000)
                #     lasso.fit(train_scaled, train_target)
                #     # 훈련점수 & 테스트점수
                #     train_score.append(lasso.score(train_scaled, train_target))
                #     test_score.append(lasso.score(test_scaled, test_target))
                #
                # plt.plot(np.log10(alpha_list), train_score)
                # plt.plot(np.log10(alpha_list), test_score)
                # plt.xlabel('alpha')
                # plt.ylabel('R^2')
                # plt.show()


                ## DecisionTreeRegressor 훈련.
                from sklearn.tree import DecisionTreeRegressor
                dt = DecisionTreeRegressor()
                dt.fit(train_scaled, train_target)
                scores = cross_validate(dt, train_scaled, train_target)
                print(scores)
                print('의사결정트리 Train R^2:', dt.score(train_scaled, train_target))
                print('의사결정트리 Train_validation R^2:', np.mean(scores['test_score']))
                print('의사결정트리 Test R^2:', dt.score(test_scaled, test_target))

                from sklearn.metrics import mean_absolute_error
                test_prediction = dt.predict(test_scaled)
                mae = mean_absolute_error(test_target, test_prediction)
                print('|(타깃 - 예측값)|:', mae)
                print()


                ## DecisionTree Regressor 훈련 by train data: not scaling with no polynomial
                from sklearn.tree import DecisionTreeRegressor
                dt = DecisionTreeRegressor()
                dt.fit(train_input, train_target)
                scores = cross_validate(dt, train_input, train_target)
                print(scores)
                print('의사결정트리 Train R^2:', dt.score(train_input, train_target))
                print('의사결정트리 Train_validation R^2:', np.mean(scores['test_score']))
                print('의사결정트리 Test R^2:', dt.score(test_input, test_target))

                from sklearn.metrics import mean_absolute_error
                test_prediction = dt.predict(test_input)
                mae = mean_absolute_error(test_target, test_prediction)
                print('|(타깃 - 예측값)|:', mae)
                print()

                from sklearn.tree import plot_tree
                plt.figure(figsize=(20, 15))
                plot_tree(dt, filled=True, feature_names=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                 'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm'])
                plt.show()
                print(dt.feature_importances_)
                print(np.round_(dt.feature_importances_/1*100, 1))
                print()


                ## Random Forest 훈련하기.
                from sklearn.ensemble import RandomForestRegressor
                rf = RandomForestRegressor(n_jobs=-1)
                scores = cross_validate(rf, train_input, train_target, return_train_score=True, n_jobs=-1)
                print('Random Forest - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
                print('Random Forest - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))
                rf.fit(train_input, train_target)
                print('Random Forest - Test R^2:', np.round_(rf.score(test_input, test_target), 3))

                from sklearn.metrics import mean_absolute_error
                test_prediction = dt.predict(test_input)
                mae = mean_absolute_error(test_target, test_prediction)
                print('|(타깃 - 예측값)|:', mae)
                print(dt.feature_importances_)
                print(np.round_(dt.feature_importances_ / 1 * 100, 1))
                print()


                ## 하이퍼파라미터 튜닝 1개만: min_impurity_decrease.
                ## Grid-search method 이용
                from sklearn.model_selection import GridSearchCV
                params = {'min_impurity_decrease': [0.0001, 0.0002, 0.0003, 0.0004, 0.0005]}

                # cv 매개변수 5개 x cross_validate(5 fold)
                gs = GridSearchCV(DecisionTreeRegressor(), params, n_jobs=-1)
                gs.fit(train_input, train_target)

                # GridSearch는 훈련이 끝나면, 25개 모델 중 검증 점수가 가장 높은 모델의 매개변수 조합으로 전체 훈현 세트로 자동으로 다시 모델 훈련.
                # 훈련된 모델은 gs 객체의 best_estimator_ 속성에 저장되어 있음.
                dt = gs.best_estimator_
                print('Decision-TreeRegressor with hyperparameter 1EA')
                print(np.round_(dt.score(train_input, train_target), 2))
                print(gs.best_params_)

                # 5 fold 점수 확인
                print(gs.cv_results_['mean_test_score'])

                # 넘파이 argmax() 함수 사용하여 가장 큰 값의 인덱스 추출
                best_index = np.argmax(gs.cv_results_['mean_test_score'])
                print(gs.cv_results_['params'][best_index])


                ## 하이퍼파라미터
                ## Random search 이용: 매개변수 값의 목록을 전달하는 것이 아니라 매개변수를 샘플링할수 있는 확률분포 객체를 전달.
                from scipy.stats import uniform, randint
                params = {'min_impurity_decrease': uniform(0.0001, 0.001),
                          'max_depth': randint(20, 50),
                          'min_samples_split': randint(2, 25),
                          'min_samples_leaf': randint(1, 25)
                          }

                # cv 매개변수 5개 x cross_validate(5 fold)
                from sklearn.model_selection import RandomizedSearchCV
                gs = RandomizedSearchCV(DecisionTreeRegressor(), params, n_iter=100, n_jobs=-1)
                gs.fit(train_input, train_target)

                # GridSearch는 훈련이 끝나면, 25개 모델 중 검증 점수가 가장 높은 모델의 매개변수 조합으로 전체 훈현 세트로 자동으로 다시 모델 훈련.
                # 훈련된 모델은 gs 객체의 best_estimator_ 속성에 저장되어 있음.
                dt = gs.best_estimator_
                print('Decision-TreeRegressor with hyperparameter 4EA')
                print(np.round_(dt.score(train_input, train_target), 2))
                print(gs.best_params_)

                # 5 fold 점수 확인
                print(gs.cv_results_['mean_test_score'])

                # 넘파이 argmax() 함수 사용하여 가장 큰 값의 인덱스 추출
                best_index = np.argmax(gs.cv_results_['mean_test_score'])
                print(gs.cv_results_['params'][best_index])



            except():
                print("Error: view_table")


        root_SQL = Tk()
        root_SQL.title(f"{database}")
        root_SQL.geometry("600x600")


        # MS-SQL 접속
        conn = pymssql.connect(server, username, passwd, database)

        query = '''
        SELECT probeName, probeId FROM probe_geo
        order by probeName, probeId
        '''


        ## SQL에서 읽어온 데이터를 DataFrame으로 변환하여 df로 집어넣기 / 데이터프레임에서 probeId만 추출.
        df = pd.read_sql(sql=query, con=conn)
        df_probeId = df[['probeId']]
        list_probeId = df_probeId.values.tolist()

        list_probeinfor = df.values.tolist()
        numprobe = len(list_probeinfor)
        list_probe = list()
        # Probelist를 probeName + probeId 생성
        for i in range(numprobe):
            list_probe.append('  |  '.join(map(str, list_probeinfor[i])))


        label_probename = Label(root_SQL, text='Probe Name')
        label_probename.place(x=10, y=50)

        # probe list를 combo-Box 만들어서 데이터베이스만들기
        probe_combo = ttk.Combobox(root_SQL, value=list_probe, height=0, state='readonly')
        # combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
        # probe_combo.current(0)
        # combo-Box 의 위치
        probe_combo.place(x=90, y=50)


        label_DB_table = Label(root_SQL, text='SQL Table Name')
        label_DB_table.place(x=290, y=50)

        # combo-Box 만들어서 table 선택하기 만들기.
        DBtable_combo = ttk.Combobox(root_SQL, value=list_M3_table, height=0)
        # combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
        # DBtable_combo.current(0)
        DBtable_combo.bind("<<ComboboxSelected>>", print(DBtable_combo.get()))
        # combo-Box 의 위치
        DBtable_combo.place(x=400, y=50)


        btn_view = Button(root_SQL, width=10, text='View Table', command=view_table)
        btn_view.place(x=450, y=10)

        conn.close()


    except():
        print("Error: SQL_main")


## Login 버튼누를 경우, listbox에 있는 database로 접속.
## root 제목 DB 변경 --> SQL 접속
def login_database():
    try:
        database = login_combo.get()
        # database = listbox.get(listbox.curselection())
        sql_main(server_address, ID, password, database)

    except:
        print("Error: login_database")


##################################################
### config 파일에서 Database information read   ###

config = configparser.ConfigParser()
config.read('AOP_config.cfg')

server_address = config["server address"]["address"]
databases = config["database"]["name"]
ID = config["username"]["ID"]
password = config["password"]["PW"]
server_table_M3 = config["server table"]["M3 server table"]


list_database = databases.split(',')
list_M3_table = server_table_M3.split(',')


## Start tk 만들기.

root = Tk()
root.title("DB를 선택해주세요")
root.geometry("250x200")
root.resizable(False, False)


label1 = Label(root, text='데이터베이스를 선택하세요')
label1.grid(row=0, column=0)

# combo-Box 만들어서 데이터베이스만들기
login_combo = ttk.Combobox(root, value=list_database)
# combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
login_combo.current(0)
# combo-Box 의 위치
login_combo.grid(row=1, column=0)
# login_combo.pack(pady=20)


# SQL database listbox 선택하기.
# Listbox만들기: e.g) server 선택할 수 있도록 수행.
# listbox = Listbox(root, selectmode="single", height=1)
# for i in range(0, num_database):
#     try:
#         listbox.insert(i, list_database[i])
#     except:
#         print('Error: SQL_Database config file')
# listbox.pack()

btn_login = Button(root, width=10, text='Login', command=login_database)
btn_login.grid(row=1, column=1)
#
# style = ttk.Style()
# style.theme_use("default")
# # style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
# # style.map('Treeview', background=[('selected', 'blue')])
# style.map("Treeview")


root.mainloop()





# label = Label(root, text="Verification Report")
# label.pack()

## LabelFrame 만들기
# wrapper1 = LabelFrame(root, text="Verification_Report")
# wrapper1.pack(fill="both", expand="yes", padx=2, pady=1)