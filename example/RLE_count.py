import os
import tkinter
import pymssql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tkinter import *
from tkinter import ttk
from functools import partial
import configparser
import warnings
warnings.filterwarnings("ignore")

from tkinter import filedialog
import joblib

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.metrics import mean_absolute_error


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

data = pd.read_csv('RLE.csv')
# print(data)

def func_cnt_cycle():

    list_cycle = []
    for i in range(len(data['TxpgWaveformStyle'])):

        if data['TxpgWaveformStyle'][i] == 0:
            rle = data['TxPulseRle'].str.split(":").tolist()[i]
            flt = list(map(float, rle))
            abs = np.abs(flt)

            cal = []
            for value in abs:
                if 1 < value:
                    cal.append(round(value-1, 4))
                else:
                    cal.append(value)

            cycle = round(sum(cal), 2)
            print(cycle)
            list_cycle.append(cycle)

        else:
            cycle = data['ProbeNumTxCycles'][i]
            print(cycle)
            list_cycle.append(cycle)


    print(list_cycle)





if __name__ == '__main__':
    func_cnt_cycle()


