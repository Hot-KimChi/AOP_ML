import pymssql

## SQL 데이터베이스에 접속하여 데이터 load.
def fn_sql_get(self):
    try:
        conn = pymssql.connect(server_address, ID, password, database)

        if self.command > 7:
            query = "f'''" + self.command + "'''"

        elif self.command == 0:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM meas_station_setup WHERE probeId = {selected_probeId}
                ORDER BY 1 desc
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''

        elif self.command == 1:
            query = '''
            SELECT probeName, probeId FROM probe_geo 
            order by probeName, probeId
            '''

        elif self.command == 2:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE measSSId IN {str_sel_param}
                ORDER BY measSSId, 1
                '''

            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeId = {selected_probeId}
                ORDER BY 1
                '''

        elif self.command == 3:
            if selected_DBtable == 'SSR_table':
                query = f'''
                SELECT * FROM meas_station_setup WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
                ORDER BY 1 desc
                '''
            else:
                query = f'''
                SELECT * FROM {selected_DBtable} WHERE probeid = {selected_probeId} and {selected_param} = '{sel_data}' 
                ORDER BY 1 desc
                '''

        ## probe_geo database load.
        elif self.command == 4:
            query = f'''
            SELECT [probePitchCm], [probeRadiusCm], [probeElevAperCm0], [probeElevFocusRangCm] FROM probe_geo WHERE probeid = {selected_probeId}
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
            SELECT * FROM meas_station_setup WHERE probeid = {selected_probeId}
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

            WHERE S.measSSId IN ({str_sel_param}) and T.MeasPurpose IN ('TMM', 'Still Air')
            order by tempVrfResID, MeasPurpose, WCSId
            '''

        Raw_data = pd.read_sql(sql=query, con=conn)

        return Raw_data
        conn.close()

    except:
        print("Error: fn_sql_get")


