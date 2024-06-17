import tkinter as tk
from tkinter import ttk

from pkg_MeasSetGen.data_inout import loadfile
from pkg_MeasSetGen.data_inout import DataOut
from pkg_MeasSetGen.param_update import ParamUpdate
from pkg_MeasSetGen.param_gen import ParamGen
from pkg_MeasSetGen.predictML import PredictML


class MeasSetGen:
    """
    MeasSetGeneration 버튼이 눌렸을 경우, 해당 클래스가 실행.
    1) select & Load 버튼: _get_sequence 함수 실행
    2) To MS-SQL / To Excel / protocol check
    """

    def __init__(self, database, list_probe):

        self.database = database
        self.list_probe = list_probe

        self.window = tk.Toplevel()
        self.window.title(f"{self.database}" + " / MeasSet_generation")
        self.window.geometry("600x200")
        self.window.resizable(False, False)

        frame = tk.Frame(self.window, relief="solid", bd=2)
        frame.pack(side="top", fill="both", expand=True)

        label_probename = tk.Label(frame, text="Probe Name")
        label_probename.place(x=5, y=5)
        self.combo_probe = ttk.Combobox(
            frame, value=self.list_probe, height=0, state="readonly"
        )
        self.combo_probe.place(x=5, y=25)

        btn_load = tk.Button(
            frame, width=15, height=2, text="Select & Load", command=self._get_sequence
        )
        btn_load.place(x=200, y=5)

        btn_insert = tk.Button(
            frame, width=15, height=2, text="To MS-SQL", command=loadfile
        )
        btn_insert.place(x=350, y=5)

    def _get_sequence(self):

        ## probename / probeid 로 구분
        probe = self.combo_probe.get().replace(" ", "")
        idx = probe.find("|")
        if idx >= 0:
            probename = probe[:idx]
            probeid = probe[idx + 1 :]

        ## 파일 선택할 수 있는 algorithm / 중복 데이터 삭제 및 group_index
        raw_data = loadfile()
        param_update = ParamUpdate(raw_data)  ## 클래스 인스턴스 생성
        self.selected_df, self.group_params = (
            param_update.remove_duplicate()
        )  ## 메서드 호출 및 반환된 값 저장.

        ## 선택한 데이터를 기반으로 parameter 생성.
        self.gen_df = ParamGen(
            data=self.selected_df, probeid=probeid, probename=probename
        )

        ## predictML for intensity case
        ML = PredictML(self.gen_df.df, probeid)
        self.gen_df = ML.intensity_zt()

        ## 클래스 인스턴스를 데이터프레임으로 변환 / DataOut 클래스 이용하여 csv 파일로 추출.
        df = self.gen_df

        dataout = DataOut(
            case=0,
            database=self.database,
            probe=probe,
            df1=df,
            group_params=self.group_params,
        )
        dataout.make_dir()
        dataout.save_excel()


if __name__ == "__main__":
    gen_window = tk.Tk()
    app_gen = MeasSetGen(gen_window)

    gen_window.mainloop()
