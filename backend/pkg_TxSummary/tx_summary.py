
class TxSumm(object):
    def __init__(self):
        super().__init__()
        self.initialize()


    def initialize(self):
        filename = filedialog.askopenfilename(initialdir='.txt')
        self.df_txsumm = pd.read_csv(filename, sep='\t', encoding='cp949')
        self.fn_tx_summ()


    def fn_tx_summ(self):
        ## mode, BeamStyle, TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE
        df_first = self.df_txsumm.iloc[:, [2, 4, 5, 6, 7, 8, 9, 10]]

        df = df_first.drop_duplicates()
        df_D_mode = df.loc[(df['BeamStyleIndex'] == 10) & (df['ProbeNumTxCycles'] == 4)]
        df_others_mode = df.loc[df['BeamStyleIndex'] != 10]

        df_D_mode = df_D_mode.drop_duplicates \
            (['Mode', 'BeamStyleIndex', 'TxFreqIndex', 'TxFrequency', 'ProbeNumElevAper', 'TxpgWaveformStyle', 'TxChannelModulationEn'])
        df_others_mode = df_others_mode.drop_duplicates()
        df_final_mode = pd.concat([df_others_mode, df_D_mode])                                                          ## 2개 데이터프레임 합치기
        df_final_mode = df_final_mode.reset_index(drop=True)                                                            ## 데이터프레임 index reset
        df_final_mode = df_final_mode.sort_values(
            by=[df_final_mode.columns[0], df_final_mode.columns[1], df_final_mode.columns[2], df_final_mode.columns[4],
                df_final_mode.columns[6]], ascending=True)

        ShowTable.fn_show_table('Tx_summary', df_final_mode)
