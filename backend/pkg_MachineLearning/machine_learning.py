import os
import tkinter as tk
from tkinter import ttk
import joblib

from pkg_MachineLearning.preProcess_ML import preProcess

from sklearn.model_selection import cross_validate


class Machine_Learning:
    """
    머신러닝 클래스
    1) Randomforest
    2) Deep learning
    """

    def __init__(self, database):
        super().__init__()

        ## load config file
        self.database = database
        name_MLs = os.environ["MLs"]
        self.list_ML = name_MLs.split(",")

        window_ML = tk.Toplevel()
        window_ML.title(f"{database}" + " / Machine Learning")
        window_ML.geometry("420x200")
        window_ML.resizable(False, False)

        # 고정 폭 글꼴 설정
        window_ML.option_add("*Font", "Consolas 10")

        frame1 = tk.Frame(window_ML, relief="solid", bd=2)
        frame1.pack(side="top", fill="both", expand=True)

        label_ML = tk.Label(frame1, text="Machine Learning")
        label_ML.place(x=5, y=5)
        self.combo_ML = ttk.Combobox(
            frame1, value=self.list_ML, width=35, height=0, state="readonly"
        )
        self.combo_ML.place(x=5, y=25)

        btn_load = tk.Button(
            frame1,
            width=15,
            height=2,
            text="Select & Train",
            command=self._sequence_ML,
        )
        btn_load.place(x=280, y=5)

        window_ML.mainloop()

    def _sequence_ML(self):
        data, target = preProcess()
        self.fn_modelML()
        self.fn_ML_fit()
        self.fn_ML_save()
        self.fn_diff_check()

    def fn_ML_fit(self):
        ## DNN 인 경우, 아래와 같이 training
        if "DNN" in self.selected_ML:
            pass

        else:
            scores = cross_validate(
                self.model,
                self.train_input,
                self.train_target,
                return_train_score=True,
                n_jobs=-1,
            )
            print()
            print(scores)
            import numpy as np

            print(
                f"{self.selected_ML} - Train R^2:",
                np.round_(np.mean(scores["train_score"]), 3),
            )
            print(
                f"{self.selected_ML} - Train_validation R^2:",
                np.round_(np.mean(scores["test_score"]), 3),
            )

            self.model.fit(self.train_input, self.train_target)
            print(
                f"{self.selected_ML} - Test R^2:",
                np.round_(self.model.score(self.test_input, self.test_target), 3),
            )
            self.prediction = np.round_(self.model.predict(self.test_input), 2)

            ## feature import table pop-up
            if self.selected_ML == "RandomForestRegressor":
                self.fn_feature_import()
            else:
                pass

    # def predict_ML(self):
