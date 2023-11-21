import tkinter as tk

class MyButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        # 기존 동작 오버라이드
        super().__init__(master, command=self.button_clicked, **kwargs)
        # 새로운 레이아웃 설정
        self.pack(side=tk.LEFT, padx=10)

    def button_clicked(self):
        print("Button Clicked in MyButton")

class AnotherButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        # 새로운 동작 정의
        super().__init__(master, command=self.custom_button_clicked, **kwargs)
        # 기존 레이아웃 설정
        self.pack(side=tk.RIGHT, padx=10)

    def custom_button_clicked(self):
        print("Custom Button Clicked")

    def button_clicked(self):
        # 해당 기능 사용하지 않음 (비어 있는 메서드)
        pass

# 사용 예제
root = tk.Tk()

# 기존 동작 및 레이아웃을 오버라이드한 MyButton
my_button = MyButton(root, text="My Button")
my_button.pack()

# 특정 기능 및 레이아웃을 사용하지 않는 AnotherButton
another_button = AnotherButton(root, text="Another Button")
another_button.pack()

root.mainloop()
