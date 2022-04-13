from tkinter import *
from tkinter import ttk
from tkinter import messagebox

#콤보박스 선택 값 돌려주기
def change1(index, value, op):
    # print(brand_combo.get())
    # print(brand_combo.current())

    brand_index = brand_combo.current()
    label = ttk.Label(win, text=brand_index)
    label.grid(row = 0, column=1)


brand = ["서울", "대전", "대구", "부산", "광주", "울산"]

# window 띄우기
win = Tk ()
win.title("test")
win.geometry('400x200')
win.resizable(FALSE, FALSE)

# brand 콤보박스
str1 = StringVar()
str1.trace('w', change1)
brand_combo = ttk.Combobox(win, width=20, state='readonly', textvariable=str1, values=brand)
brand_combo.grid(row = 0, column=0)

win.mainloop()