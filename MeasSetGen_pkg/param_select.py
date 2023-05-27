import pandas as pd


class ParamSelect:

    def __int__(self):
        self.initialize()


    ## 대문자로 변경하여 param 선택.
    def select(data):
        ## columns name to 대문자.
        data.columns = [x.upper() for x in data.columns]

        list_param = ['PROBENAME', 'MODE', 'SUBMODEINDEX', 'BEAMSTYLEINDEX', 'SYSTXFREQINDEX', 'TXPGWAVEFORMSTYLE', 'TXFOCUSLOCCM', 'NUMTXELEMENTS',
                      'PROBENUMTXCYCLES', 'ISTXCHANNELMODULATIONEN', 'ISPRESETCPAEN', 'CPADELAYOFFSETCLK', 'TXPULSERLE', 'TXPGWAVEFORMLUT', 'ELEVAPERINDEX',
                      'SYSTEMPULSERSEL', 'VTXINDEX']

        ## list_param, 즉 선택한 parameter만 데이터프레임 생성.
        df = data.loc[:, list_param]

        global selected_probeId
        selected_probeId = str(list_probeIds[self.combo_probename.current()])[1:-1]
        selected_probename = str(list_probenames[self.combo_probename.current()])


        self.df['probeId'] = selected_probeId
        self.df['probeName'] = str(list_probenames[self.combo_probename.current()])
        self.df['maxTxVoltageVolt'] = self.box_MaxVolt.get()
        self.df['ceilTxVoltageVolt'] = self.box_CeilVolt.get()
        self.df['totalVoltagePt'] = self.box_TotalVoltpt.get()
        self.df['numMeasVoltage'] = self.box_NumMeasVolt.get()
        self.df['zStartDistCm'] = 0.5
        self.df['DTxFreqIndex'] = 0
        self.df['dumpSwVersion'] = self.box_DumpSW.get()
        self.df['measSetComments'] = f'Beamstyle_{selected_probename}_Intensity'