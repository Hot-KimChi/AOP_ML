import pandas as pd


class ParamUpdate:

    """
    1) parameter 선정 진행
    2) selection한 데이터프레임을 기반으로 merge 작업진행: 중복을 제거하기 위해.
    """

    def __init__(self, df):
        self.df = df
        
        ## parameter selection
        list_param = ['Mode', 'SubModeIndex', 'BeamStyleIndex', 'SysTxFreqIndex', 'TxpgWaveformStyle', 
                      'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 
                      'IsPresetCpaEn', 'CpaDelayOffsetClk', 'ElevAperIndex', 'SystemPulserSel', 'VTxIndex', 
                      'TxPulseRle']
        self.selected_df = self.df.loc[:, list_param]
        
        ## sorting 은 안하는 것으로 결정. --> UE에서 #F에 따른 데이터를 구분하지 않기에.
        ## sorting parameter
        # self.sortParam = ['Mode', 'BeamStyleIndex', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles',
        #              'IsTxChannelModulationEn', 'ElevAperIndex', 'IsPresetCpaEn', 'CpaDelayOffsetClk',
        #              'TxFocusLocCm', 'TxPulseRle']
        
        # self.selected_df = self.selected_df.sort_values(by=self.sortParam, ascending=True).reset_index(drop=True)
        

    ## B / C / D / M 모드 구분하여 중복 삭제하고 난 후, merge.
    def param_merge(self):

        df = self.selected_df
        
        """
        1) focus 갯수를 파악하여 group index count --> 정렬하기 / 포커스가 올라가다가 내려가면 그룹인덱스가 다음 인덱스로 넘어감.
        2) 만약에 UE에서 중복이 된 condition을 request하면 어떻게 하는가? --> 나중에 해결
        3) 
        
        """
       
        
        ##### B & M mode process #####
        df_B_mode = df.loc[(df['Mode'] == 'B')]
        df_M_mode = df.loc[(df['Mode'] == 'M')]
        df_C_mode = df.loc[df['Mode'] == 'Cb']
        df_D_mode = df.loc[df['Mode'] == 'D']
        df_CEUS_mode = df.loc[df['Mode'] == 'Contrast']


        ## B and M-mode에서 중복된 부분 삭제 --> NumTxElement까지 포함하여 삭제하기.
        df_total_BM = pd.concat([df_B_mode, df_M_mode])
        df_total_BM = df_total_BM.reset_index(drop=True)
        df_total_BM = df_total_BM.fillna(0)
        
        
        
        # GroupIndex 열 생성
        group_index = 1
        group_indices = []
        prev_value = None
        for value in df_total_BM['TxFocusLocCm']:
            if prev_value is None or value >= prev_value:
                group_indices.append(group_index)
            else:
                group_index += 1
                group_indices.append(group_index)
            prev_value = value
        df_total_BM['GroupIndex'] = group_indices

        # 첫 번째 조건의 중복 제거
        group_params = ['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 
                        'TxPulseRle', 'ElevAperIndex', 'IsPresetCpaEn']
        data_no_duplicates = df_total_BM.drop_duplicates(subset=group_params, keep='first')


        # 두 번째 조건의 중복 제거 (GroupIndex에 따라 NumTxElements가 동일할 경우)
        def remove_group_duplicates(df):
            # GroupIndex별로 그룹핑
            grouped = df.groupby('GroupIndex')
            # 중복 제거된 데이터프레임을 저장할 리스트
            unique_rows = []
            for _, group in grouped:
                # 모든 NumTxElements 값이 동일한지 확인
                if group['NumTxElements'].nunique() == 1:
                    continue  # 중복된 그룹은 제외
                unique_rows.extend(group.to_dict('records'))
            return pd.DataFrame(unique_rows)

        # 적용
        df_total = remove_group_duplicates(data_no_duplicates)  
        
        

    #     ## groupby count 를 위해 parameter setting
    #     group_params_TxElement = ['IsTxChannelModulationEn', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'ProbeNumTxCycles', 
    #                             'TxPulseRle', 'ElevAperIndex', 'IsPresetCpaEn', 'TxFocusLocCm', 'NumTxElements'] 
    #     ## 중복된 column 갯수 세기 --> 중복된 열 삭제됨.
    #     dup_count = df_total_BM.groupby(group_params_TxElement, as_index=False).size()

    #   # 중복된 열 제거, 위쪽에 갯수와 동일하게 하기 위해, 동일하게 정열. / 중복된 열 갯수를 df_total에 집어넣기.
    #     df_total = df_total_BM.drop_duplicates(subset=group_params_TxElement, keep='first')
        
        
    #     # 그룹별로 행 수를 계산하여 'Count' 열에 추가
    #     df_total['Count'] = df_total[group_params_TxElement].merge(dup_count, on=group_params_TxElement, how='left')['size']
    #     df_total = df_total.sort_values(by=self.sortParam, ascending=True).reset_index(drop=True)

        ## Test code
        df_total.to_csv('test.csv')        

    #     ## 4개 모드 데이터프레임 합치기 / 합쳐진 데이터프레임 index reset 
    #     ## 데이터 Null --> [0]으로 변환(데이터의 정렬, groupby null 값 문제 발생)
    #     ## 1) df_B = df_M 일 경우, M 삭제
    #     # B_numTxElements = list(df_B_mode['NumTxElements'])
    #     # M_numTxElements = list(df_M_mode['NumTxElements'])
    #     # BC_numTxElements = list(df_C_mode['NumTxElements'])
    #     # D_numTxElements = list(df_D_mode['NumTxElements'])
                
    #     # if B_numTxElements == M_numTxElements:
    #     df_total = pd.concat([df_B_mode, df_M_mode, df_C_mode, df_D_mode, df_CEUS_mode])
        
        
    #     df_total = df_total.reset_index(drop=True)
    #     df_total = df_total.fillna(0)

    #     ## groupby count 를 위해 parameter setting
    #     group_params = ['IsTxChannelModulationEn', 'ProbeNumTxCycles', 'SysTxFreqIndex', 'TxpgWaveformStyle',
    #                    'TxPulseRle', 'ElevAperIndex', 'IsPresetCpaEn', 'TxFocusLocCm']

    #     ## 중복된 column 갯수 세기 --> 중복된 열 삭제됨.
    #     dup_count = df_total.groupby(group_params, as_index=False).size()

    #     ## 중복된 열 제거, 위쪽에 갯수와 동일하게 하기 위해, 동일하게 정열.
    #     ## 중복된 열 갯수를 df_total에 집어넣기.
    #     df_total = df_total.drop_duplicates(subset=group_params, keep='first')
    #     df_total = df_total.sort_values(by=group_params, ascending=True).reset_index()
    #     df_total['Count'] = dup_count['size']



        
        return df_total, group_params
