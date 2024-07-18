# import os
# import pandas as pd
# import pymssql


# class DBInfor(object):
#     def __init__(self):
#         self.server_address = os.environ["SERVER_ADDRESS"]
#         self.ID = os.environ["USER_NAME"]
#         self.password = os.environ["PASSWORD"]
#         self.database = os.environ["DATABASE"]


# class SQL(DBInfor):
#     def __init__(
#         self,
#         command=None,
#         selected_DBtable=None,
#         selected_probeId=None,
#         selected_measSSId=None,
#         selected_param=None,
#         sel_data=None,
#         sorted_param=None,
#         report_term=None,
#         data=None,
#     ):

#         super().__init__()

#         self.command = command
#         self.selected_DBtable = selected_DBtable
#         self.selected_probeId = selected_probeId
#         self.selected_measSSId = selected_measSSId
#         self.selected_param = selected_param
#         self.sel_data = sel_data
#         self.sorted_param = sorted_param
#         self.report_term = report_term
#         self.df = data

#     ## SQL 데이터베이스에 접속하여 데이터 load.
#     def sql_get(self):
#         try:
#             conn = pymssql.connect(
#                 self.server_address, self.ID, self.password, self.database
#             )
#             query = self.build_query()

#             if query:
#                 # print(query)
#                 Raw_data = pd.read_sql(sql=query, con=conn)

#                 conn.commit()
#                 conn.close()

#                 return Raw_data
#             else:
#                 return pd.DataFrame()

#         except Exception as e:
#             print(f"Error: sql_get function{e}")
#             return pd.DataFrame()

#     def sql_parse(self):
#         try:
#             conn = pymssql.connect(
#                 self.server_address, self.ID, self.password, self.database
#             )
#             query = self.build_query()

#             cursor = conn.cursor()

#             if self.command == 10:  ## DataFrame parsing.
#                 for row in self.df.itertuples():
#                     cursor.execute(
#                         query,
#                         (
#                             row.ProbeName,
#                             row.ProbeID,
#                             row.Software_version,
#                             row.Exam,
#                             row.CurrentState,
#                             row.BeamStyleIndex,
#                             row.TxFrequency,
#                             row.TxFreqIndex,
#                             row.ElevAperIndex,
#                             row.NumTxCycles,
#                             row.TxpgWaveformStyle,
#                             row.TxChannelModulationEn,
#                             row.Dual_Mode,
#                             row.SubModeIndex,
#                             row.IsProcessed,
#                             row.IsCPAEn,
#                             row.RLE,
#                             row.VTxIndex,
#                             row.IsLatest,
#                         ),
#                     )
#             elif self.command == 9:  ## IsLatest set = 0
#                 cursor.execute(query)

#             # 트랜잭션 커밋 및 연결 종료
#             conn.commit()
#             conn.close()

#         except Exception as e:
#             print(f"Error: {e}")

#     def build_query(self):

#         if self.command == 0:
#             if self.selected_DBtable == "SSR_table":
#                 query = f"""
#                 SELECT * FROM meas_station_setup WHERE probeId = {self.selected_probeId}
#                 ORDER BY 1 desc
#                 """
#             else:
#                 query = f"""
#                 SELECT * FROM {self.selected_DBtable} WHERE probeId = {self.selected_probeId}
#                 ORDER BY 1 desc
#                 """

#         elif self.command == 1:
#             query = """
#             SELECT probeName, probeId FROM probe_geo
#             order by probeName, probeId
#             """

#         elif self.command == 2:
#             if self.selected_DBtable == "SSR_table":
#                 query = f"""
#                 SELECT * FROM {self.selected_DBtable} WHERE measSSId IN {self.selected_measSSId}
#                 ORDER BY measSSId, 1
#                 """

#             else:
#                 query = f"""
#                 SELECT * FROM {self.selected_DBtable} WHERE probeId = {self.selected_probeId}
#                 ORDER BY 1
#                 """

#         elif self.command == 3:
#             if self.selected_DBtable == "SSR_table":
#                 query = f"""
#                 SELECT * FROM meas_station_setup WHERE probeid = {self.selected_probeId} and {self.selected_param} = '{self.sel_data}'
#                 ORDER BY 1 desc
#                 """
#             else:
#                 query = f"""
#                 SELECT * FROM {self.selected_DBtable} WHERE probeid = {self.selected_probeId} and {self.selected_param} = '{self.sel_data}'
#                 ORDER BY 1 desc
#                 """

