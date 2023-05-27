import tkinter
from tkinter import *
from tkinter import ttk
from MeasSetGen_pkg import data_inout
from MeasSetGen_pkg import param_select
from MeasSetGen_pkg import merge_df
from MeasSetGen_pkg import param_gen


class MeasSetGen:

    def __init__(self, database, list_probe):
        self.initialize()
        self.database = database
        self.list_probe = list_probe


    def initialize(self):
        window_gen = tkinter.Toplevel()
        window_gen.title(f"{self.database}" + ' / MeasSet_generation')
        window_gen.geometry("600x200")
        window_gen.resizable(False, False)

        frame1 = Frame(window_gen, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)

        label_probename = Label(frame1, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probename = ttk.Combobox(frame1, value=self.list_probe, height=0, state='readonly')
        self.combo_probename.place(x=5, y=25)

        btn_load = Button(frame1, width=15, height=2, text='Select & Load', command=self._fn_gen_sequence)
        btn_load.place(x=200, y=5)

        btn_insert = Button(frame1, width=15, height=2, text='To MS-SQL', command=self.fn_dataout)
        btn_insert.place(x=350, y=5)
        #
        # frame2 = Frame(window_gen, relief="solid", bd=2)
        # frame2.pack(side="bottom", fill="both", expand=True)
        #
        # # Labels
        # label_DumpSW = Label(frame2, text="[dumpSwVersion]")
        # label_DumpSW.grid(row=0, column=0)
        #
        # label_MaxVolt = Label(frame2, text="[maxTxVoltageVolt]")
        # label_MaxVolt.grid(row=2, column=0)
        #
        # label_CeilVolt = Label(frame2, text="[ceilTxVoltageVolt]")
        # label_CeilVolt.grid(row=2, column=1)
        #
        # label_TotalVoltpt = Label(frame2, text="[totalVoltagePt]")
        # label_TotalVoltpt.grid(row=2, column=2)
        #
        # label_NumMeasVolt = Label(frame2, text="[numMeasVoltage]")
        # label_NumMeasVolt.grid(row=2, column=3)
        #
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

        window_gen.mainloop()


    def _fn_gen_sequence(self):
        self.fn_loadfile()
        self.fn_select()
        self.fn_merge_df()
        self.fn_findOrgIdx()
        self.fn_bsIdx()
        self.fn_freqidx2Hz()
        self.fn_cnt_cycle()
        self.fn_calc_profvolt()
        self.fn_zMeasNum()
        self.fn_predictML()

        self.fn_dataout()




    def fn_predictML(self):
        ## predict by Machine Learning model.
        ## load modeling by pickle file.
        loaded_model = joblib.load('Model/RandomForest_v1_python37.pkl')

        ## take parameters for ML from measSet_gen file.
        est_params = self.df[
            ['TxFrequencyHz', 'TXFOCUSLOCCM', 'NUMTXELEMENTS', 'TXPGWAVEFORMSTYLE', 'ProbeNumTxCycles', 'ELEVAPERINDEX',
             'ISTXCHANNELMODULATIONEN']]
        connect = SQL(command=4)
        est_geo = connect.fn_sql_get()

        est_params[['probePitchCm']] = est_geo['probePitchCm']
        est_params[['probeRadiusCm']] = est_geo['probeRadiusCm']
        est_params[['probeElevAperCm0']] = est_geo['probeElevAperCm0']
        est_params[['probeElevFocusRangCm']] = est_geo['probeElevFocusRangCm']

        zt_est = loaded_model.predict(est_params)
        df_zt_est = pd.DataFrame(zt_est, columns=['zt_est'])

        self.df['zt_est'] = round(df_zt_est, 1)

