from tkinter import filedialog
import pandas as pd


def loadfile():
    ### 데이터 파일 읽어오기.
    data = filedialog.askopenfilename(initialdir='.txt')
    encoding_data = pd.read_csv(data, sep='\t', encoding='cp949')

    return encoding_data


def data_out(df, group_params):
    ## group param에서 SUBMODEINDEX 추가하여 정렬 준비 및 정렬하기

    sort_params = ['OrgBeamstyleIdx'] + group_params
    df_sort = df.sort_values(by=sort_params, ascending=True).reset_index()

    ## data-out
    df_sort.to_csv('./csv_files/check_20230131.csv')
