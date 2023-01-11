import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from tkinter import filedialog

if __name__ == '__main__':
    
    data = filedialog.askopenfilename(initialdir='.txt')
    data = pd.read_csv(data, sep='\t', encoding='cp949')
    
    ## columns name to 대문자.
    data.columns = [x.upper() for x in data.columns]
    
    list_param = ['PROBENAME', 'MODE', 'SUBMODEINDEX', 'BEAMSTYLEINDEX', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE', 'TXFOCUSLOCCM', 'NUMTXELEMENTS',
                  'PROBENUMTXCYCLES', 'ISTXCHANNELMODULATIONEN', 'ISPRESETCPAEN', 'CPADELAYOFFSETCLK', 'TXPULSERLE', 'TXPGWAVEFORMLUT', 'ELEVAPERINDEX',
                  'SYSTEMPULSERSEL', 'VTXINDEX']
    
    selected_data = data.loc[:, list_param]
    
    ##############################
    ##### B & M mode process #####
    df_B_mode = selected_data.loc[(selected_data['MODE'] == 'B')]
    df_M_mode = selected_data.loc[(selected_data['MODE'] == 'M')]
    df_C_mode = selected_data.loc[selected_data['MODE'] == 'Cb']
    df_D_mode = selected_data.loc[selected_data['MODE'] == 'D']
    df_CEUS_mode = selected_data.loc[selected_data['MODE'] == 'Contrast']
    
    
    ## 4개 모드 데이터프레임 합치기
    ## 합쳐진 데이터프레임 index reset
    df_total = pd.concat([df_B_mode, df_M_mode, df_C_mode, df_D_mode, df_CEUS_mode])                                            
    df_total = df_total.reset_index(drop=True)                                                                          
    
    
    ## 데이터 Null --> [0]으로 변환(데이터의 정렬, groupby null 값 문제 발생)
    df_total = df_total.fillna(0)
    
    
    ## duplicated parameter check. => dup = df.duplicated(['SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 'TxPulseRle'], keep='first')
    ## 중복된 parameter가 있을 경우, 제거하기.
    ## group_param 기준으로 데이터 정렬하기
    group_params =['ISTXCHANNELMODULATIONEN', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE', 'PROBENUMTXCYCLES', 'TXPULSERLE', 'TXFOCUSLOCCM', 'NUMTXELEMENTS']
    df_drop_dup = df_total.drop_duplicates(group_params)
    df_sort = df_drop_dup.sort_values(by=group_params, ascending=True).reset_index()
    
    
    ## groupby 로 중복 count
    dup_count = df_drop_dup.groupby(by=group_params, as_index=False).count()                                          
    
    bsIndexTrace = []
    
    for subidx, cnt in zip(df_sort['SUBMODEINDEX'], dup_count['BEAMSTYLEINDEX']):
        if subidx == 0 and cnt >= 2:
            bsIndexTrace.append(15)
        elif subidx == 1 and cnt >= 2:
            bsIndexTrace.append(20)
        elif subidx == 5 and cnt >= 2:
            bsIndexTrace.append(10)
        else:
            bsIndexTrace.append(0)
    
    df_sort['bsIndexTrace'] = bsIndexTrace
    
    df_sort.to_csv('check_20230111.csv')