#         ## probe_geo database load.
#         elif self.command == 4:
#             query = f"""
#             SELECT [probePitchCm], [probeRadiusCm], [probeElevAperCm0], [probeElevAperCm1], [probeElevFocusRangCm], [probeElevFocusRangCm1]
#             FROM probe_geo WHERE probeid = {self.selected_probeId}
#             ORDER BY 1
#             """

#         ## meas_station_setup database load
#         elif self.command == 5:
#             query = f"""
#                 SELECT * FROM meas_station_setup
#                 ORDER BY 1 desc
#                 """

#         ## For selected probeId, load meas_station_setup
#         elif self.command == 6:
#             query = f"""
#             SELECT * FROM meas_station_setup WHERE probeid = {self.selected_probeId}
#             ORDER BY 1 desc
#             """

#         elif self.command == 7:
#             query = f"""
#             SELECT
#             T.tempvrfid AS WCSId,
#             T.tempVrfResID,
#             T.DataUsable,
#             S.probeName,
#             S.Exam,
#             S.measSSId,
#             T.Mode,
#             T.TxFrequencyHz,
#             T.ElevIndex,
#             T.NumTxCycles,
#             T.WaveformStyle,
#             T.ChModulationEn,
#             T.SystemVolt,
#             T.MeasPurpose,
#             S.SSRId,
#             S.reportTerm_1,
#             S.XP_Value_1,
#             S.reportValue_1,
#             S.Difference_1,
#             S.Ambient_Temp_1

#             FROM dbo.tempVrf_result AS T

#             INNER JOIN dbo.SSR_table AS S
#             ON T.tempVrfId = S.WCSId and T.tempVrfResID = S.measResId

#             WHERE S.measSSId IN ({self.selected_measSSId}) and T.MeasPurpose IN ('TMM', 'Still Air')
#             order by tempVrfResID, MeasPurpose, WCSId
#             """

#         ## verification Report Step
#         elif self.command == 8:
#             query = f"""
#             SELECT * FROM (
#                 SELECT  TOP (100) PERCENT
#                     dbo.Tx_summary.Num, dbo.Tx_summary.ProbeName, dbo.Tx_summary.ProbeID, dbo.Tx_summary.Software_version, dbo.Tx_summary.Exam,
#                     dbo.Tx_summary.CurrentState,dbo.Tx_summary.Dual_Mode, dbo.Tx_summary.BeamStyleIndex, dbo.Tx_summary.TxFrequency,
#                     dbo.Tx_summary.ElevAperIndex, dbo.Tx_summary.NumTxCycles, dbo.WCS.NumTxCycles AS WCS_Cycle,
#                     dbo.Tx_summary.TxpgWaveformStyle, dbo.Tx_summary.TxChannelModulationEn, dbo.Tx_summary.IsCPAEn,
#                     dbo.Tx_summary.RLE, dbo.SSR_table.WCSId, dbo.SSR_table.SSRId, dbo.SSR_table.reportTerm_1,
#                     dbo.SSR_table.XP_Value_1, dbo.SSR_table.reportValue_1, dbo.SSR_table.Difference_1,
#                     dbo.SSR_table.Ambient_Temp_1, dbo.SSR_table.reportTerm_2, dbo.SSR_table.XP_Value_2,
#                     dbo.SSR_table.reportValue_2, dbo.SSR_table.Difference_2,
#                     ROW_NUMBER() over (partition by num order by {self.sorted_param} desc) as RankNo,
#                     dbo.meas_res_summary.isDataUsable, dbo.Tx_summary.IsLatest

#                 FROM dbo.Tx_summary

#                 LEFT OUTER JOIN dbo.WCS
#                     ON dbo.Tx_summary.ProbeID = dbo.WCS.probeId AND dbo.Tx_summary.BeamStyleIndex = dbo.WCS.Mode
#                     AND dbo.Tx_summary.TxFreqIndex = dbo.WCS.TxFrequencyIndex AND dbo.Tx_summary.ElevAperIndex = dbo.WCS.ElevAperIndex
#                     AND dbo.Tx_summary.TxpgWaveformStyle = dbo.WCS.WaveformStyle AND dbo.Tx_summary.TxChannelModulationEn = dbo.WCS.ChModulationEn
#                     AND dbo.Tx_summary.CurrentState = dbo.WCS.CurrentState AND dbo.Tx_summary.Dual_Mode = dbo.WCS.InterpolateFactor
#                     AND dbo.Tx_summary.IsCPAEn = dbo.WCS.IsCPAEn
#                     AND (dbo.Tx_summary.TxpgWaveformStyle <> 0						-- TxpgWaveformStyle가 0이 아닌 경우
#                         OR (dbo.Tx_summary.TxpgWaveformStyle = 0					-- TxpgWaveformStyle가 0인 경우
#                         AND dbo.Tx_summary.RLE = dbo.WCS.TxPulseRleA))				-- TxPulseRleA와 RLE를 비교
#                     AND (dbo.Tx_summary.CurrentState = 'D'							-- CurrentState가 D인 경우
#                         OR (dbo.Tx_summary.CurrentState <> 'D'						-- CurrentState가 D가 아닌 경우
#                         AND dbo.Tx_summary.NumTxCycles = dbo.WCS.NumTxCycles))		-- NumTxCycles와 NumTxCycles를 비교

