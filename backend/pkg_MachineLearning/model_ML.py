from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor,
    VotingRegressor,
)
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class ModelTrainer:
    def __init__(self, data, target, model_type):
        self.data = data
        self.target = target
        self.model_type = model_type.strip()
        self.train_input, self.test_input, self.train_target, self.test_target = (
            train_test_split(data, target, test_size=0.2)
        )
        self.train_scaled = None
        self.test_scaled = None
        self.model = None
        self.prediction = None

    def preprocess_data(self, scaler=StandardScaler(), poly_degree=None):
        if poly_degree:
            poly = PolynomialFeatures(degree=poly_degree, include_bias=False)
            self.train_input = poly.fit_transform(self.train_input)
            self.test_input = poly.transform(self.test_input)
        if scaler:
            self.train_scaled = scaler.fit_transform(self.train_input)
            self.test_scaled = scaler.transform(self.test_input)

    def select_model(self):
        if self.model_type == "RandomForestRegressor":
            self.model = RandomForestRegressor(
                max_depth=40,
                max_features="sqrt",
                min_samples_split=2,
                n_estimators=90,
                n_jobs=-1,
            )
        elif self.model_type == "Gradient_Boosting":
            self.model = GradientBoostingRegressor(n_estimators=500, learning_rate=0.2)
        elif self.model_type == "Histogram-based Gradient Boosting":
            self.model = HistGradientBoostingRegressor()
        elif self.model_type == "XGBoost":
            from xgboost import XGBRegressor

            self.model = XGBRegressor(tree_method="hist")
        elif self.model_type == "VotingRegressor":
            model1 = Ridge(alpha=0.1)
            model2 = RandomForestRegressor(n_jobs=-1)
            model3 = KNeighborsRegressor()
            self.preprocess_data()
            self.model = VotingRegressor(
                estimators=[("ridge", model1), ("random", model2), ("neigh", model3)]
            )
        elif self.model_type == "LinearRegression":
            self.preprocess_data()
            self.model = LinearRegression()
        elif self.model_type == "PolynomialFeatures with linear regression":
            self.preprocess_data(poly_degree=3)
            self.model = LinearRegression()
        elif self.model_type == "Ridge regularization(L2 regularization)":
            self.preprocess_data(poly_degree=3)
            self.model = Ridge(alpha=0.1)
        elif self.model_type in [
            "DecisionTreeRegressor(scaled data)",
            "DecisionTreeRegressor(No scaled data)",
        ]:
            if "scaled" in self.model_type:
                self.preprocess_data()
            self.model = DecisionTreeRegressor(max_depth=10, random_state=42)
        elif self.model_type == "DL_DNN":
            import tensorflow as tf
            from tensorflow import keras

            self.preprocess_data()

            def build_dnn():
                dense1 = keras.layers.Dense(
                    100,
                    activation="relu",
                    input_shape=(self.train_scaled.shape[1],),
                    name="hidden",
                )
                dense2 = keras.layers.Dense(10, activation="relu")
                dense3 = keras.layers.Dense(1)
                model = keras.Sequential([dense1, dense2, dense3])
                optimizer = tf.keras.optimizers.Adam(0.001)
                model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])
                return model

            self.model = build_dnn()
            print(self.model.summary())

            early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10)
            history = self.model.fit(
                self.train_scaled,
                self.train_target,
                epochs=1000,
                batch_size=3,
                validation_split=0.2,
                verbose=0,
                callbacks=[early_stop],
            )

            self.prediction = self.model.predict(self.test_scaled).flatten()
            self.plot_dnn_history(history)

        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def train_and_evaluate(self):
        if self.model_type not in ["DL_DNN", "DecisionTreeRegressor(No scaled data)"]:
            self.model.fit(self.train_input, self.train_target)
            self.prediction = self.model.predict(self.test_input)

        print(
            "훈련 세트 정확도: ", self.model.score(self.train_input, self.train_target)
        )
        print(
            "테스트 세트 정확도: ", self.model.score(self.test_input, self.test_target)
        )

        if "DecisionTree" in self.model_type:
            self.plot_tree_model()
        else:
            self.plot_regression_results()

    def plot_dnn_history(self, history):
        hist = pd.DataFrame(history.history)
        hist["epoch"] = history.epoch

        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.xlabel("Epoch")
        plt.ylabel("Mean Abs Error [Cm]")
        plt.plot(hist["epoch"], hist["mae"], label="Train Error")
        plt.plot(hist["epoch"], hist["val_mae"], label="Val Error")
        plt.ylim([0, 2])
        plt.legend()

        plt.subplot(2, 2, 2)
        plt.xlabel("Epoch")
        plt.ylabel("Mean Square Error [$Cm^2$]")
        plt.plot(hist["epoch"], hist["mse"], label="Train Error")
        plt.plot(hist["epoch"], hist["val_mse"], label="Val Error")
        plt.ylim([0, 3])
        plt.legend()

        plt.subplot(2, 2, 3)
        plt.scatter(self.test_target, self.prediction)
        plt.xlabel("True Values [Cm]")
        plt.ylabel("Predictions [Cm]")
        plt.axis("equal")
        plt.axis("square")
        plt.xlim([0, plt.xlim()[1]])
        plt.ylim([0, plt.ylim()[1]])
        _ = plt.plot([-10, 10], [-10, 10])

        plt.subplot(2, 2, 4)
        error = self.prediction - self.test_target
        plt.hist(error, bins=25)
        plt.xlabel("Prediction Error [Cm]")
        _ = plt.ylabel("Count")

        plt.show()

    def plot_regression_results(self):
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.scatter(self.test_target, self.prediction)
        plt.xlabel("True Values [Cm]")
        plt.ylabel("Predictions [Cm]")
        plt.axis("equal")
        plt.axis("square")
        plt.xlim([0, plt.xlim()[1]])
        plt.ylim([0, plt.ylim()[1]])
        _ = plt.plot([-10, 10], [-10, 10])

        plt.subplot(2, 2, 2)
        error = self.prediction - self.test_target
        plt.hist(error, bins=25)
        plt.xlabel("Prediction Error [Cm]")
        _ = plt.ylabel("Count")

        plt.show()

    def plot_tree_model(self):
        plt.figure(figsize=(10, 7))
        plot_tree(
            self.model,
            max_depth=2,
            filled=True,
            feature_names=[
                "txFrequencyHz",
                "focusRangeCm",
                "numTxElements",
                "txpgWaveformStyle",
                "numTxCycles",
                "elevAperIndex",
                "IsTxAperModulationEn",
                "probePitchCm",
                "probeRadiusCm",
                "probeElevAperCm0",
                "probeElevFocusRangCm",
            ],
        )
        plt.show()

    def fn_feature_import(self):
        if hasattr(self.model, "feature_importances_"):
            df_import = pd.DataFrame(
                [np.round((self.model.feature_importances_) * 100, 2)],
                columns=[
                    "txFrequencyHz",
                    "focusRangeCm",
                    "numTxElements",
                    "txpgWaveformStyle",
                    "numTxCycles",
                    "elevAperIndex",
                    "IsTxAperModulationEn",
                    "probePitchCm",
                    "probeRadiusCm",
                    "probeElevAperCm0",
                    "probeElevFocusRangCm",
                ],
            )
            print(df_import)


# 사용 예시
# data와 target은 사용자 데이터셋에 따라 달라집니다.
data = ...  # 사용자의 데이터셋
target = ...  # 사용자의 타겟 값
model_type = "RandomForestRegressor"  # 선택된 모델 타입

trainer = ModelTrainer(data, target, model_type)
trainer.select_model()
trainer.train_and_evaluate()
