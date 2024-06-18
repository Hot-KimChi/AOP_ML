import numpy as np
from datetime import datetime


class ParamGen:
    def __init__(self, data, probeid, probename):

        today = datetime.today()

        self.df = data
        self.probeid = probeid
        self.probename = probename

        self.df['probeId'] = self.probeid
        self.df['probeName'] = self.probename

        self.df['maxTxVoltageVolt'] = 90
        self.df['ceilTxVoltageVolt'] = 90
        self.df['totalVoltagePt'] = 20
        self.df['zStartDistCm'] = 0.5
        self.df['DTxFreqIndex'] = 0
        self.df['dumpSwVersion'] = today.strftime('%Y-%m-%d')
        self.df['measSetComments'] = f'Beamstyle_{self.probename}_Intensity'

        
    def gen_sequence(self):
        
        self.numvoltpt()
        self.findOrgIdx()
        self.bsIdx()
        self.freqidx2Hz()
        self.cnt_cycle()
        self.calc_profvolt()
        self.zMeasNum()
        
        return self.df


    def numvoltpt(self):
        ## Contrast mode 일 경우, numMeasVoltage 10 그 외에는 8
        ##  = self.df['Mode'].apply(lambda mode: 10 if mode == 'Contrast' else 8)
        self.df['numMeasVoltage'] = 10
        
        return self.df


    ## find freq index
    def findOrgIdx(self):

        orgindex = []

        for mode, subidx in zip(self.df['Mode'], self.df['SubModeIndex']):
            if mode == 'B' and subidx == 0:
                orgindex.append(0)
            elif mode == 'B' and subidx == 1:
                orgindex.append(1)
            elif mode == 'Cb' and subidx == 0:
                orgindex.append(5)
            elif mode == 'D' and subidx == 0:
                orgindex.append(10)
            elif mode == 'M' and subidx == 0:
                orgindex.append(15)
            elif mode == 'M' and subidx == 1:
                orgindex.append(20)

        self.df['OrgBeamstyleIdx'] = orgindex

        return self.df


    ## bsIndexTrace algorithm
    def bsIdx(self):

        bsIndexTrace = []

        for orgidx, duplicate in zip(self.df['OrgBeamstyleIdx'], self.df['isDuplicate']):
            if orgidx == 0 and duplicate == 1:
                bsIndexTrace.append(15)
            elif orgidx == 1 and duplicate == 1:
                bsIndexTrace.append(20)
            elif orgidx == 5 and duplicate == 1:
                bsIndexTrace.append(10)
            else:
                bsIndexTrace.append(0)

        self.df['bsIndexTrace'] = bsIndexTrace

        return self.df


    ## FrequencyIndex to FrequencyHz
    def freqidx2Hz(self):
        try:
            frequencyTable = [1000000, 1111100, 1250000, 1333300, 1428600, 1538500, 1666700, 1818200, 2000000, 2222200,
                              2500000, 2666700, 2857100, 3076900, 3333300, 3636400, 3809500, 4000000, 4210500, 4444400,
                              4705900, 5000000, 5333300, 5714300, 6153800, 6666700, 7272700, 8000000, 8888900, 10000000,
                              11428600, 13333333, 16000000, 20000000, 26666667, 11428600, 11428600, 11428600, 11428600,
                              11428600,
                              11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600]

            frequencyHz = []
            for i in self.df['SysTxFreqIndex'].values:
                frequencyHz.append(frequencyTable[i])

            self.df['TxFrequencyHz'] = frequencyHz

        except:
            print("Error: fn_freqidx2Hz")

        return self.df


    ## Calc_cycle for RLE code
    def cnt_cycle(self):

        list_cycle = []
        for waveform, rle, cycle in zip(self.df['TxpgWaveformStyle'], self.df['TxPulseRle'], self.df['ProbeNumTxCycles']):
            if waveform == 0:
                raw_rle = str(rle).split(":")
                list_flt = list(map(float, raw_rle))
                abs_value = np.abs(list_flt)
                
                calc = []
                for value in abs_value:
                    if 1 < value:
                        calc.append(round(value - 1, 4))
                    else:
                        calc.append(value)
                cycle = round(sum(calc), 2)
                list_cycle.append(cycle)

            else:
                list_cycle.append(cycle)
        
        self.df['ProbeNumTxCycles'] = list_cycle

        return self.df
       
        
        # list_cycle = []
        # for i in range(len(self.df['TxpgWaveformStyle'])):
        #     if self.df['TxpgWaveformStyle'][i] == 0:
        #         rle = self.df['TxPulseRle'].str.split(":")[i]
        #         list_flt = list(map(float, rle))
        #         ## 아래 code도 가능.
        #         ## floatList = [float(x) for x in list_option]
        #         abs_value = np.abs(list_flt)

        #         calc = []
        #         for value in abs_value:
        #             if 1 < value:
        #                 calc.append(round(value - 1, 4))
        #             else:
        #                 calc.append(value)
        #         cycle = round(sum(calc), 2)
        #         list_cycle.append(cycle)

        #     else:
        #         cycle = self.df['ProbeNumTxCycles'][i]
        #         list_cycle.append(cycle)

        # self.df['ProbeNumTxCycles'] = list_cycle

        # return self.df


    ## function: calc_profTxVoltage 구현
    def calc_profvolt(self):
        try:
            profTxVoltageVolt = []
            for str_maxV, str_ceilV, str_totalpt in zip(self.df['maxTxVoltageVolt'], self.df['ceilTxVoltageVolt'],
                                                        self.df['totalVoltagePt']):
                idx = 2
                maxV = float(str_maxV)
                ceilV = float(str_ceilV)
                totalpt = int(str_totalpt)

                profTxVoltageVolt.append(round((min(maxV, ceilV)) ** ((totalpt - 1 - idx) / (totalpt - 1)), 2))

            self.df['profTxVoltageVolt'] = profTxVoltageVolt

        except:
            print('error: func_profvolt')

        return self.df


    ## function: calc zMeasNum 구현
    def zMeasNum(self):
        try:
            zStartDistCm = 0.5
            zMeasNum = []

            for focus in self.df['TxFocusLocCm']:
                if (focus <= 3):
                    zMeasNum.append((5 - zStartDistCm) * 10)
                elif (focus <= 6):
                    zMeasNum.append((8 - zStartDistCm) * 10)
                elif (focus <= 9):
                    zMeasNum.append((12 - zStartDistCm) * 10)
                else:
                    zMeasNum.append((14 - zStartDistCm) * 10)

            self.df['zMeasNum'] = zMeasNum

        except:
            print('error: func_zMeaNum')

        return self.df
