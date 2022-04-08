import tkinter as tk
from tkinter import ttk

def update(updated_entry, entry):
    ''' Combobox change Callback. '''
    entry.delete('1.0', tk.END)
    entry.insert(tk.END, updated_entry)

def gui(root):
    root.geometry('300x150')
    root.config(background='snow3')

    for row in range(2):
        text = tk.Text(root, height=1, width=10)  # Widget to be updated.
        text.grid(row=row, column=2)

        def check_okay(new_value, text=text):
            update(new_value, text)
            return True  # Note: accepts anything.

        combobox = ttk.Combobox(root, value=('test', 'test1', 'test2'),
                                validate='focusout',
                                validatecommand=(root.register(check_okay), '%P'))
        combobox.grid(row=row, column=1)

        combobox.bind('<Return>', lambda event, entry=combobox, text=text:
                                    update(entry.get(), entry=text))
        combobox.bind('<<ComboboxSelected>>', lambda event, entry=combobox, text=text:
                                                update(entry.get(), entry=text))

if __name__ == '__main__':
    root = tk.Tk()
    gui(root)
    tk.mainloop()