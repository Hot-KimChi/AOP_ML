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


class SQL(object):
    def __init__(self, command=None):
        super().__init__()
        self.command = command
        
    ## SQL 데이터베이스에 접속하여 데이터 load.
    def fn_sql_get(self):
        try:
            conn = pymssql.connect(server_address, ID, password, database)

            if self.command > 5:
                query = "f'''" + self.command + "'''"

            # elif self.command == 0:
            #     if selected_DBtable == 'SSR_table':
            #         query = f'''
            #         SELECT * FROM meas_station_setup WHERE probeId = {selected_probeId}
            #         ORDER BY 1 desc
            #         '''
            #     else:
            #         query = f'''
            #         SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
            #         ORDER BY 1
            #         '''

            elif self.command == 1:
                query = '''
                SELECT probeName, probeId FROM probe_geo 
                order by probeName, probeId
                '''
            # elif command == 2:
            #     if selected_DBtable == 'SSR_table':
            #         query = f'''
            #         SELECT * FROM {selected_DBtable} WHERE measSSId IN {str_sel_param}
            #         ORDER BY measSSId, 1
            #         '''

            #     else:
            #         query = f'''
            #         SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
            #         ORDER BY 1
            #         '''

            # elif command == 3:
            #     if selected_DBtable == 'SSR_table':
            #         query = f'''
            #         SELECT * FROM meas_station_setup WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
            #         ORDER BY 1
            #         '''
            #     else:
            #         query = f'''
            #         SELECT * FROM {selected_DBtable} WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
            #         ORDER BY 1
            #         '''

            # probe_geo database load.
            elif self.command == 4:
                query = f'''
                SELECT [probePitchCm], [probeRadiusCm], [probeElevAperCm0], [probeElevFocusRangCm] FROM probe_geo WHERE probeid = {selected_probeId}
                ORDER BY 1
                '''

            # # Tx_summary database load.
            # elif command == 5:
            #     query = f'''
            #     SELECT * FROM Tx_summary WHERE probeid = {selected_probeId}
            #     ORDER BY 1
            #     '''


            Raw_data = pd.read_sql(sql=query, con=conn)

            return Raw_data
            conn.close()

        except:
            print("Error: func_sql_get")


    ## SQL data get from database.
    ## parameter 중 한 개를 선정하게 되면 filter 기능.
    def fn_SQL_value_filter(df=None, param=None):
        try:
            selected_param = param
            print(selected_param)
            list_datas = df['Software_version'].values.tolist()
            # list_datas = df[f'{selected_param}'].values.tolist()
            # list에서 unique한 데이터를 추출하기 위해 set으로 변경하여 고유값으로 변경 후, 다시 list로 변경.
            set_datas = set(list_datas)
            filtered_datas = list(set_datas)

            return filtered_datas

        except:
            print("Error: func_SQL_value")
    
