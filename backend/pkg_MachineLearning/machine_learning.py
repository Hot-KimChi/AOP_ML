import os
import tkinter as tk
from tkinter import ttk
import joblib

from pkg_MachineLearning.fetch_selectFeature import merge_selectionFeature
from pkg_MachineLearning.data_splitting import dataSplit
from pkg_MachineLearning.data_preprocessing import DataPreprocessor
from pkg_MachineLearning.model_selection import ModelSelector
from pkg_MachineLearning.training_evaluation import ModelEvaluator
from pkg_MachineLearning.plotting import Plotter

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

        # Combo 선택한 ML update
        selectionML = self.combo_ML.get().replace(" ", "")
        selectionML = selectionML.strip()

        # 데이터 가져와서 feature selection / data 나누기
        data, target = merge_selectionFeature()
        train_input, test_input, train_target, test_target = dataSplit(data, target)

        # 데이터 전처리(train_scaled, test_scaled을 train_input, test_input으로 공통적으로 사용)
        preprocessor = DataPreprocessor(train_input, test_input)
        train_input, test_input = preprocessor.preprocess(model_type=selectionML)

        # 모델 선택
        selector = ModelSelector(model_type=selectionML)
        model = selector.select_model(train_input)

        # 모델 훈련 및 평가: train and test score에 대해서 출력까지 수행.
        evaluator = ModelEvaluator(
            model, train_input, train_target, test_input, test_target
        )
        evaluator.evaluate_model()

        # 결과 플롯팅
        Plotter.plot_regression_results(test_target, evaluator.prediction)
