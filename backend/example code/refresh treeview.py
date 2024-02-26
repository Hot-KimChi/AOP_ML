import tkinter as tk
from tkinter import ttk


class View(tk.Frame):
    """A frame with an expose event"""
    shared_text = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Expose>', self.expose_event)

        self.local_text = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.local_text)
        self.entry.pack()
        self.entry.bind('<Return>', self.set_value)

    def set_value(self, event):
        """Called when enter key is pressed in entry widget"""
        View.shared_text = self.local_text.get()

    def expose_event(self, event):
        """Called when I become visible"""
        self.local_text.set(View.shared_text)


root = tk.Tk()
notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=tk.YES)
for i in range(5):
    notebook.add(View(notebook), text=str(i))
root.mainloop()