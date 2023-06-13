import tkinter as tk

from pkg_LogIn.login import LogIn
from pkg_TopMenu.top_menu import TopMenu


if __name__ == '__main__':
    login_window = tk.Tk()
    app_login = LogIn(login_window)

    login_window.mainloop()

