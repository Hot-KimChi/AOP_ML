import joblib
import pandas as pd

from pkg_SQL.database import SQL


class PredictML:
    """
    Predict AOP value
    1) intensity case: peak of scanning-mode / using set-up range of measurement by ML
    2) temperature case: find initial PRF(for target temperature)
    3) Power case: find to set-up PRF for preventing of transducer damage
    """

    def __init__(self, df, probe):

        self.df = df
        self.probe = probe


        ## take parameters for ML from measSet_gen file.
        self.est_params = self.df[['TxFrequencyHz', 'TxFocusLocCm', 'NumTxElements', 'TxpgWaveformStyle',
                                   'ProbeNumTxCycles', 'ElevAperIndex', 'IsTxChannelModulationEn']]

        ## load parameters from SQL database
        connect = SQL(command=4, selected_probeId=self.probe)
        est_geo = connect.sql_get()

        self.est_params[['probePitchCm']] = est_geo['probePitchCm']
        self.est_params[['probeRadiusCm']] = est_geo['probeRadiusCm']
        self.est_params[['probeElevAperCm0']] = est_geo['probeElevAperCm0']
        self.est_params[['probeElevFocusRangCm']] = est_geo['probeElevFocusRangCm']


    def intensity_zt(self):
        ## predict zt by Machine Learning model.

        loaded_model = joblib.load('Model/RandomForest_v1_python37.pkl')

        zt_est = loaded_model.predict(self.est_params)
        df_est = pd.DataFrame(zt_est, columns=['zt_est'])

        self.df['zt_est'] = round(df_est, 1)

        return self.df


    def temperature_PRF(self):
        pass

        return self.df