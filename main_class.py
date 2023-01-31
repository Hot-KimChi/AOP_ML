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
    def __init__(self, server_address, ID, password, database, command=None):
        super().__init__()
        self.server_address = server_address
        self.ID = ID
        self.password = password
        self.database = database
        self.command = command
        
    ## SQL 데이터베이스에 접속하여 데이터 load.
    def fn_sql_get(self):
        try:
            conn = pymssql.connect(self.server_address, self.ID, self.password, self.database)

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
        self.initialize()
        
        
    def initialize(self):
        config = configparser.ConfigParser()
        config.read('AOP_config.cfg')

        self.server_address = config["server address"]["address"]
        databases = config["database"]["name"]
        self.ID = config["username"]["ID"]
        self.password = config["password"]["PW"]
        server_table_M3 = config["server table"]["M3 server table"]
        Machine_Learning = config["Machine Learning"]["Model"]

        list_database = databases.split(',')
        self.list_M3_table = server_table_M3.split(',')
        self.list_ML = Machine_Learning.split(',')

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
        connect = SQL(self.server_address, self.ID, self.password, database, 1)
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
        # self.fn_predictML()
        
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
        connect = SQL(self.server_address, self.ID, self.password, database, 4)
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
        

if __name__ == '__main__':
    app = TopMain()  