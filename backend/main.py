import tkinter as tk

from pkg_LogIn.login import LogIn


## Login을 기반으로 접속 후, Top_menu 실행
if __name__ == "__main__":
    login_window = tk.Tk()
    LogIn(login_window)

    login_window.mainloop()
