import os

from tkinter import *
import tkinter as tk
from tkinter import ttk
import configparser
import warnings

warnings.filterwarnings("ignore")

from pkg_TopMenu.top_menu import TopMenu

class LogIn:
    """
    1) 초기 데이터베이스 접속을 위한 Log-in windows
    2) LogIn 이 후에 Top_menu.py 호출(wrapper_function 참고)
    """

    def __init__(self, login_window):
        self.window = login_window
        self.window.title("DB 선택")
        self.window.geometry("280x150")
        self.window.resizable(False, False)

        label = Label(self.window, text="데이터베이스를 선택하세요")
        label.place(x=10, y=10)

        self.combo_login = ttk.Combobox(self.window)
        self.combo_login.place(x=10, y=30)

        btn_login = Button(self.window, width=10, height=2, text="Login", command=self._get_sequence)
        btn_login.place(x=180, y=10)

        self.server_address = None
        self.ID = None
        self.password = None
        self.database = None

        self.load_config()


    def load_config(self):
        config_path = os.path.join("pkg_login", "../AOP_config.cfg")
        config = configparser.ConfigParser()
        config.read(config_path)

        self.server_address = config["server address"]["address"]
        self.ID = config["username"]["ID"]
        self.password = config["password"]["PW"]

        databases = config["database"]["name"]
        self.list_database = databases.split(',')

        self.combo_login["values"] = self.list_database
        self.combo_login.current(0)

        return config

    def print_login_info(self):
        print("-------------------------")
        print("Server Address:", self.server_address)
        print("ID:", self.ID)
        print("Password:", self.password)
        print("Database:", self.database)
        print("-------------------------")


    def get_login_info(self):
        self.database = self.combo_login.get()
        self.print_login_info()
        return self.server_address, self.ID, self.password, self.database


    def _get_sequence(self):
        self.get_login_info()
        TopMenu(self.server_address, self.ID, self.password, self.database)


if __name__ == '__main__':
    login_window = tk.Tk()
    app_login = LogIn(login_window)

    login_window.mainloop()
