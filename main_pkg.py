import tkinter
from tkinter import *
from tkinter import ttk

import configparser
import warnings
warnings.filterwarnings("ignore")

from pkg_TopMain.top_main import TopMain

class LogIn(tkinter.Tk):

    """
    초기 데이터베이스 접속을 위한 Log-in windows
    """

    def __init__(self):
        super().__init__()

        config = configparser.ConfigParser()
        config.read('AOP_config.cfg')

        global server_address, ID, password
        server_address = config["server address"]["address"]
        databases = config["database"]["name"]
        ID = config["username"]["ID"]
        password = config["password"]["PW"]

        self.list_database = databases.split(',')

        self.log_in()


    def log_in(self):

        ## Start tk 만들기.
        self.title("DB 선택")
        self.geometry("280x150")
        self.resizable(False, False)

        label1 = Label(self, text='데이터베이스를 선택하세요')
        label1.place(x=10, y=10)


        self.combo_login = ttk.Combobox(self, value=self.list_database)         # combo-Box 만들어서 데이터베이스만들기
        self.combo_login.current(0)                                             # combo-Box 처음 선택되는 위치가 공란이 아니라 처음 데이터베이스 선택 옵션
        self.combo_login.place(x=10, y=30)                                      # combo-Box 의 위치
        # login_combo.pack(pady=20)

        btn_login = Button(self, width=10, height=2, text='Login', command=self.select_DB)
        btn_login.place(x=180, y=10)

        self.mainloop()


    def select_DB(self):
        global database
        database = self.combo_login.get()
        TopMain()


if __name__ == '__main__':
    LogIn()
