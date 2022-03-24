import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


from tkinter import filedialog
filename = filedialog.askopenfilename(initialdir='.txt')
df_UEdata = pd.read_csv(filename, sep='\t', encoding='cp949')
df_first = df_UEdata.iloc[:, [4, 5, 6, 7, 8, 9, 10, 11, 12, 13]]                                        ## BeamStyle, TxFrequncyIndex, WF, Focus, Element, cycle, Chmodul, IsCPA, CPAclk, RLE

df_B_mode = df_first.loc[(df_first['BeamStyleIndex'] == 0) | (df_first['BeamStyleIndex'] == 1)]         # df_sort_B = df_B_mode.sort_values(by=[df_B_mode.columns[0], df_B_mode.columns[1], df_B_mode.columns[2], df_B_mode.columns[5], df_B_mode.columns[3]], ascending=True)
# B_num = df_sort_B['TxFocusLocCm'].nunique()
df_M_mode = df_first.loc[(df_first['BeamStyleIndex'] == 15) | (df_first['BeamStyleIndex'] == 20)]       # df_sort_M = df_M_mode.sort_values(by=[df_M_mode.columns[0], df_M_mode.columns[1], df_M_mode.columns[2], df_M_mode.columns[5], df_M_mode.columns[3]], ascending=True)

df_C_mode = df_first.loc[df_first['BeamStyleIndex'] == 5]
df_D_mode = df_first.loc[df_first['BeamStyleIndex'] == 10]

##------------------
##------------------

df_B_mode_update = df_B_mode.copy()                                                                                     # SettingWithCopyWarning 해결 / 복사본만 수정할 것인지 혹은 원본도 수정할 것인지 알 수 없어 경고
df_B_mode_update['bsIndexTrace'] = np.where(df_B_mode_update['BeamStyleIndex'] == 0, '15', '20')
df_C_mode_update, df_D_mode_update = df_C_mode.copy(), df_D_mode.copy()
df_C_mode_update['bsIndexTrace'] = 1
# df_D_mode_update = df_D_mode.copy()
df_D_mode_update['bsIndexTrace'] = 2

print(df_B_mode_update)
print(df_C_mode_update, df_D_mode_update)
