import tkinter as tk
from tkinter import *
from tkinter import ttk

from pkg_MeasSetGen.data_inout import loadfile
from pkg_MeasSetGen.param_update import ParamUpdate


# from pkg_MeasSetGen import param_select
# from pkg_MeasSetGen import merge_df
# from pkg_MeasSetGen import param_gen


class MeasSetGen:

    def __init__(self, database, list_probe):

        self.database = database
        self.list_probe = list_probe

        self.window = tk.Toplevel()
        self.window.title(f"{self.database}" + ' / MeasSet_generation')
        self.window.geometry("600x200")
        self.window.resizable(False, False)

        frame = Frame(self.window, relief="solid", bd=2)
        frame.pack(side="top", fill="both", expand=True)

        label_probename = Label(frame, text='Probe Name')
        label_probename.place(x=5, y=5)
        self.combo_probe = ttk.Combobox(frame, value=self.list_probe, height=0, state='readonly')
        self.combo_probe.place(x=5, y=25)

        btn_load = Button(frame, width=15, height=2, text='Select & Load', command=self._get_sequence)
        btn_load.place(x=200, y=5)

        btn_insert = Button(frame, width=15, height=2, text='To MS-SQL', command=loadfile)
        btn_insert.place(x=350, y=5)


    def _get_sequence(self):
        self.probe = self.combo_probe.get().replace(" ", "")
        idx = self.probe.find("|")
        if idx >= 0:
            probename = self.probe[:idx]
            probeid = self.probe[idx+1:]

        print(probename)
        print(probeid)

        raw_data = loadfile()

        param_update = ParamUpdate(raw_data)                        ## 클래스 인스턴스 생성
        selected_df = param_update.param_merge()                    ## 메서드 호출 및 반환된 값 저장.



if __name__ == '__main__':
    gen_window = tk.Tk()
    app_gen = MeasSetGen(gen_window)

    gen_window.mainloop()
