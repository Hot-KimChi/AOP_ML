import tkinter as tk
from tkinter import *

from pkg_Table.treeview_update import DataTable


class DetailTable:
    """
    detail table from selected parameter
    """

    def __init__(self, name_database, feature, data):

        self.database = name_database
        self.feature = feature
        self.data = data

        window_detail = tk.Toplevel()
        window_detail.title(f"{self.database}" + ' / Detail Table')
        window_detail.geometry("1600x700")
        # window_verify.resizable(False, False)

        self.frame1 = Frame(window_detail, relief="solid", bd=2)
        self.frame1.pack(side="top", fill="both", expand=True)

        # global btn_selection
        if self.feature == 0:  ## To SQL parsing
            btn_selection = Button(self.frame1, width=15, height=2, text='To SQL', command=self.test)

        elif self.feature == 1:  ## To excel for viewer
            btn_selection = Button(self.frame1, width=15, height=2, text='To Excel', command=self.test)

        btn_selection.place(x=550, y=5)


    def test(self):
        pass
