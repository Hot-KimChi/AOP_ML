
#
# -- Rev
# 3.0
#
# SELECT * FROM
# (
#     SELECT TOP (100)
# PERCENT
# dbo.Tx_summary.Num, dbo.Tx_summary.ProbeName, dbo.Tx_summary.Software_version, dbo.Tx_summary.Exam, dbo.Tx_summary.CurrentState, dbo.Tx_summary.BeamStyleIndex,
# dbo.Tx_summary.TxFrequency, dbo.Tx_summary.ElevAperIndex, dbo.Tx_summary.NumTxCycles, dbo.WCS.NumTxCycles
# AS
# WCS_Cycle, dbo.Tx_summary.TxpgWaveformStyle,
# dbo.Tx_summary.TxChannelModulationEn, dbo.Tx_summary.Compounding, dbo.SSR_table.WCSId, dbo.SSR_table.SSRId, dbo.SSR_table.reportTerm_1, dbo.SSR_table.XP_Value_1,
# dbo.SSR_table.reportValue_1, dbo.SSR_table.Difference_1, dbo.SSR_table.Ambient_Temp_1, dbo.SSR_table.reportTerm_2, dbo.SSR_table.XP_Value_2, dbo.SSR_table.reportValue_2,
# dbo.SSR_table.Difference_2, ROW_NUMBER()
# over(partition
# by
# num
# order
# by
# reportvalue_1
# desc) as RankNo, dbo.meas_res_summary.isDataUsable
#
# FROM
# dbo.Tx_summary
#
# LEFT
# OUTER
# JOIN
# dbo.WCS
# ON
# dbo.Tx_summary.ProbeID = dbo.WCS.probeId
# AND
# dbo.Tx_summary.BeamStyleIndex = dbo.WCS.Mode
# AND
# dbo.Tx_summary.TxFreqIndex = dbo.WCS.TxFrequencyIndex
# AND
# dbo.Tx_summary.ElevAperIndex = dbo.WCS.ElevAperIndex
# AND
# dbo.Tx_summary.TxpgWaveformStyle = dbo.WCS.WaveformStyle
# AND
# dbo.Tx_summary.TxChannelModulationEn = dbo.WCS.ChModulationEn
# AND
# dbo.Tx_summary.CurrentState = dbo.WCS.CurrentState
# LEFT
# OUTER
# JOIN
# dbo.meas_res_summary
# ON
# dbo.WCS.wcsID = dbo.meas_res_summary.VerifyID
# LEFT
# OUTER
# JOIN
# dbo.SSR_table
# ON
# dbo.WCS.wcsID = dbo.SSR_table.WCSId
# AND
# dbo.SSR_table.measSSId
# IN(1361, 1366, 1370, 1388, 1389, 1396)
#
# - - MI는
# 위에
# reportvalue_1로
# 수정 // Ispta
# .3
# 는
# 위를
# reportvalue_2로
# 수정.
# - -where
# reportTerm_1 = 'MI' or reportTerm_1
# IS
# NULL
# - -where
# reportTerm_2 = 'Ispta.3'
#                - -where
# reportTerm_1 = 'MI' or reportTerm_1
# IS
# NULL
# where
# reportTerm_1 = 'Temp' or reportTerm_1
# IS
# NULL
# ) T
# where
# RankNo = 1 and ProbeName = 'P8'
# order
# by
# num
#
#
#
#
#
#
#
#
#
#
# select * from
# (
#     SELECT  TOP (100) PERCENT dbo.Tx_summary.Num, dbo.Tx_summary.ProbeName, dbo.Tx_summary.Software_version, dbo.Tx_summary.Exam, dbo.Tx_summary.CurrentState ,dbo.Tx_summary.Dual_Mode, dbo.Tx_summary.BeamStyleIndex,
# dbo.Tx_summary.TxFrequency, dbo.Tx_summary.ElevAperIndex, dbo.Tx_summary.NumTxCycles, dbo.WCS.NumTxCycles AS WCS_Cycle, dbo.Tx_summary.TxpgWaveformStyle,
# dbo.Tx_summary.TxChannelModulationEn, dbo.Tx_summary.IsCPAEn, dbo.Tx_summary.RLE, dbo.SSR_table.WCSId, dbo.SSR_table.SSRId, dbo.SSR_table.reportTerm_1, dbo.SSR_table.XP_Value_1,
# dbo.SSR_table.reportValue_1, dbo.SSR_table.Difference_1, dbo.SSR_table.Ambient_Temp_1, dbo.SSR_table.reportTerm_2, dbo.SSR_table.XP_Value_2, dbo.SSR_table.reportValue_2,
# dbo.SSR_table.Difference_2, ROW_NUMBER() over (partition by num order by reportvalue_1 desc) as RankNo, dbo.meas_res_summary.isDataUsable
# FROM     dbo.Tx_summary
# LEFT OUTER JOIN dbo.WCS
# ON dbo.Tx_summary.ProbeID = dbo.WCS.probeId AND dbo.Tx_summary.BeamStyleIndex = dbo.WCS.Mode AND dbo.Tx_summary.TxFreqIndex = dbo.WCS.TxFrequencyIndex AND
# dbo.Tx_summary.ElevAperIndex = dbo.WCS.ElevAperIndex AND dbo.Tx_summary.TxpgWaveformStyle = dbo.WCS.WaveformStyle AND
# dbo.Tx_summary.TxChannelModulationEn = dbo.WCS.ChModulationEn AND dbo.Tx_summary.CurrentState = dbo.WCS.CurrentState AND dbo.Tx_summary.Dual_Mode = dbo.WCS.InterpolateFactor AND
# dbo.Tx_summary.IsCPAEn = dbo.WCS.IsCPAEn AND dbo.Tx_summary.RLE = dbo.WCS.TxPulseRleA --AND
# dbo.Tx_summary.NumTxCycles = dbo.WCS.NumTxCycles
# LEFT
# OUTER
# JOIN
# dbo.meas_res_summary
# ON
# dbo.WCS.wcsID = dbo.meas_res_summary.VerifyID
# LEFT
# OUTER
# JOIN
# dbo.SSR_table
# ON
# dbo.SSR_table.probeName
# NOT
# LIKE
# '%notuse%'
# AND
# dbo.WCS.wcsID = dbo.SSR_table.WCSId
# AND
# dbo.SSR_table.measSSId
# IN(1077)
#
# - -where
# reportTerm_1 = 'MI' or reportTerm_1
# IS
# NULL
# - -where
# reportTerm_2 = 'Ispta.3'
#                - -where
# reportTerm_1 = 'MI' or reportTerm_1
# IS
# NULL - -isDataUsable = 'yes'
# AND
# where
# reportTerm_1 = 'Temp' or reportTerm_1
# IS
# NULL - -isDataUsable = 'yes'
# AND
# ) T
# where
# RankNo = 1 and ProbeName = 'P4-2'
# order
# by
# num