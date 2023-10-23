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

    def __init__(self, database, probe, df, group_params):

        self.database = database
        self.df = df
        self.group_params = group_params

        self.probe = probe
        idx = self.probe.find("|")
        self.probename = self.probe[:idx]

        current_datetime = datetime.now()
        self.formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M")

        self.directory = f'./0_MeasSetGen_files/{self.database}'

        self.make_dir()
        self.data_out()


    def make_dir(self):

        if not os.path.exists(self.directory):
            try:
                os.makedirs(self.directory)
                print(f"디렉토리 '{self.directory}'가 생성되었습니다.")
            except OSError as e:
                print(f"디렉토리 '{self.directory}' 생성 중 오류가 발생했습니다:", e)


    def data_out(self):

        ## group param에서 SUBMODEINDEX 추가하여 정렬 준비 및 정렬하기
        sort_params = ['OrgBeamstyleIdx'] + self.group_params
        df_sort = self.df.sort_values(by=sort_params, ascending=True).reset_index()

        df_sort.to_csv(f'{self.directory}/meas_setting_{self.probename}_{self.formatted_datetime}_result.csv')

        return df_sort