class TopMain(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.initialize_loadConf()
        
        
    def initialize_loadConf(self):
        config = configparser.ConfigParser()
        config.read('AOP_config.cfg')
        
        global server_address, ID, password
        server_address = config["server address"]["address"]
        databases = config["database"]["name"]
        ID = config["username"]["ID"]
        password = config["password"]["PW"]
        server_table_M3 = config["server table"]["M3 server table"]
        Machine_Learning = config["Machine Learning"]["Model"]

        global list_ML, list_database
        list_database = databases.split(',')
        self.list_M3_table = server_table_M3.split(',')
        list_ML = Machine_Learning.split(',')

        ## Start tk 만들기.
        # root = Tk()
        self.title("DB 선택")
        self.geometry("280x150")
        self.resizable(False, False)

        label1 = Label(self, text='데이터베이스를 선택하세요')
        label1.place(x=10, y=10)

        # combo-Box 만들어서 데이터베이스만들기
        self.combo_login = ttk.Combobox(self, value=list_database)
        # combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
        self.combo_login.current(0)
        # combo-Box 의 위치
        self.combo_login.place(x=10, y=30)
        # login_combo.pack(pady=20)

        btn_login = Button(self, width=10, height=2, text='Login', command=self.fn_Menu)
        btn_login.place(x=180, y=10)

        self.mainloop()
        
        
    def fn_Menu(self):
        global database, list_probeIds, list_probe, list_probenames
        database = self.combo_login.get()

        window_Menu = tkinter.Toplevel()
        window_Menu.title(f"{database}" + ' / Menu')
        window_Menu.geometry("440x300")
        window_Menu.resizable(False, False)

        ## SQL class 객체 생성.
        connect = SQL(command = 1)
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


        btn_gen = Button(window_Menu, width=30, height=3, text='MeasSetGeneration', command=MeasSetGen)
        btn_gen.grid(row=0, column=0)

        # btn_sum = Button(frame_Menu, width=30, height=3, text='SQL Viewer', command=func_viewer_database)
        # btn_sum.grid(row=0, column=1)

        # btn_tx_sum = Button(frame_Menu, width=30, height=3, text='Tx Summary', command=func_tx_summ)
        # btn_tx_sum.grid(row=1, column=0)

        # btn_ML = Button(frame_Menu, width=30, height=3, text='Verification Report', command=func_verify_report)
        # btn_ML.grid(row=1, column=1)

        # btn_ML = Button(frame_Menu, width=30, height=3, text='Machine Learning', command=func_machine_learning)
        # btn_ML.grid(row=2, column=0)

        window_Menu.mainloop()
    
class MeasSetGen(object):
    
    def __init__(self):
        super().__init__()
        self.initialize()
        
        
    def initialize(self):
        window_gen = tkinter.Toplevel()
        window_gen.title(f"{database}" + ' / MeasSet_generation')
        window_gen.geometry("600x200")
        window_gen.resizable(False, False)

        frame1 = Frame(window_gen, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)

        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(frame1, value=list_probe, height=0, state='readonly')
        self.combo_probename.place(x=5, y=25)

        btn_load = Button(frame1, width=15, height=2, text='Select & Load', command=self._fn_gen_sequence)
        btn_load.place(x=200, y=5)

        btn_insert = Button(frame1, width=15, height=2, text='To MS-SQL', command=self.fn_dataout)
        btn_insert.place(x=350, y=5)

        frame2 = Frame(window_gen, relief="solid", bd=2)
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
        self.box_DumpSW = Entry(frame2, justify='center')
        self.box_DumpSW.grid(row=1, column=0)

        self.box_MaxVolt = Entry(frame2, justify='center')
        self.box_MaxVolt.grid(row=3, column=0)

        self.box_CeilVolt = Entry(frame2, justify='center')
        self.box_CeilVolt.grid(row=3, column=1)

        self.box_TotalVoltpt = Entry(frame2, justify='center')
        self.box_TotalVoltpt.grid(row=3, column=2)

        self.box_NumMeasVolt = Entry(frame2, justify='center')
        self.box_NumMeasVolt.grid(row=3, column=3)
        
        window_gen.mainloop()

    
    def _fn_gen_sequence(self):
        self.fn_loadfile()
        self.fn_select()
        self.fn_merge_df()
        self.fn_findOrgIdx()
        self.fn_bsIdx()
        self.fn_freqidx2Hz()
        self.fn_cnt_cycle()
        self.fn_calc_profvolt()
        self.fn_zMeasNum()
        self.fn_predictML()
        
        self.fn_dataout()
    
        
    def fn_loadfile(self):
        ### 데이터 파일 읽어오기.
        self.data = filedialog.askopenfilename(initialdir='.txt')
        self.data = pd.read_csv(self.data, sep='\t', encoding='cp949')
    
    
    def fn_select(self):    
        ## columns name to 대문자.
        self.data.columns = [x.upper() for x in self.data.columns]
        
        list_param = ['PROBENAME', 'MODE', 'SUBMODEINDEX', 'BEAMSTYLEINDEX', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE', 'TXFOCUSLOCCM', 'NUMTXELEMENTS',
                    'PROBENUMTXCYCLES', 'ISTXCHANNELMODULATIONEN', 'ISPRESETCPAEN', 'CPADELAYOFFSETCLK', 'TXPULSERLE', 'TXPGWAVEFORMLUT', 'ELEVAPERINDEX',
                    'SYSTEMPULSERSEL', 'VTXINDEX']
        
        ## list_param, 즉 선택한 parameter만 데이터프레임.
        self.df = self.data.loc[:, list_param]
        
        global selected_probeId
        selected_probeId = str(list_probeIds[self.combo_probename.current()])[1:-1]
        selected_probename = str(list_probenames[self.combo_probename.current()])        
        
        
        self.df['probeId'] = selected_probeId
        self.df['probeName'] = str(list_probenames[self.combo_probename.current()])
        self.df['maxTxVoltageVolt'] = self.box_MaxVolt.get()
        self.df['ceilTxVoltageVolt'] = self.box_CeilVolt.get()
        self.df['totalVoltagePt'] = self.box_TotalVoltpt.get()
        self.df['numMeasVoltage'] = self.box_NumMeasVolt.get()
        self.df['zStartDistCm'] = 0.5
        self.df['DTxFreqIndex'] = 0
        self.df['dumpSwVersion'] = self.box_DumpSW.get()
        self.df['measSetComments'] = f'Beamstyle_{selected_probename}_Intensity'
        
        
    def fn_merge_df(self):
        
        df = self.df
        
        ##### B & M mode process #####
        df_B_mode = df.loc[(df['MODE'] == 'B')]
        df_M_mode = df.loc[(df['MODE'] == 'M')]
        df_C_mode = df.loc[df['MODE'] == 'Cb']
        df_D_mode = df.loc[df['MODE'] == 'D']
        df_CEUS_mode = df.loc[df['MODE'] == 'Contrast']
                        
        ## 4개 모드 데이터프레임 합치기 / 합쳐진 데이터프레임 index reset / 데이터 Null --> [0]으로 변환(데이터의 정렬, groupby null 값 문제 발생)
        df_total = pd.concat([df_B_mode, df_M_mode, df_C_mode, df_D_mode, df_CEUS_mode])                                            
        df_total = df_total.reset_index(drop=True)                                                                          
        df_total = df_total.fillna(0)
                
        ## groupby count 를 위해 parameter setting 
        self.group_params =['ISTXCHANNELMODULATIONEN', 'PROBENUMTXCYCLES', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE', 'TXPULSERLE', 'ELEVAPERINDEX', 'TXFOCUSLOCCM', 'NUMTXELEMENTS']
        
        ## 중복된 column 갯수 세기 --> 중복된 열 삭제됨.
        dup_count = df_total.groupby(self.group_params, as_index=False).size()
        
        ## 중복된 열 제거, 위쪽에 갯수와 동일하게 하기 위해, 동일하게 정열.                
        ## 중복된 열 갯수를 df_total에 집어넣기.
        df_total = df_total.drop_duplicates(subset = self.group_params, keep='first')
        df_total = df_total.sort_values(by=self.group_params, ascending=True).reset_index()
        df_total['Count'] = dup_count['size']
        
        self.df = df_total
                
    
    def fn_findOrgIdx(self):
        
        orgindex = []
        
        for mode, subidx in zip(self.df['MODE'], self.df['SUBMODEINDEX']):
            if mode == 'B' and subidx == 0:
                orgindex.append(0)
            elif mode == 'B' and subidx == 1:
                orgindex.append(1)
            elif mode == 'Cb' and subidx == 0:
                orgindex.append(5)
            elif mode == 'D' and subidx == 0:
                orgindex.append(10)
            elif mode == 'M' and subidx == 0:
                orgindex.append(15)
            elif mode == 'M' and subidx == 1:
                orgindex.append(20)
        
        self.df['OrgBeamstyleIdx'] = orgindex
        
    
    ## bsIndexTrace algorithm    
    def fn_bsIdx(self):
        
        bsIndexTrace = []
        
        for orgidx, cnt in zip(self.df['OrgBeamstyleIdx'], self.df['Count']):
            if orgidx == 0 and cnt >= 2:
                bsIndexTrace.append(15)
            elif orgidx == 1 and cnt >= 2:
                bsIndexTrace.append(20)
            elif orgidx == 5 and cnt >= 2:
                bsIndexTrace.append(10)
            else:
                bsIndexTrace.append(0)
        
        self.df['bsIndexTrace'] = bsIndexTrace
           
        
    ## FrequencyIndex to FrequencyHz    
    def fn_freqidx2Hz(self):
        try:
            frequencyTable = [1000000, 1111100, 1250000, 1333300, 1428600, 1538500, 1666700, 1818200, 2000000, 2222200,
                              2500000, 2666700, 2857100, 3076900, 3333300, 3636400, 3809500, 4000000, 4210500, 4444400,
                              4705900, 5000000, 5333300, 5714300, 6153800, 6666700, 7272700, 8000000, 8888900, 10000000,
                              11428600, 13333333, 16000000, 20000000, 26666667, 11428600, 11428600, 11428600, 11428600, 11428600,
                              11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600] 
            
            
            FrequencyHz = []
            for i in self.df['SYSTXFREQINDEX'].values:
                FrequencyHz.append(frequencyTable[i])
            
            self.df['TxFrequencyHz'] = FrequencyHz
                        
        except:
            print("Error: fn_freqidx2Hz")
    
    # n = 0
    # FrequencyHz = []
    # for i in df_sort['SYSTXFREQINDEX'].values:
    #     FrequencyHz.insert(n, func_freqidx2Hz(i))
    #     n += 1
    # df_sort['TxFrequencyHz'] = FrequencyHz
    
    
    ## Calc_cycle for RLE code
    def fn_cnt_cycle(self):

        list_cycle = []
        for i in range(len(self.df['TXPGWAVEFORMSTYLE'])):
            if self.df['TXPGWAVEFORMSTYLE'][i] == 0:
                rle = self.df['TXPULSERLE'].str.split(":")[i]
                list_flt = list(map(float, rle))
                ## 아래 code도 가능.
                ## floatList = [float(x) for x in list_option]
                abs_value = np.abs(list_flt)

                calc = []
                for value in abs_value:
                    if 1 < value:
                        calc.append(round(value-1, 4))
                    else:
                        calc.append(value)
                cycle = round(sum(calc), 2)
                list_cycle.append(cycle)

            else:
                cycle = self.df['PROBENUMTXCYCLES'][i]
                list_cycle.append(cycle)
        
        self.df['ProbeNumTxCycles'] = list_cycle
    
    
    ## function: calc_profTxVoltage 구현
    def fn_calc_profvolt(self):
        try:
            profTxVoltageVolt = []
            for str_maxV, str_ceilV, str_totalpt in zip(self.df['maxTxVoltageVolt'], self.df['ceilTxVoltageVolt'], self.df['totalVoltagePt']):
                idx = 2
                ## tkinter에서 넘어오는 데이터 string.
                maxV = float(str_maxV)
                ceilV = float(str_ceilV)
                totalpt = int(str_totalpt)

                profTxVoltageVolt.append(round((min(maxV, ceilV)) ** ((totalpt-1-idx)/(totalpt-1)), 2))
            
            self.df['profTxVoltageVolt'] = profTxVoltageVolt

        except:
            print('error: func_profvolt')
    
    
    ## function: calc zMeasNum 구현
    def fn_zMeasNum(self):
        try:
            zStartDistCm = 0.5
            zMeasNum = []
            
            for focus in self.df['TXFOCUSLOCCM']:
                if (focus <= 3):
                    zMeasNum.append((5 - zStartDistCm) * 10)
                elif (focus <= 6):
                    zMeasNum.append((8 - zStartDistCm) * 10)
                elif (focus <= 9):
                    zMeasNum.append((12 - zStartDistCm) * 10)
                else:
                    zMeasNum.append((14 - zStartDistCm) * 10)
            
            self.df['zMeasNum'] = zMeasNum

        except:
            print('error: func_zMeaNum')
            
    
    def fn_predictML(self):
        ## predict by Machine Learning model.
        ## load modeling by pickle file.
        loaded_model = joblib.load('Model/RandomForest_v1_python37.pkl')

        ## take parameters for ML from measSet_gen file.
        est_params = self.df[['TxFrequencyHz', 'TXFOCUSLOCCM', 'NUMTXELEMENTS', 'TXPGWAVEFORMSTYLE', 'ProbeNumTxCycles', 'ELEVAPERINDEX', 'ISTXCHANNELMODULATIONEN']]
        connect = SQL(command = 4)
        est_geo = connect.fn_sql_get()


        est_params[['probePitchCm']] = est_geo['probePitchCm']
        est_params[['probeRadiusCm']] = est_geo['probeRadiusCm']
        est_params[['probeElevAperCm0']] = est_geo['probeElevAperCm0']
        est_params[['probeElevFocusRangCm']] = est_geo['probeElevFocusRangCm']


        zt_est = loaded_model.predict(est_params)
        df_zt_est = pd.DataFrame(zt_est, columns=['zt_est'])

        self.df['zt_est'] = round(df_zt_est, 1)
    
    
    def fn_dataout(self):
        
        ## group param에서 SUBMODEINDEX 추가하여 정렬 준비 및 정렬하기
        sort_params = ['OrgBeamstyleIdx'] + self.group_params
        df_sort = self.df.sort_values(by=sort_params, ascending=True).reset_index()
        
        ## data-out
        df = df_sort
        df.to_csv('./csv_files/check_20230131.csv')    
        

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
        combo_ML = ttk.Combobox(frame1, value=list_ML, width=35, height=0, state='readonly')
        combo_ML.place(x=5, y=25)

        btn_load = Button(frame1, width=15, height=2, text='Select & Train', command=self._fn_ML_sequence)
        btn_load.place(x=280, y=5)

        window_ML.mainloop()
    
    
    def _fn_ML_sequence(self):
        self.fn_preprocessML()
        
    
    def fn_preprocessML(self):
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
                        --,d.[probeElevFocusRangCm1]
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

            self.data = AOP_data[['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles',
                            'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm', 'probeRadiusCm', 'probeElevAperCm0', 
                            'probeElevFocusRangCm']].to_numpy()
            self.target = AOP_data['zt'].to_numpy()
        
        
        except:
            print('Error: fn_preprocessML')
        
   
    def fn_feature_import(self):
        try:
            df_import = pd.DataFrame()
            df_import = df_import.append(pd.DataFrame([np.round((self.model.feature_importances_) * 100, 2)],
                                        columns=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle', 'numTxCycles', 
                                                'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm', 'probeRadiusCm', 'probeElevAperCm0',
                                                'probeElevFocusRangCm']), ignore_index=True)

            func_show_table(f'{selected_ML}', df=df_import)

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
        
        train_input, test_input, train_target, test_target = train_test_split(self.data, self.target, test_size=0.2)

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
            self.model = RandomForestRegressor(max_depth=40, max_features='sqrt', min_samples_split=2, n_estimators=90, n_jobs=-1)


        ## Gradient Boosting
        elif selected_ML == 'Gradient_Boosting':
            from sklearn.ensemble import GradientBoostingRegressor
            self.model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.2)


        ## Histogram-based Gradient Boosting
        elif selected_ML == 'Histogram-based Gradient Boosting':
            from sklearn.experimental import enable_hist_gradient_boosting
            from sklearn.ensemble import HistGradientBoostingRegressor
            self.model = HistGradientBoostingRegressor()


        elif selected_ML == 'XGBoost':
            from xgboost import XGBRegressor
            self.model = XGBRegressor(tree_method='hist')


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

            self.model = VotingRegressor(estimators=[('ridge', model1), ('random', model2), ('neigh', model3)])


        ## LinearRegression 훈련하기.
        elif selected_ML == 'LinearRegression':

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(train_input)
            train_scaled = ss.transform(train_input)
            test_scaled = ss.transform(test_input)

            from sklearn.linear_model import LinearRegression
            self.model = LinearRegression()


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
            self.model = LinearRegression()

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
            self.model = Ridge(alpha=0.1)

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
                self.model = Ridge(alpha=alpha)
                self.model.fit(train_scaled, train_target)
                # 훈련점수 & 테스트점수
                train_score.append(self.model.score(train_scaled, train_target))
                test_score.append(self.model.score(test_scaled, test_target))

            plt.plot(np.log10(alpha_list), train_score)
            plt.plot(np.log10(alpha_list), test_score)
            plt.xlabel('alpha')
            plt.ylabel('R^2')
            plt.show()


        elif selected_ML == 'DecisionTreeRegressor(scaled data)':

            from sklearn.tree import DecisionTreeRegressor
            self.model = DecisionTreeRegressor(max_depth=10, random_state=42)

            from sklearn.preprocessing import StandardScaler
            ss = StandardScaler()
            ss.fit(train_input)
            train_scaled = ss.transform(train_input)
            test_scaled = ss.transform(test_input)

            self.model.fit(train_scaled, train_target)


            scores = cross_validate(self.model, train_scaled, train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            print('결정트리 - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
            print('결정트리 - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            # dt.fit(train_scaled, train_target)
            print('결정트리 - Test R^2:', np.round_(self.model.score(test_scaled, test_target), 3))
            prediction = self.model.predict(test_scaled)

            df_import = pd.DataFrame()
            df_import = df_import.append(pd.DataFrame([np.round((self.model.feature_importances_) * 100, 2)],
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
            plot_tree(self.model, max_depth=2, filled=True,
                    feature_names=['txFrequencyHz', 'focusRangeCm', 'numTxElements', 'txpgWaveformStyle',
                                    'numTxCycles', 'elevAperIndex', 'IsTxAperModulationEn', 'probePitchCm',
                                    'probeRadiusCm', 'probeElevAperCm0', 'probeElevFocusRangCm'])
            plt.show()


        elif selected_ML == 'DecisionTreeRegressor(No scaled data)':

            from sklearn.tree import DecisionTreeRegressor
            self.model = DecisionTreeRegressor(max_depth=10, random_state=42)
            self.model.fit(train_input, train_target)

            func_feature_import()

            ## plot_tree 이용하여 어떤 트리가 생성되었는지 확인.
            import matplotlib.pyplot as plt
            from sklearn.tree import plot_tree
            plt.figure(figsize=(10, 7))
            plot_tree(self.model, max_depth=1, filled=True,
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


            def fn_build_DNN():
                dense1 = keras.layers.Dense(100, activation='relu', input_shape=(11,), name='hidden')
                dense2 = keras.layers.Dense(10, activation='relu')
                dense3 = keras.layers.Dense(1)

                model = keras.Sequential([dense1, dense2, dense3])

                optimizer = tf.keras.optimizers.RMSprop(0.001)

                model.compile(loss='mse', optimizer=optimizer, metrics=['mae', 'mse'])
                return model

            self.model = fn_build_DNN()
            print(self.model.summary())

            example_batch = train_scaled[:10]
            example_result = self.model.predict(example_batch)
            print('example_batch 형태:', example_batch.shape)


            import matplotlib.pyplot as plt

            def plot_history(history):
                hist = pd.DataFrame(history.history)
                hist['epoch'] = history.epoch

                plt.figure(figsize=(8, 12))

                plt.subplot(2, 1, 1)
                plt.xlabel('Epoch')
                plt.ylabel('Mean Abs Error [Cm]')
                plt.plot(hist['epoch'], hist['mae'], label='Train Error')
                plt.plot(hist['epoch'], hist['val_mae'], label='Val Error')
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

            self.model = fn_build_DNN()

            # patience 매개변수는 성능 향상을 체크할 에포크 횟수입니다
            early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)
            history = self.model.fit(train_scaled, train_target, epochs=EPOCHS, validation_split=0.2, verbose=0,
                                callbacks=[early_stop, PrintDot()])

            hist = pd.DataFrame(history.history)
            hist['epoch'] = history.epoch
            print(hist.tail())

            plot_history(history)

            loss, mae, mse = self.model.evaluate(test_scaled, test_target, verbose=2)
            print("테스트 세트의 평균 절대 오차: {:5.2f} Cm".format(mae))


            ## 테스트 세트에 있는 샘플을 사용해 zt 값을 예측하여 비교하기.
            test_predictions = self.model.predict(test_scaled).flatten()
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
            self.model = model_fn()
            print(self.model.summary())

            rmsprop = keras.optimizers.RMSprop(0.001)
            self.model.compile(optimizer=rmsprop, loss='mse', metrics=['mae', 'mse'])

            checkpoint_cb = keras.callbacks.ModelCheckpoint('best-model.h5')
            early_stopping_cb = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
            history = self.model.fit(train_scaled, train_target, epochs=1000, validation_split=0.2, callbacks=[checkpoint_cb, early_stopping_cb])

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
            loss, mae, mse = self.model.evaluate(test_scaled, test_target, verbose=2)
            print('Test evaluate:', self.model.evaluate(test_scaled, test_target))
            print("테스트 세트의 평균 절대 오차: {:5.2f} Cm".format(mae))


            prediction = self.model.predict(test_scaled).flatten()


            ## np.round_ error check. => why does works for this sequence?
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
            joblib.dump(self.model, f'Model/{selected_ML}_v1_python37.pkl')


            scores = cross_validate(self.model, train_input, train_target, return_train_score=True, n_jobs=-1)
            print()
            print(scores)
            import numpy as np
            print(f'{selected_ML} - Train R^2:', np.round_(np.mean(scores['train_score']), 3))
            print(f'{selected_ML} - Train_validation R^2:', np.round_(np.mean(scores['test_score']), 3))

            self.model.fit(train_input, train_target)
            print(f'{selected_ML} - Test R^2:', np.round_(self.model.score(test_input, test_target), 3))
            prediction = np.round_(self.model.predict(test_input), 2)

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


                        ## np.round_ error check. => why does works for this sequence?
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


if __name__ == '__main__':
    app = TopMain()  