#                 LEFT OUTER JOIN dbo.meas_res_summary
#                     ON dbo.WCS.wcsID = dbo.meas_res_summary.VerifyID

#                 LEFT OUTER JOIN dbo.SSR_table
#                     ON dbo.SSR_table.probeName NOT LIKE '%notuse%' AND dbo.WCS.wcsID = dbo.SSR_table.WCSId
#                     AND dbo.SSR_table.measSSId IN {self.selected_measSSId}

#                 where reportTerm_1 = '{self.report_term}' or reportTerm_1 IS NULL
#                 ) T

#             where RankNo = 1 and ProbeID = {self.selected_probeId} and IsLatest = 1
#             order by num
#             """

#         ## parsing MS-SQL database: Tx_summary_table / IsLatest = 0 update before parsing Tx summary data
#         elif self.command == 9:
#             query = f"""
#             UPDATE dbo.Tx_summary SET IsLatest = 0
#             WHERE ProbeID = {self.selected_probeId}
#            """

#         ## parsing MS-SQL database: Tx_summary_table
#         elif self.command == 10:
#             query = f"""
#            INSERT INTO Tx_summary(
#                  [ProbeName]
#                 ,[ProbeID]
#                 ,[Software_version]
#                 ,[Exam]
#                 ,[CurrentState]
#                 ,[BeamStyleIndex]
#                 ,[TxFrequency]
#                 ,[TxFreqIndex]
#                 ,[ElevAperIndex]
#                 ,[NumTxCycles]
#                 ,[TxpgWaveformStyle]
#                 ,[TxChannelModulationEn]
#                 ,[Dual_Mode]
#                 ,[SubModeIndex]
#                 ,[IsProcessed]
#                 ,[IsCPAEn]
#                 ,[RLE]
#                 ,[VTxIndex]
#                 ,[IsLatest]
#             )

#             VALUES (%s, %s, %s, %s, %s,
#                     %s, %s, %s, %s, %s,
#                     %s, %s, %s, %s, %s,
#                     %s, %s, %s, %s)
#             """

#         return query

#     ## SQL data get from database.
#     ## parameter 중 한 개를 선정하게 되면 filter 기능.
#     def sql_filter(df=None, param=None):
#         try:
#             selected_param = param
#             print(selected_param)
#             list_datas = df["Software_version"].values.tolist()

#             # list_datas = df[f'{selected_param}'].values.tolist()
#             # list에서 unique한 데이터를 추출하기 위해 set으로 변경하여 고유값으로 변경 후, 다시 list로 변경.
#             set_datas = set(list_datas)
#             filtered_datas = list(set_datas)

#             return filtered_datas

#         except:
#             print("Error: func_SQL_value")


import pyodbc
import pandas as pd
import os


class SQL:
    def __init__(self, command=1, windows_auth=False):
        self.server = os.environ.get("SERVER_ADDRESS_ADDRESS")
        self.database = os.environ.get("DATABASE_NAME")
        # self.username = os.environ.get('DATABASE_USERNAME')
        # self.password = os.environ.get('DATABASE_PASSWORD')
        self.command = command
        self.windows_auth = windows_auth

    def connect(self):
        if self.windows_auth:
            conn_str = f"DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;"
        # else:
        #     conn_str = f'DRIVER={{SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'

        return pyodbc.connect(conn_str)

    def sql_get(self):
        conn = self.connect()
        cursor = conn.cursor()

        if self.command == 1:
            query = "SELECT * FROM ProbeInfo"
        else:
            query = "SELECT * FROM OtherTable"  # 다른 명령에 대한 쿼리

        df = pd.read_sql(query, conn)
        conn.close()
        return df

    def sql_execute(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()
        conn.close()
