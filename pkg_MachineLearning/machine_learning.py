
class Machine_Learning(object):
    def __init__(self):
        super().__init__()
        self.initialize()


    def initialize(self):
        window_ML = tkinter.Toplevel()
        window_ML.title(f"{database}" + ' / Machine Learning')
        window_ML.geometry("410x200")
        window_ML.resizable(False, False)

        frame1 = Frame(window_ML, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)

        label_ML = Label(frame1, text='Machine Learning')
        label_ML.place(x=5, y=5)
        self.combo_ML = ttk.Combobox(frame1, value=list_ML, width=35, height=0, state='readonly')
        self.combo_ML.place(x=5, y=25)

        btn_load = Button(frame1, width=15, height=2, text='Select & Train', command=self._fn_ML_sequence)
        btn_load.place(x=280, y=5)

        window_ML.mainloop()


    def _fn_ML_sequence(self):
        self.fn_preprocessML()
        self.fn_modelML()
        self.fn_ML_fit()
        self.fn_ML_save()
        self.fn_diff_check()


    def fn_preprocessML(self):
        try:
            print(list_database)

            SQL_list = []
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
                        ,d.[probeElevAperCm1]
                        ,d.[probeElevFocusRangCm]
                        ,d.[probeElevFocusRangCm1]
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
                # AOP_data = Raw_data.dropna()
                SQL_list.append(Raw_data)

            ## 결합할 데이터프레임 list: SQL_list
            AOP_data = pd.concat(SQL_list, ignore_index=True)


            ## 결측치 제거 및 대체
            AOP_data['probeRadiusCm'] = AOP_data['probeRadiusCm'].fillna(0)
            AOP_data['probeElevAperCm1'] = AOP_data['probeElevAperCm1'].fillna(0)
            AOP_data['probeElevFocusRangCm1'] = AOP_data['probeElevFocusRangCm1'].fillna(0)
            AOP_data = AOP_data.drop(AOP_data[AOP_data['beamstyleIndex'] == 12].index)
            AOP_data = AOP_data.dropna()


            print(AOP_data.count())
            AOP_data.to_csv('AOP_data.csv')

            self.feature_list = ['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles',
                                 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm', 'probeRadiusCm', 'probeElevAperCm0',
                                 'probeElevAperCm1', 'probeElevFocusRangCm', 'probeElevFocusRangCm1']
            ## feature 2개 추가.
            self.data = AOP_data[self.feature_list].to_numpy()
            self.target = AOP_data['zt'].to_numpy()


        except:
            print('Error: fn_preprocessML')


    def fn_feature_import(self):
        try:
            df_import = pd.DataFrame()
            df_import = df_import.append(pd.DataFrame([np.round((self.model.feature_importances_) * 100, 2)],
                                                      columns=self.feature_list), ignore_index=True)

            ShowTable.fn_show_table(f'{self.selected_ML}', df=df_import)

            importances = self.model.feature_importances_
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

        except:
            print('fn_feature_import')


    def fn_modelML(self):

        self.selected_ML = self.combo_ML.get()
        self.train_input, self.test_input, self.train_target, self.test_target = train_test_split(self.data, self.target, test_size=0.2)

        ## 왼쪽 공백 삭제
        self.selected_ML = self.selected_ML.lstrip()

        ## Random Forest 훈련하기.
        if self.selected_ML == 'RandomForestRegressor':
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
            self.model = RandomForestRegressor(max_depth=40, max_features='sqrt', min_samples_split=2, n_estimators=90, n_jobs=-1)


        ## Gradient Boosting
        elif self.selected_ML == 'Gradient_Boosting':
            from sklearn.ensemble import GradientBoostingRegressor
            self.model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.2)


        ## Histogram-based Gradient Boosting
        elif self.selected_ML == 'Histogram-based Gradient Boosting':
            from sklearn.experimental import enable_hist_gradient_boosting
            from sklearn.ensemble import HistGradientBoostingRegressor
            self.model = HistGradientBoostingRegressor()


        elif self.selected_ML == 'XGBoost':
            from xgboost import XGBRegressor
            self.model = XGBRegressor(tree_method='hist')


        ## VotingRegressor 훈련하기
        ## Need to update....
        elif self.selected_ML == 'VotingRegressor':
            from sklearn.ensemble import VotingRegressor
            from sklearn.linear_model import Ridge
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.neighbors import KNeighborsRegressor

            from sklearn.pipeline import make_pipeline

            from sklearn.preprocessing import PolynomialFeatures
            poly = PolynomialFeatures(degree=5, include_bias=False)
            poly.fit(self.train_input)
            train_poly = poly.transform(self.train_input)
            test_poly = poly.transform(self.test_input)

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(train_poly)
            self.train_scaled = ss.transform(train_poly)
            self.test_scaled = ss.transform(test_poly)


            model1 = Ridge(alpha=0.1)
            model2 = RandomForestRegressor(n_jobs=-1)
            model3 = KNeighborsRegressor()

            self.model = VotingRegressor(estimators=[('ridge', model1), ('random', model2), ('neigh', model3)])


        ## LinearRegression 훈련하기.
        elif self.selected_ML == 'LinearRegression':

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(self.train_input)
            self.train_scaled = ss.transform(self.train_input)
            self.test_scaled = ss.transform(self.test_input)

            from sklearn.linear_model import LinearRegression
            self.model = LinearRegression()


            ## PolynomialFeatures 데이터를 train_input / test_input에 넣어서 아래 common에 입력
            self.train_input = self.train_scaled
            self.test_input = self.test_scaled


        ## StandardScaler 적용 with linear regression
        elif self.selected_ML == 'PolynomialFeatures with linear regression':

            from sklearn.preprocessing import PolynomialFeatures
            poly = PolynomialFeatures(degree=3, include_bias=False)
            poly.fit(self.train_input)
            train_poly = poly.transform(self.train_input)
            test_poly = poly.transform(self.test_input)

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(train_poly)
            self.train_scaled = ss.transform(train_poly)
            self.test_scaled = ss.transform(test_poly)

            from sklearn.linear_model import LinearRegression
            self.model = LinearRegression()

            ## PolynomialFeatures 데이터를 train_input / test_input에 넣어서 아래 common에 입력
            self.train_input = self.train_scaled
            self.test_input = self.test_scaled


        ## Ridge regularization(L2 regularization)
        elif self.selected_ML == 'Ridge regularization(L2 regularization)':

            from sklearn.preprocessing import PolynomialFeatures
            poly = PolynomialFeatures(degree=3, include_bias=False)
            poly.fit(self.train_input)
            train_poly = poly.transform(self.train_input)
            test_poly = poly.transform(self.test_input)

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(train_poly)
            self.train_scaled = ss.transform(train_poly)
            self.test_scaled = ss.transform(test_poly)

            from sklearn.linear_model import Ridge
            self.model = Ridge(alpha=0.1)

            ## PolynomialFeatures 데이터를 train_input / test_input에 넣어서 아래 common에 입력
            self.train_input = self.train_scaled
            self.test_input = self.test_scaled


            ## L2 하이퍼파라미터 찾기
            train_score = []
            test_score = []

            alpha_list = [0.001, 0.01, 0.1, 1, 10, 100]
            import matplotlib.pyplot as plt
            for alpha in alpha_list:
                # 릿지모델 생성 & 훈련
                self.model = Ridge(alpha=alpha)
                self.model.fit(self.train_scaled, self.train_target)
                # 훈련점수 & 테스트점수
                train_score.append(self.model.score(self.train_scaled, self.train_target))
                test_score.append(self.model.score(self.test_scaled, self.test_target))

            plt.plot(np.log10(alpha_list), train_score)
            plt.plot(np.log10(alpha_list), test_score)
            plt.xlabel('alpha')
            plt.ylabel('R^2')
            plt.show()


        elif self.selected_ML == 'DecisionTreeRegressor(scaled data)':

            from sklearn.tree import DecisionTreeRegressor
            self.model = DecisionTreeRegressor(max_depth=10, random_state=42)

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(self.train_input)
            self.train_scaled = ss.transform(self.train_input)
            self.test_scaled = ss.transform(self.test_input)

            self.model.fit(self.train_scaled, self.train_target)


            scores = cross_validate(self.model, self.train_scaled, self.train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            print('결정트리 - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
            print('결정트리 - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            # dt.fit(train_scaled, train_target)
            print('결정트리 - Test R^2:', np.round_(self.model.score(self.test_scaled, self.test_target), 3))
            self.prediction = self.model.predict(self.test_scaled)

            df_import = pd.DataFrame()
            df_import = df_import.append(pd.DataFrame([np.round((self.model.feature_importances_) * 100, 2)],
                                                      columns=['txFrequencyHz', 'focusRangeCm', 'numTxElements',
                                                               'txpgWaveformStyle',
                                                               'numTxCycles', 'elevAperIndex',
                                                               'IsTxAperModulationEn', 'probePitchCm',
                                                               'probeRadiusCm', 'probeElevAperCm0',
                                                               'probeElevFocusRangCm']), ignore_index=True)

            ShowTable.fn_show_table('DecisionTreeRegressor', df=df_import)

            ## plot_tree 이용하여 어떤 트리가 생성되었는지 확인.
            import matplotlib.pyplot as plt
            from sklearn.tree import plot_tree
            plt.figure(figsize=(10, 7))
            plot_tree(self.model, max_depth=2, filled=True,
                      feature_names=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle',
                                     'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                     'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm'])
            plt.show()


        elif self.selected_ML == 'DecisionTreeRegressor(No scaled data)':

            from sklearn.tree import DecisionTreeRegressor
            self.model = DecisionTreeRegressor(max_depth=10, random_state=42)
            self.model.fit(self.train_input, self.train_target)

            self.fn_feature_import()

            ## plot_tree 이용하여 어떤 트리가 생성되었는지 확인.
            import matplotlib.pyplot as plt
            from sklearn.tree import plot_tree
            plt.figure(figsize=(10, 7))
            plot_tree(self.model, max_depth=1, filled=True,
                      feature_names=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle',
                                     'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                     'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm'])
            plt.show()


        ## common DNN
        elif self.selected_ML == 'DL_DNN':
            import tensorflow as tf
            from tensorflow import keras

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(self.train_input)
            self.train_scaled = ss.transform(self.train_input)
            self.test_scaled = ss.transform(self.test_input)


            def fn_build_DNN():
                dense1 = keras.layers.Dense(100, activation='relu', input_shape=(13,), name='hidden')
                dense2 = keras.layers.Dense(10, activation='relu')
                dense3 = keras.layers.Dense(1)

                model = keras.Sequential([dense1, dense2, dense3])

                optimizer = tf.keras.optimizers.Adam(0.001)

                model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
                return model

            self.model = fn_build_DNN()
            print(self.model.summary())

            example_batch = self.train_scaled[:10]
            example_result = self.model.predict(example_batch)
            print('example_batch 형태:', example_batch.shape)


            import matplotlib.pyplot as plt

            def plot_data(history):
                hist = pd.DataFrame(history.history)
                hist['epoch'] = history.epoch

                plt.figure(figsize=(12, 8))

                plt.subplot(2, 2, 1)
                plt.xlabel('Epoch')
                plt.ylabel('Mean Abs Error [Cm]')
                plt.plot(hist['epoch'], hist['mae'], label='Train Error')
                plt.plot(hist['epoch'], hist['val_mae'], label='Val Error')
                plt.ylim([0, 2])
                plt.legend()

                plt.subplot(2, 2, 2)
                plt.xlabel('Epoch')
                plt.ylabel('Mean Square Error [$Cm^2$]')
                plt.plot(hist['epoch'], hist['mse'],
                         label='Train Error')
                plt.plot(hist['epoch'], hist['val_mse'],
                         label='Val Error')
                plt.ylim([0, 3])
                plt.legend()

                ## test_target vs. prediction 차이
                plt.subplot(2, 2, 3)
                plt.scatter(self.test_target, self.prediction)
                plt.xlabel('True Values [Cm]')
                plt.ylabel('Predictions [Cm]')
                plt.axis('equal')
                plt.axis('square')
                plt.xlim([0, plt.xlim()[1]])
                plt.ylim([0, plt.ylim()[1]])
                _ = plt.plot([-10, 10], [-10, 10])


                ## 오차의 분표확인.
                plt.subplot(2, 2, 4)
                error = self.prediction - self.test_target
                plt.hist(error, bins=25)
                plt.xlabel('Prediction Error [Cm]')
                _ = plt.ylabel('Count')


                plt.show()

            ## 모델 훈련 / 에포크가 끝날 때마다 점(.)을 출력해 훈련 진행 과정을 표시합니다
            class PrintDot(keras.callbacks.Callback):
                def on_epoch_end(self, epoch, logs):
                    if epoch % 100 == 0: print('')
                    print('.', end='')

            EPOCHS = 1000
            self.model = fn_build_DNN()

            # patience 매개변수는 성능 향상을 체크할 에포크 횟수입니다
            early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
            history = self.model.fit(self.train_scaled, self.train_target, epochs=EPOCHS, batch_size= 3, validation_split=0.2, verbose=0,
                                     callbacks=[early_stop, PrintDot()])

            hist = pd.DataFrame(history.history)
            hist['epoch'] = history.epoch
            print()
            print(hist.tail())


            loss, mae, mse = self.model.evaluate(self.test_scaled, self.test_target, verbose=2)
            print("테스트 세트의 평균 절대 오차: {:5.2f} Cm".format(mae))


            ## 테스트 세트에 있는 샘플을 사용해 zt 값을 예측하여 비교하기.
            self.prediction = self.model.predict(self.test_scaled).flatten()

            plot_data(history)


        ## 위 아래 DNN 비교.
        elif self.selected_ML == 'DNN_HonGong':
            import tensorflow as tf
            from tensorflow import keras
            # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

            # train_target 분포 확인.
            import seaborn as sns
            import matplotlib.pyplot as plt
            plt.title('Distport for zt')
            sns.distplot(self.train_target)
            plt.show()

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(self.train_input)
            self.train_scaled = ss.transform(self.train_input)
            self.test_scaled = ss.transform(self.test_input)

            def model_fn(a_layer=None):
                model = keras.Sequential()
                model.add(keras.layers.Flatten(input_shape=(13,), name='input'))
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
            self.model = model_fn()
            print(self.model.summary())

            rmsprop = keras.optimizers.RMSprop(0.001)
            self.model.compile(optimizer=rmsprop, loss='mse', metrics=['mae', 'mse'])

            checkpoint_cb = keras.callbacks.ModelCheckpoint('best-model.h5')
            early_stopping_cb = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            history = self.model.fit(self.train_scaled, self.train_target, epochs=1000, validation_split=0.2, callbacks=[checkpoint_cb, early_stopping_cb])

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
            self.model = keras.models.load_model('best-model.h5')
            print()
            print('<Test evaluate>')
            loss, mae, mse = self.model.evaluate(self.test_scaled, self.test_target, verbose=2)
            print('Test evaluate:', self.model.evaluate(self.test_scaled, self.test_target))
            print("테스트 세트의 평균 절대 오차: {:5.2f} Cm".format(mae))


            self.prediction = self.model.predict(self.test_scaled).flatten()


            ## np.round_ error check. => why does works for this sequence?
            self.prediction = np.around(self.prediction, 2)
            # prediction = {:.2f}.format(prediction)
            df = pd.DataFrame(self.prediction, self.test_target)
            print('[csv 파일 추출 완료]')
            df.to_csv('test_est.csv')

            import matplotlib.pyplot as plt
            plt.scatter(self.test_target, self.prediction)
            plt.xlabel('True Values [Cm]')
            plt.ylabel('Predictions [Cm]')
            plt.axis('equal')
            plt.axis('square')
            plt.xlim([0, plt.xlim()[1]])
            plt.ylim([0, plt.ylim()[1]])
            _ = plt.plot([-10, 10], [-10, 10])
            plt.show()

            ## 오차의 분표확인.
            Error = self.prediction - self.test_target
            plt.hist(Error, bins=25)
            plt.xlabel('Prediction Error [Cm]')
            _ = plt.ylabel('Count')
            plt.show()


    def fn_ML_fit(self):
        ## DNN 인 경우, 아래와 같이 training
        if "DNN" in self.selected_ML:
            pass

        else:
            scores = cross_validate(self.model, self.train_input, self.train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            import numpy as np
            print(f'{self.selected_ML} - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
            print(f'{self.selected_ML} - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            self.model.fit(self.train_input, self.train_target)
            print(f'{self.selected_ML} - Test R^2:', np.round_(self.model.score(self.test_input, self.test_target), 3))
            self.prediction = np.round_(self.model.predict(self.test_input), 2)

            ## feature import table pop-up
            if self.selected_ML == 'RandomForestRegressor':
                self.fn_feature_import()
            else:
                pass


    def fn_ML_save(self):
        newpath = './Model'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        ## DNN 인 경우 아래와 같이 저장.
        if "DNN" in self.selected_ML:
            self.model.save(f'Model/{self.selected_ML}_v1_python37.h5')


        ## DNN 아닐 경우 아래와 같이 저장.
        else:
            ## modeling file 저장 장소.
            joblib.dump(self.model, f'Model/{self.selected_ML}_v1_python37.pkl')


    def fn_diff_check(self):
        mae = mean_absolute_error(self.test_target, self.prediction)
        print('|(타깃 - 예측값)|:', mae)

        Diff = np.round_(self.prediction - self.test_target, 2)
        Diff_per = np.round_((self.test_target - self.prediction) / self.test_target * 100, 1)


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

                df_bad = df_bad.append \
                    (pd.DataFrame([[i, self.test_target[i], self.prediction[i], Diff[i], Diff_per[i]]],
                                                    columns=['index', '측정값(Cm)', '예측값(Cm)', 'Diff(Cm)', 'Diff(%)']),
                                       ignore_index=True)
                # df_bad_sort_values = df_bad.sort_values(by=df_bad.columns[3], ascending=True)
                # df_bad_sort_values = df_bad_sort_values.reset_index(drop=True)

                failed_condition = failed_condition.append(pd.DataFrame([self.test_input[i]],
                                                                        columns=self.feature_list),
                                                           ignore_index=True)


            else:
                good = good + 1

                df = df.append(pd.DataFrame([[i, self.test_target[i], self.prediction[i], Diff[i], Diff_per[i]]],
                                            columns=['index', 'target', 'expect', 'Diff(Cm)', 'Diff(%)']),
                               ignore_index=True)
                # df_sort_values = df.sort_values(by=df.columns[3], ascending=True)
                # df_sort_values = df_sort_values.reset_index(drop=True)

                pass_condition = pass_condition.append(pd.DataFrame([self.test_input[i]],
                                                                    columns=self.feature_list),
                                                       ignore_index=True)

        print()
        print('bad:', bad)
        print('good:', good)

        merge_bad_inner = pd.concat([df_bad, failed_condition], axis=1)
        merge_good_inner = pd.concat([df, pass_condition], axis=1)

        ## failed condition show-up
        ShowTable.fn_show_table("failed_condition", df=merge_bad_inner if len(merge_bad_inner.index) > 0 else None)

        ShowTable.fn_show_table("pass_condition", df=merge_good_inner if len(merge_good_inner.index) > 0 else None)

