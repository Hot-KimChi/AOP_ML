from tkinter import filedialog
import pandas as pd


def loadfile():
    ### 데이터 파일 읽어오기.
    data = filedialog.askopenfilename(initialdir='.txt')
    encoding_data = pd.read_csv(data, sep='\t', encoding='cp949')

    return encoding_data


class Dataout:
    def __init__(self, df, group_params):
        self.df = df
        self.group_parmas = group_params

    def make_dir(self):



    def data_out(self):
        ## group param에서 SUBMODEINDEX 추가하여 정렬 준비 및 정렬하기
        sort_params = ['OrgBeamstyleIdx'] + self.group_params

        df_sort = self.df.sort_values(by=sort_params, ascending=True).reset_index()

        df_sort.to_csv('result.csv')

        return df_sort
