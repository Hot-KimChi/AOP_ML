import pandas as pd
import pymssql


class DBInfor(object):
    def __init__(self, server_address, server_id, password, database):
        self.server_address = server_address
        self.ID = server_id
        self.password = password
        self.database = database


class SQL(DBInfor):
    def __init__(self, server_address, server_id, password, database,
                 command=None, selected_DBtable=None, selected_probeId=None,
                 selected_measSSId=None, selected_param=None, sel_data=None):

        super().__init__(server_address, server_id, password, database)

        self.command = command
        self.selected_DBtable = selected_DBtable
        self.selected_probeId = selected_probeId
        self.selected_measSSId = selected_measSSId
        self.selected_param = selected_param
        self.sel_data = sel_data

    ## SQL 데이터베이스에 접속하여 데이터 load.
    def sql_get(self):
        try:
            conn = pymssql.connect(self.server_address, self.ID, self.password, self.database)

            if self.command > 7:
                query = "f'''" + self.command + "'''"

            elif self.command == 0:
                if self.selected_DBtable == 'SSR_table':
                    query = f'''
                    SELECT * FROM meas_station_setup WHERE probeId = {self.selected_probeId}
                    ORDER BY 1 desc
                    '''
                else:
                    query = f'''
                    SELECT * FROM {self.selected_DBtable} WHERE probeId = {self.selected_probeId}
                    ORDER BY 1
                    '''


            elif self.command == 1:
                query = '''
                SELECT probeName, probeId FROM probe_geo 
                order by probeName, probeId
                '''


            elif self.command == 2:
                if self.selected_DBtable == 'SSR_table':
                    query = f'''
                    SELECT * FROM {self.selected_DBtable} WHERE measSSId IN {self.selected_measSSId}
                    ORDER BY measSSId, 1
                    '''

                else:
                    query = f'''
                    SELECT * FROM {self.selected_DBtable} WHERE probeId = {self.selected_probeId}
                    ORDER BY 1
                    '''


            elif self.command == 3:
                if self.selected_DBtable == 'SSR_table':
                    query = f'''
                    SELECT * FROM meas_station_setup WHERE probeid = {self.selected_probeId} and {self.selected_param} = '{self.sel_data}' 
                    ORDER BY 1 desc
                    '''
                else:
                    query = f'''
                    SELECT * FROM {self.selected_DBtable} WHERE probeid = {self.selected_probeId} and {self.selected_param} = '{self.sel_data}' 
                    ORDER BY 1 desc
                    '''


            ## probe_geo database load.
            elif self.command == 4:
                query = f'''
                SELECT [probePitchCm], [probeRadiusCm], [probeElevAperCm0], [probeElevFocusRangCm] FROM probe_geo WHERE probeid = {self.selected_probeId}
                ORDER BY 1
                '''


            ## meas_station_setup database load
            elif self.command == 5:
                query = f'''
                    SELECT * FROM meas_station_setup
                    ORDER BY 1 desc
                    '''


            elif self.command == 6:
                query = f'''
                SELECT * FROM meas_station_setup WHERE probeid = {self.selected_probeId}
                ORDER BY 1 desc
                '''


            elif self.command == 7:
                query = f'''
                SELECT
                T.tempvrfid AS WCSId,
                T.tempVrfResID,
                T.DataUsable,
                S.probeName,	
                S.Exam, 
                S.measSSId, 
                T.Mode, 
                T.TxFrequencyHz, 
                T.ElevIndex, 
                T.NumTxCycles, 
                T.WaveformStyle, 
                T.ChModulationEn, 
                T.SystemVolt,
                T.MeasPurpose,	
                S.SSRId, 
                S.reportTerm_1, 
                S.XP_Value_1,
                S.reportValue_1, 
                S.Difference_1, 
                S.Ambient_Temp_1 

                FROM dbo.tempVrf_result AS T

                INNER JOIN dbo.SSR_table AS S
                ON T.tempVrfId = S.WCSId and T.tempVrfResID = S.measResId

                WHERE S.measSSId IN ({self.selected_measSSId}) and T.MeasPurpose IN ('TMM', 'Still Air')
                order by tempVrfResID, MeasPurpose, WCSId
                '''

            Raw_data = pd.read_sql(sql=query, con=conn)

            return Raw_data
            conn.close()

        except:
            print("Error: fn_sql_get")

    ## SQL data get from database.
    ## parameter 중 한 개를 선정하게 되면 filter 기능.
    def sql_filter(df=None, param=None):
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