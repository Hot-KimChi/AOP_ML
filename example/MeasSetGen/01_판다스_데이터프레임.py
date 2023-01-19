import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from tkinter import filedialog

class MeasSetgen(object):
    
    def __init__(self) -> None:
        
        ### 데이터 파일 읽어오기.
        self.data = filedialog.askopenfilename(initialdir='.txt')
        self.data = pd.read_csv(self.data, sep='\t', encoding='cp949')
        
        ## columns name to 대문자.
        self.data.columns = [x.upper() for x in self.data.columns]
        
        list_param = ['PROBENAME', 'MODE', 'SUBMODEINDEX', 'BEAMSTYLEINDEX', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE', 'TXFOCUSLOCCM', 'NUMTXELEMENTS',
                    'PROBENUMTXCYCLES', 'ISTXCHANNELMODULATIONEN', 'ISPRESETCPAEN', 'CPADELAYOFFSETCLK', 'TXPULSERLE', 'TXPGWAVEFORMLUT', 'ELEVAPERINDEX',
                    'SYSTEMPULSERSEL', 'VTXINDEX']
        
        self.df_selected = self.data.loc[:, list_param]
        
        
    def fn_merge_df(self):
        
        df = self.df_selected
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
        
        
        ## groupby 로 중복 count / df_total에 count해서 집어넣기
        group_params =['ISTXCHANNELMODULATIONEN', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE', 'PROBENUMTXCYCLES', 'TXPULSERLE', 'ELEVAPERINDEX', 'TXFOCUSLOCCM', 'NUMTXELEMENTS']
        dup_count = df_total.groupby(by=group_params, as_index=False).count()    
        df_total['Count'] = dup_count['BEAMSTYLEINDEX']
        
        
        ## 중복된 parameter가 있을 경우, 제거하기.
        df_drop_dup = df_total.drop_duplicates(group_params)
        
        
        ## group param에서 SUBMODEINDEX 추가하여 정렬 준비 및 정렬하기
        sort_params = ['SUBMODEINDEX'] + group_params
        df_sort = df_drop_dup.sort_values(by=sort_params, ascending=True).reset_index()
         
        df = df_sort
        
        return df
        
        
    def fn_bsIdx(self, df):
        
        bsIndexTrace = []
        for subidx, cnt in zip(df['SUBMODEINDEX'], df['Count']):
            if subidx == 0 and cnt >= 2:
                bsIndexTrace.append(15)
            elif subidx == 1 and cnt >= 2:
                bsIndexTrace.append(20)
            elif subidx == 5 and cnt >= 2:
                bsIndexTrace.append(10)
            else:
                bsIndexTrace.append(0)
        
        df['bsIndexTrace'] = bsIndexTrace
        
        return df       
        
        
    def fn_freqidx2Hz(idx):
        try:
            frequencyTable = [1000000, 1111100, 1250000, 1333300, 1428600, 1538500, 1666700, 1818200, 2000000, 2222200,
                              2500000, 2666700, 2857100, 3076900, 3333300, 3636400, 3809500, 4000000, 4210500, 4444400,
                              4705900, 5000000, 5333300, 5714300, 6153800, 6666700, 7272700, 8000000, 8888900, 10000000,
                              11428600, 13333333, 16000000, 20000000, 26666667, 11428600, 11428600, 11428600, 11428600, 11428600,
                              11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600] 
            FreqIndex = idx
            freqHz = frequencyTable[FreqIndex]

            return freqHz

        except:
            print("Error: fn_freqidx2Hz")
                
        
    ## FrequencyIndex to FrequencyHz
    n = 0
    FrequencyHz = []
    for i in df_sort['SYSTXFREQINDEX'].values:
        FrequencyHz.insert(n, func_freqidx2Hz(i))
        n += 1
    df_sort['TxFrequencyHz'] = FrequencyHz



if __name__ == '__main__':
    cl_measset = MeasSetgen()
    df = cl_measset.fn_merge_df()

    df.to_csv('./example/MeasSetGen/csv_files/check_20230113.csv')