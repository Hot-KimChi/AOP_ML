class ParamSelect:
    """
    parameter selection Class
    """

    def __int__(self, df):
        self.df = df


    ## 대문자로 변경하여 param 선택.
    def select(self):
        ## columns name to 대문자.
        self.df.columns = [x.upper() for x in self.df.columns]

        list_param = ['PROBENAME', 'MODE', 'SUBMODEINDEX', 'BEAMSTYLEINDEX', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE',
                      'TXFOCUSLOCCM', 'NUMTXELEMENTS', 'PROBENUMTXCYCLES', 'ISTXCHANNELMODULATIONEN', 'ISPRESETCPAEN',
                      'CPADELAYOFFSETCLK', 'TXPULSERLE', 'TXPGWAVEFORMLUT', 'ELEVAPERINDEX', 'SYSTEMPULSERSEL',
                      'VTXINDEX']

        selected_df = self.df.loc[:, list_param]

        return selected_df