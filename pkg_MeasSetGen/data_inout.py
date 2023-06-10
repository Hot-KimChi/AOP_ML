from tkinter import filedialog
import pandas as pd


class DataInOut:

    def __int__(self):
        self.initialize()


    def loadfile(self):
        ### 데이터 파일 읽어오기.
        self.data = filedialog.askopenfilename(initialdir='.txt')
        self.data = pd.read_csv(self.data, sep='\t', encoding='cp949')

        return self.data


    def dataout(self, group_params, df):
        ## group param에서 SUBMODEINDEX 추가하여 정렬 준비 및 정렬하기

        self.group_params = group_params
        self.df = df

        sort_params = ['OrgBeamstyleIdx'] + self.group_params
        df_sort = self.df.sort_values(by=sort_params, ascending=True).reset_index()

        ## data-out
        df = df_sort
        df.to_csv('./csv_files/check_20230131.csv')