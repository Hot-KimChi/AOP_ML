

## B / C / D / M 모드 구분하여 중복 삭제하고 난 후, merge.
def fn_merge_df(self):

    df = self.df

    ##### B & M mode process #####
    df_B_mode = df.loc[(df['MODE'] == 'B')]
    df_M_mode = df.loc[(df['MODE'] == 'M')]
    df_C_mode = df.loc[df['MODE'] == 'Cb']
    df_D_mode = df.loc[df['MODE'] == 'D']
    df_CEUS_mode = df.loc[df['MODE'] == 'Contrast']

    ## 4개 모드 데이터프레임 합치기 / 합쳐진 데이터프레임 index reset / 데이터 Null --> [0]으로 변환(데이터의 정렬, groupby null 값 문제 발생)
    df_total = pd.concat([df_B_mode, df_M_mode, df_C_mode, df_D_mode, df_CEUS_mode])
    df_total = df_total.reset_index(drop=True)
    df_total = df_total.fillna(0)

    ## groupby count 를 위해 parameter setting
    self.group_params =['ISTXCHANNELMODULATIONEN', 'PROBENUMTXCYCLES', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE',
                         'TXPULSERLE', 'ELEVAPERINDEX', 'TXFOCUSLOCCM', 'NUMTXELEMENTS']

    ## 중복된 column 갯수 세기 --> 중복된 열 삭제됨.
    dup_count = df_total.groupby(self.group_params, as_index=False).size()

    ## 중복된 열 제거, 위쪽에 갯수와 동일하게 하기 위해, 동일하게 정열.
    ## 중복된 열 갯수를 df_total에 집어넣기.
    df_total = df_total.drop_duplicates(subset=self.group_params, keep='first')
    df_total = df_total.sort_values(by=self.group_params, ascending=True).reset_index()
    df_total['Count'] = dup_count['size']

    self.df = df_total
