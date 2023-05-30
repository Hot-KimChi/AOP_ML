class ParamGen:
    def __int__(self, data):
        self.initialize()

        ## list_param, 즉 선택한 parameter만 데이터프레임 생성.


        global selected_probeId
        selected_probeId = str(list_probeIds[self.combo_probename.current()])[1:-1]
        selected_probename = str(list_probenames[self.combo_probename.current()])

        # # Entry boxes
        # self.box_DumpSW = Entry(frame2, justify='center')
        # self.box_DumpSW.grid(row=1, column=0)
        #
        # self.box_MaxVolt = Entry(frame2, justify='center')
        # self.box_MaxVolt.grid(row=3, column=0)
        #
        # self.box_CeilVolt = Entry(frame2, justify='center')
        # self.box_CeilVolt.grid(row=3, column=1)
        #
        # self.box_TotalVoltpt = Entry(frame2, justify='center')
        # self.box_TotalVoltpt.grid(row=3, column=2)
        #
        # self.box_NumMeasVolt = Entry(frame2, justify='center')
        # self.box_NumMeasVolt.grid(row=3, column=3)


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


    ## find freq index
    def fn_findOrgIdx(self):

        orgindex = []

        for mode, subidx in zip(self.df['MODE'], self.df['SUBMODEINDEX']):
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


    ## bsIndexTrace algorithm
    def fn_bsIdx(self):

        bsIndexTrace = []

        for orgidx, cnt in zip(self.df['OrgBeamstyleIdx'], self.df['Count']):
            if orgidx == 0 and cnt >= 2:
                bsIndexTrace.append(15)
            elif orgidx == 1 and cnt >= 2:
                bsIndexTrace.append(20)
            elif orgidx == 5 and cnt >= 2:
                bsIndexTrace.append(10)
            else:
                bsIndexTrace.append(0)

        self.df['bsIndexTrace'] = bsIndexTrace

    ## FrequencyIndex to FrequencyHz
    def fn_freqidx2Hz(self):
        try:
            frequencyTable = [1000000, 1111100, 1250000, 1333300, 1428600, 1538500, 1666700, 1818200, 2000000, 2222200,
                              2500000, 2666700, 2857100, 3076900, 3333300, 3636400, 3809500, 4000000, 4210500, 4444400,
                              4705900, 5000000, 5333300, 5714300, 6153800, 6666700, 7272700, 8000000, 8888900, 10000000,
                              11428600, 13333333, 16000000, 20000000, 26666667, 11428600, 11428600, 11428600, 11428600,
                              11428600,
                              11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600, 11428600]

            FrequencyHz = []
            for i in self.df['SYSTXFREQINDEX'].values:
                FrequencyHz.append(frequencyTable[i])

            self.df['TxFrequencyHz'] = FrequencyHz

        except:
            print("Error: fn_freqidx2Hz")

    # n = 0
    # FrequencyHz = []
    # for i in df_sort['SYSTXFREQINDEX'].values:
    #     FrequencyHz.insert(n, func_freqidx2Hz(i))
    #     n += 1
    # df_sort['TxFrequencyHz'] = FrequencyHz

    ## Calc_cycle for RLE code
    def fn_cnt_cycle(self):

        list_cycle = []
        for i in range(len(self.df['TXPGWAVEFORMSTYLE'])):
            if self.df['TXPGWAVEFORMSTYLE'][i] == 0:
                rle = self.df['TXPULSERLE'].str.split(":")[i]
                list_flt = list(map(float, rle))
                ## 아래 code도 가능.
                ## floatList = [float(x) for x in list_option]
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
                cycle = self.df['PROBENUMTXCYCLES'][i]
                list_cycle.append(cycle)

        self.df['ProbeNumTxCycles'] = list_cycle

    ## function: calc_profTxVoltage 구현
    def fn_calc_profvolt(self):
        try:
            profTxVoltageVolt = []
            for str_maxV, str_ceilV, str_totalpt in zip(self.df['maxTxVoltageVolt'], self.df['ceilTxVoltageVolt'],
                                                        self.df['totalVoltagePt']):
                idx = 2
                ## tkinter에서 넘어오는 데이터 string.
                maxV = float(str_maxV)
                ceilV = float(str_ceilV)
                totalpt = int(str_totalpt)

                profTxVoltageVolt.append(round((min(maxV, ceilV)) ** ((totalpt - 1 - idx) / (totalpt - 1)), 2))

            self.df['profTxVoltageVolt'] = profTxVoltageVolt

        except:
            print('error: func_profvolt')

    ## function: calc zMeasNum 구현
    def fn_zMeasNum(self):
        try:
            zStartDistCm = 0.5
            zMeasNum = []

            for focus in self.df['TXFOCUSLOCCM']:
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