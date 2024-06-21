import tkinter as tk
from tkinter import ttk
import math

class ProbeInfo:
    def __init__(self):
        self.list_probe = []

    def load_probeinfo(self):
        ## 임시 데이터로 SQL 클래스 대체
        data = [
            ["New_C5-2v", "1001"],
            ["Old_B3-1s", "1002"],
            ["New_A2-4x", "1003"],
            ["Old_X5-7y", "1004"]
        ]
        
        list_probenames = [row[0] for row in data]
        list_probeIds = [row[1] for row in data]

        # Probelist를 probeName + probeId 생성
        for probename, probeid in zip(list_probenames, list_probeIds):
            formatted_probe = self.format_probe_string(str(probename), str(probeid))
            self.list_probe.append(formatted_probe)

        return self.list_probe

    def format_probe_string(self, probename, probeid, total_width=20):
        # 전체 문자열 길이 (probename + 공백 + '|' + 공백 + probeid)
        total_length = len(probename) + 1 + 1 + 4 + len(probeid)
        
        # '|'의 위치를 계산 (전체 길이의 중앙)
        pipe_position = total_width // 2
        
        # probeid를 기록할 위치 계산
        space_before_probeid = total_width - pipe_position - len(probeid)
        
        # probename 왼쪽 정렬, '|' 중앙, probeid 오른쪽 정렬
        formatted_string = f"{probename:<{pipe_position}}|{' ' * space_before_probeid}{probeid}"
        
        return formatted_string


def main():
    # Tkinter root 윈도우 생성
    root = tk.Tk()
    root.title("Combobox Example")

    # 고정 폭 글꼴 설정
    root.option_add('*TCombobox*Listbox*Font', 'Courier 10')
    root.option_add('*Font', 'Courier 10')

    # ProbeInfo 클래스 인스턴스 생성 및 데이터 로드
    probe_info = ProbeInfo()
    probe_list = probe_info.load_probeinfo()

    # Combobox 생성 및 데이터 추가
    combo = ttk.Combobox(root, values=probe_list)
    combo.pack(padx=10, pady=10)

    # 메인 루프 시작
    root.mainloop()

if __name__ == "__main__":
    main()
