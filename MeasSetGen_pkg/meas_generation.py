import tkinter
from tkinter import *
from tkinter import ttk
from MeasSetGen_pkg.data_inout import DataInOut
import MeasSetGen_pkg.data_inout

# from MeasSetGen_pkg import param_select
# from MeasSetGen_pkg import merge_df
# from MeasSetGen_pkg import param_gen


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

        btn_load = Button(frame1, width=15, height=2, text='Select & Load', command=DataInOut.loadfile)
        btn_load.place(x=200, y=5)

        btn_insert = Button(frame1, width=15, height=2, text='To MS-SQL', command=self.fn_dataout)
        btn_insert.place(x=350, y=5)


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