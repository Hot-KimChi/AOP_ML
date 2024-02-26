import pandas as pd
import pymssql
import joblib


## SQL 데이터베이스에 접속하여 데이터 load.
## Command에 따라 query문 실행되게 수정완료.
def func_sql_get(server_address, ID, password, database, command):
    try:
        conn = pymssql.connect(server_address, ID, password, database)

        if command > 5:
            query = "f'''" + command + "'''"

        elif command == 0:
            query = f'''
            SELECT [probePitchCm], [probeRadiusCm], [probeElevAperCm0], [probeElevFocusRangCm] FROM probe_geo WHERE probeid = 11503103
            ORDER BY 1
            '''

        ## SQL에서 나온 데이터를 Pandas로 받아서 return.
        Raw_data = pd.read_sql(sql=query, con=conn)

        return Raw_data
        conn.close()

    except:
        print("Error: func_sql_get")


if __name__ == '__main__':
    ## 9C2 Meas-Setting condition 읽어오기(Pandas 형태)
    df = pd.read_csv('meas_setting_9C2_1st_LUT.csv')

    ## 9C2의 probeId를 기반으로 SQL에서 아래 데이터 가져오기
    est_geo = func_sql_get('kr001s1804srv', 'sel02776', '1qaz!QAZ', 'K2_r01_05', 0)
    df[['probePitchCm']] = est_geo['probePitchCm']
    df[['probeRadiusCm']] = est_geo['probeRadiusCm']
    df[['probeElevAperCm0']] = est_geo['probeElevAperCm0']
    df[['probeElevFocusRangCm']] = est_geo['probeElevFocusRangCm']


    ## 예측하기 위해 input 데이터 2D로 만들어서 변수 저장.
    est_params = df[['TxFrequencyHz', 'TxFocusLocCm', 'NumTxElements', 'TxpgWaveformStyle', 'ProbeNumTxCycles',
                     'elevAperIndex', 'IsTxChannelModulationEn', 'probePitchCm', 'probeRadiusCm', 'probeElevAperCm0',
                     'probeElevFocusRangCm']]

    ## 모델링한 모델읽어서 변수에 넣기
    loaded_model = joblib.load('RandomForest_v1_python37.pkl')
    ## 예측하기.
    zt_est = loaded_model.predict(est_params)

    ## 예측한 데이터를 Pandas DataFrame 형태로 저장.
    df_zt_est = pd.DataFrame(zt_est, columns=['zt_est'])

    df[['zt_est']] = round(df_zt_est, 1)
    print(df)