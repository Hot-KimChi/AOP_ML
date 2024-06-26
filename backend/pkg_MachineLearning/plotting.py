import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Plotter:
    """
    플롯팅 관련 코드
    """

    @staticmethod
    def plot_dnn_history(history, test_target=None, prediction=None):
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

        if test_target is not None and prediction is not None:
            plt.subplot(2, 2, 3)
            plt.scatter(test_target, prediction)
            plt.xlabel("True Values [Cm]")
            plt.ylabel("Predictions [Cm]")
            plt.axis("equal")
            plt.axis("square")
            plt.xlim([0, plt.xlim()[1]])
            plt.ylim([0, plt.ylim()[1]])
            _ = plt.plot([-10, 10], [-10, 10])

            plt.subplot(2, 2, 4)
            error = prediction - test_target
            plt.hist(error, bins=25)
            plt.xlabel("Prediction Error [Cm]")
            _ = plt.ylabel("Count")

        plt.show()

    @staticmethod
    def plot_regression_results(test_target, prediction):
        plt.figure(figsize=(12, 8))

        plt.subplot(2, 2, 1)
        plt.scatter(test_target, prediction)
        plt.xlabel("True Values [Cm]")
        plt.ylabel("Predictions [Cm]")
        plt.axis("equal")
        plt.axis("square")
        plt.xlim([0, plt.xlim()[1]])
        plt.ylim([0, plt.ylim()[1]])
        _ = plt.plot([-10, 10], [-10, 10])

        plt.subplot(2, 2, 2)
        error = prediction - test_target
        plt.hist(error, bins=25)
        plt.xlabel("Prediction Error [Cm]")
        _ = plt.ylabel("Count")

        plt.show()

    @staticmethod
    def plot_feature_importance(model, feature_list):
        try:
            df_import = pd.DataFrame()
            df_import = df_import.append(
                pd.DataFrame(
                    [np.round((model.feature_importances_) * 100, 2)],
                    columns=feature_list,
                ),
                ignore_index=True,
            )

            print("Feature Importances:")
            print(df_import)

            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1]
            x = np.arange(len(importances))

            plt.figure(figsize=(10, 8))
            plt.title("Feature Importance")
            plt.bar(x, importances[indices], align="center")
            labels = (
                feature_list
                if feature_list
                else [f"Feature {i}" for i in range(len(importances))]
            )
            plt.xticks(x, np.array(labels)[indices], rotation=90)
            plt.xlim([-1, len(importances)])
            plt.tight_layout()
            plt.show()

        except AttributeError:
            print("Feature importances can only be computed for tree-based models.")


# 사용 예시
# history 객체는 텐서플로우 모델 훈련 결과로부터 생성
# test_target과 prediction 데이터는 모델 예측 결과로부터 생성
# Plotter.plot_dnn_history(history, test_target, prediction)
# Plotter.plot_regression_results(test_target, prediction)
