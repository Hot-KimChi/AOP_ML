import pandas as pd
import pymssql
import joblib


## SQL 데이터베이스에 접속하여 데이터 load.
def func_sql_get(server_address, ID, password, database, command):
    try:
        conn = pymssql.connect(server_address, ID, password, database)

        if command > 5:
            query = "f'''" + command + "'''"

        elif command == 0:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM meas_station_setup WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''

        elif command == 1:
            query = '''
            SELECT probeName, probeId FROM probe_geo 
            order by probeName, probeId
            '''
        elif command == 2:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE measSSId = {sel_param_click}
                ORDER BY measSSId, 1
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''

        elif command == 3:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM meas_station_setup WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
                ORDER BY 1
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
                ORDER BY 1
                '''

        elif command == 4:
            query = f'''
            SELECT [probePitchCm], [probeRadiusCm], [probeElevAperCm0], [probeElevFocusRangCm] FROM probe_geo WHERE probeid = 11503103
            ORDER BY 1
            '''


        Raw_data = pd.read_sql(sql=query, con=conn)

        return Raw_data
        conn.close()

    except:
        print("Error: func_sql_get")


df = pd.read_csv('./meas_setting_9C2_1st_LUT.csv')
est_geo = func_sql_get('kr001s1804srv', 'sel02776', '1qaz!QAZ', 'K2_r01_05', 4)

# pitch = est_geo['probePitchCm']
# radius = est_geo['probeRadiusCm']
# elevaper = est_geo['probeElevAperCm0']
# elevfocus = est_geo['probeElevFocusRangCm']

df[['probePitchCm']] = est_geo['probePitchCm']
df[['probeRadiusCm']] = est_geo['probeRadiusCm']
df[['probeElevAperCm0']] = est_geo['probeElevAperCm0']
df[['probeElevFocusRangCm']] = est_geo['probeElevFocusRangCm']

est_params = df[['TxFrequencyHz', 'TxFocusLocCm', 'NumTxElements', 'TxpgWaveformStyle',
                       'ProbeNumTxCycles', 'elevAperIndex', 'IsTxChannelModulationEn', 'probePitchCm', 'probeRadiusCm',
                 'probeElevAperCm0', 'probeElevFocusRangCm']]

loaded_model = joblib.load('./RandomForest_v1_python37.pkl')
zt_est = loaded_model.predict(est_params)
print(zt_est)
print(type(zt_est))
df_zt_est = pd.DataFrame(zt_est, columns=['zt_est'])

print(df_zt_est)
print(type(df_zt_est))

df = pd.concat([est_params, df_zt_est])
print(df)