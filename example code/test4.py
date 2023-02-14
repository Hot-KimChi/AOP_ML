import tkinter as tk
from tkinter import ttk

import pandas as pd


def update(updated_entry, entry):
    entry.delete('1.0', tk.END)
    entry.insert(tk.END, updated_entry)
def gui(root):
    root.geometry('300x150')
    root.config(background='snow3')
    for row in range(2):
        combobox= ttk.Combobox(root, value=('test', 'test1', 'test2'))
        combobox.grid(row=row, column=1)
        text= tk.Text(root, height=1, width=10)
        text.grid(row=row, column=2)
        def check_okay(new_value, text=text):
            update(new_value, text)
            return True  # Accepts anything.
        ok_command= root.register(check_okay)
        combobox.config(validate='focusout', validatecommand=(ok_command, '%P'))
        combobox.bind('<Return>', lambda event, entry=combobox, text=text:
                                    update(entry.get(), entry=text))
        combobox.bind('<<ComboboxSelected>>', lambda event, entry=combobox, text=text:
                                                update(entry.get(), entry=text))
if __name__== '__main__':
    root= tk.Tk()
    gui(root)
    tk.mainloop()