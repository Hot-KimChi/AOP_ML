import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from tkinter import filedialog

if __name__ == '__main__':
    
    data = filedialog.askopenfilename(initialdir='.txt')
    data = pd.read_csv(data, sep='\t', encoding='cp949')
    
    ## columns name
    data.columns = [x.upper() for x in data.columns]
    
        
    # list_params = ['Mode', 'BeamStyleIndex', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn',
    #                'IsPresetCpaEn', 'CpaDelayOffsetClk', 'TxPulseRle', 'TxpgWaveformLut', 'SystemPulserSel', 'VTxIndex', 'elevAperIndex']
    
    selected_data = data.loc[:, list_params]
    
    ##############################
    ##### B & M mode process #####
    ## df_sort_B = df_B_mode.sort_values(by=[df_B_mode.columns[0], df_B_mode.columns[1], df_B_mode.columns[2], df_B_mode.columns[5], df_B_mode.columns[3]], ascending=True)
    ## B_num = df_sort_B['TxFocusLocCm'].nunique()
    
    df_B_mode = selected_data.loc[(selected_data['Mode'] == 'B')]
    df_M_mode = selected_data.loc[(selected_data['Mode'] == 'M')]
    df_C_mode = selected_data.loc[selected_data['Mode'] == 'Cb']
    df_D_mode = selected_data.loc[selected_data['Mode'] == 'D']
    df_CEUS_mode = selected_data.loc[selected_data['Mode'] == 'Contrast']
    
    ## 4개 모드 데이터프레임 합치기
    ## 합쳐진 데이터프레임 index reset
    df_total = pd.concat([df_B_mode, df_M_mode, df_C_mode, df_D_mode, df_CEUS_mode])                                            
    df_total = df_total.reset_index(drop=True)                                                                          
    
    ## 데이터 Null --> [0]으로 변환(데이터의 정렬, groupby null 값 문제 발생)
    df_total = df_total.fillna(0)
    
    df_total.to_csv('test_total.csv')