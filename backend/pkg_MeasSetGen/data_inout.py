import os
from tkinter import filedialog
import pandas as pd
from datetime import datetime
import xlsxwriter


def loadfile():
    ## 데이터 파일 읽어오기.
    data = filedialog.askopenfilename(initialdir=".txt")
    encoding_data = pd.read_csv(data, sep="\t", encoding="cp949")

    return encoding_data


def arrangeParam(func):
    ## parameter 순서 변경.
    def wrapper(self):
        arrange_param = [
            "measSetComments",
            "probeId",
            "OrgBeamstyleIdx",
            "bsIndexTrace",
            "TxFrequencyHz",
            "TxFocusLocCm",
            "maxTxVoltageVolt",
            "ceilTxVoltageVolt",
            "profTxVoltageVolt",
            "totalVoltagePt",
            "numMeasVoltage",
            "NumTxElements",
            "TxpgWaveformStyle",
            "ProbeNumTxCycles",
            "ElevAperIndex",
            "zStartDistCm",
            "zMeasNum",
            "IsTxChannelModulationEn",
            "dumpSwVersion",
            "DTxFreqIndex",
            "VTxIndex",
            "IsPresetCpaEn",
            "TxPulseRle",
            "SystemPulserSel",
            "CpaDelayOffsetClk",
            "groupIndex",
            "zt_est",
            "probeName",
            "Mode",
            "SubModeIndex",
            "BeamStyleIndex",
            "SysTxFreqIndex",
            "isDuplicate",
        ]

        self.df = self.df.reindex(columns=arrange_param)
        return func(self)

    return wrapper


class DataOut:
    """
    폴더 생성 후, 파일 저장.
    """

    def __init__(self, case, database, df1, df2=None, probename=None):

        self.database = database

        current_datetime = datetime.now()
        self.formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M")
        self.df1 = df1
        self.df2 = df2
        self.probename = probename
        self.case = case

        if self.case == 0:
            ## MeasSetGen_files
            self.df = df1
            self.directory = f"./backend/0_MeasSetGen_files/{self.database}"

        elif self.case == 1:
            ## Verification_reports
            self.directory = f"./backend/1_Verification_Reports/{self.database}"

    def make_dir(self):
        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
                print(f"디렉토리 '{self.directory}'가 생성되었습니다.")
            except OSError as e:
                print(f"디렉토리 '{self.directory}' 생성 중 오류가 발생했습니다:", e)

    @arrangeParam
    def save_excel(self):
        if self.case == 0:
            self.df.to_csv(
                f"{self.directory}/meas_setting_{self.probename}_{self.formatted_datetime}_result.csv"
            )

        if self.case == 1:
            df_Intensity = pd.DataFrame(self.df1)
            df_Temperature = pd.DataFrame(self.df2)

            probename = df_Intensity["ProbeName"][0]
            probename = probename.strip()  ##문자열 앞뒤의 공백만 제거.

            # 엑셀 파일로 출력
            output_file = f"./backend/1_Verification_Reports/{self.database}/{probename}_{self.formatted_datetime}_result.xlsx"

            with pd.ExcelWriter(output_file, engine="xlsxwriter") as writer:
                df_Intensity.to_excel(writer, sheet_name="Intensity", index=False)
                df_Temperature.to_excel(writer, sheet_name="Temperature", index=False)
