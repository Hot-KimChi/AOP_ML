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
databases = ['Frosk_r03', 'K2_r01_05', 'Griffin_r01']

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
    AOP_data = AOP_data.append(AOP_data, ignore_index=True)

print(AOP_data.count())