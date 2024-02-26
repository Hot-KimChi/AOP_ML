import pymssql
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import ttk
from functools import partial
import configparser
import warnings
from tkinter import filedialog

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

## K2, Juniper, NX3, NX2 and FROSK
server_address = 'kr001s1804srv'
ID = 'sel02776'
password = '1qaz!QAZ'
databases = ['K2_r01_05', 'Griffin_r01', 'Frosk_r03', 'New_Trees']


res_df_list = []
for i in databases:
    database = i
    print(database)
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
    res_df_list.append(Raw_data)
    
    # AOP_data = Raw_data
    # AOP_data.to_csv(f'data_{database}.csv')

AOP_data = pd.concat(res_df_list, ignore_index=True)

print('before data_shape:', AOP_data.shape)
## 결측치 제거 및 대체
AOP_data['probeRadiusCm'] = AOP_data['probeRadiusCm'].fillna(0)
AOP_data['probeElevAperCm1'] = AOP_data['probeElevAperCm1'].fillna(0)
AOP_data['probeElevFocusRangCm1'] = AOP_data['probeElevFocusRangCm1'].fillna(0)
AOP_data = AOP_data.drop(AOP_data[AOP_data['beamstyleIndex'] == 12].index)
AOP_data = AOP_data.dropna()

print('after data_shape:', AOP_data.shape)

print(AOP_data.count())
AOP_data.to_csv('AOP_data.csv')


