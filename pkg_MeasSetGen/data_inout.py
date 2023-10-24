import os
from tkinter import filedialog
import pandas as pd
from datetime import datetime


def loadfile():
    ### 데이터 파일 읽어오기.
    data = filedialog.askopenfilename(initialdir='.txt')
    encoding_data = pd.read_csv(data, sep='\t', encoding='cp949')

    return encoding_data


class DataOut:
    """

    """

    def __init__(self, case, database, df1, df2=None, df3=None, probe=None, group_params=None):

        self.database = database

        current_datetime = datetime.now()
        self.formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M")
        self.df1 = df1
        self.df2 = df2
        self.df3 = df3

        self.case = case

        if self.case == 0:

            ## MeasSetGen_files
            self.df = df1
            self.group_params = group_params

            self.probe = probe
            idx = self.probe.find("|")
            self.probename = self.probe[:idx]
            self.directory = f'./0_MeasSetGen_files/{self.database}'

        elif self.case == 1:

            ## Verification_reports
            self.probename = probe
            self.directory = f'./0_Verification_Reports/{self.database}'


    def make_dir(self):

        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
                print(f"디렉토리 '{self.directory}'가 생성되었습니다.")
            except OSError as e:
                print(f"디렉토리 '{self.directory}' 생성 중 오류가 발생했습니다:", e)


    def save_excel(self):

        if self.case == 0:
            ## group param에서 SUBMODEINDEX 추가하여 정렬 준비 및 정렬하기
            sort_params = ['OrgBeamstyleIdx'] + self.group_params
            df_sort = self.df.sort_values(by=sort_params, ascending=True).reset_index()

            df_sort.to_csv(f'{self.directory}/meas_setting_{self.probename}_{self.formatted_datetime}_result.csv')


        if self.case == 1:

            df_MI = pd.DataFrame(self.df1)
            df_Ispta = pd.DataFrame(self.df2)
            df_Temp = pd.DataFrame(self.df3)

            self.probename = df_MI['probeName']

            # 엑셀 파일로 출력
            output_file = f'{self.directory}/verification_report_{self.probename}_{self.formatted_datetime}_result.xlsx'

            with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
                df_MI.to_excel(writer, sheet_name='MI', index=False)
                df_Ispta.to_excel(writer, sheet_name='Ispta.3', index=False)
                df_Temp.to_excel(writer, sheet_name='Temperature', index=False)
