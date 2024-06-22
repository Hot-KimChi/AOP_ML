import pymssql
import os
import pandas as pd


def fetchData():
    ## 데이터베이스에서 데이터를 가져오는 함수

    server_address = os.environ["SERVER_ADDRESS"]
    ID = os.environ["USER_NAME"]
    password = os.environ["PASSWORD"]
    list_database = os.environ["DB_ML"]

    print(list_database)

    SQL_list = []
    ## K2, Juniper, NX3, NX2 and FROSK
    for i in list_database:
        print(i)
        conn = pymssql.connect(server_address, ID, password, database=i)

        query = f"""
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
            """

        Raw_data = pd.read_sql(sql=query, con=conn)
        print(Raw_data["probeName"].value_counts(dropna=False))
        # AOP_data = Raw_data.dropna()
        SQL_list.append(Raw_data)

        return SQL_list


def preProcess():

    SQL_list = fetchData()
    ## 결합할 데이터프레임 list: SQL_list
    AOP_data = pd.concat(SQL_list, ignore_index=True)

    ## 결측치 제거 및 대체
    AOP_data["probeRadiusCm"] = AOP_data["probeRadiusCm"].fillna(0)
    AOP_data["probeElevAperCm1"] = AOP_data["probeElevAperCm1"].fillna(0)
    AOP_data["probeElevFocusRangCm1"] = AOP_data["probeElevFocusRangCm1"].fillna(0)
    AOP_data = AOP_data.drop(AOP_data[AOP_data["beamstyleIndex"] == 12].index)
    AOP_data = AOP_data.dropna()

    print(AOP_data.count())
    AOP_data.to_csv("AOP_data.csv")

    feature_list = [
        "txFrequencyHz",
        "focusRangeCm",
        "numTxElements",
        "txpgWaveformStyle",
        "numTxCycles",
        "elevAperIndex",
        "IsTxAperModulationEn",
        "probePitchCm",
        "probeRadiusCm",
        "probeElevAperCm0",
        "probeElevAperCm1",
        "probeElevFocusRangCm",
        "probeElevFocusRangCm1",
    ]
    ## feature 2개 추가.
    data = AOP_data[feature_list].to_numpy()
    target = AOP_data["zt"].to_numpy()

    return data, target
