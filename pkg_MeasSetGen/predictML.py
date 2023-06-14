

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