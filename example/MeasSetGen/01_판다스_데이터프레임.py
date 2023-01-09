import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from tkinter import filedialog

if __name__ == '__main__':
    data = filedialog.askopenfilename(initialdir='.txt')
    data = pd.read_csv(data, sep='\t', encoding='cp949')
        
    list_params = ['BeamStyleIndex', 'SysTxFreqIndex', 'TxpgWaveformStyle', 'TxFocusLocCm', 'NumTxElements', 'ProbeNumTxCycles', 'IsTxChannelModulationEn', 
             'IsPresetCpaEn', 'CpaDelayOffsetClk', 'TxPulseRle', 'TxpgWaveformLut', 'SystemPulserSel', 'VTxIndex', 'elevAperIndex']
    
    selected_data = data.loc[:, list_params]
    
    ########################
    ## B & M mode process ##
    # df_sort_B = df_B_mode.sort_values(by=[df_B_mode.columns[0], df_B_mode.columns[1], df_B_mode.columns[2], df_B_mode.columns[5], df_B_mode.columns[3]], ascending=True)
    # B_num = df_sort_B['TxFocusLocCm'].nunique()
    df_B_mode = selected_data.loc[(selected_data['BeamStyleIndex'] == 0) | (selected_data['BeamStyleIndex'] == 1)]
    df_M_mode = selected_data.loc[(selected_data['BeamStyleIndex'] == 15) | (selected_data['BeamStyleIndex'] == 20)]
    df_C_mode = selected_data.loc[selected_data['BeamStyleIndex'] == 5]
    df_D_mode = selected_data.loc[selected_data['BeamStyleIndex'] == 10]