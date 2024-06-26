from sklearn.model_selection import cross_validate
import numpy as np
import os, sys
import joblib
import sklearn


class ModelEvaluator:
    """
    1) 모델을 cross_validate algorithm
    2) train / train_validation score 출력하는 algorithm
    """

    def __init__(self, model, train_input, train_target, test_input, test_target):
        self.model = model
        self.train_input = train_input
        self.train_target = train_target
        self.test_input = test_input
        self.test_target = test_target
        self.prediction = None

    def evaluate_model(self):
        scores = cross_validate(
            self.model,
            self.train_input,
            self.train_target,
            return_train_score=True,
            n_jobs=-1,
        )
        self.print_scores(scores)
        self.evaluate_test_set()

    def print_scores(self, scores):
        train_score_mean = self.calculate_mean_score(scores["train_score"])
        test_score_mean = self.calculate_mean_score(scores["test_score"])
        print(f"\n{self.model.__class__.__name__} - Train R^2:", train_score_mean)
        print(f"{self.model.__class__.__name__} - Validation R^2:", test_score_mean)

    @staticmethod
    def calculate_mean_score(scores):
        return np.round_(np.mean(scores), 3)

    def evaluate_test_set(self):
        self.model.fit(self.train_input, self.train_target)
        test_score = self.calculate_mean_score(
            [self.model.score(self.test_input, self.test_target)]
        )
        print(f"{self.model.__class__.__name__} - Test R^2:", test_score)
        self.prediction = np.round_(self.model.predict(self.test_input), 2)

    def modelSave(self):
        newpath = "./backend/Model"
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        python_version = f"{sys.version_info.major}{sys.version_info.minor}"
        sklearn_version = sklearn.__version__
        model_name = self.model.__class__.__name__

        if "DNN" in self.model:
            self.model.save(f"{newpath}/{model_name}_v1_python{python_version}_tf.h5")
        else:
            joblib.dump(
                self.model,
                f"{newpath}/{model_name}_v1_python{python_version}_sklearn{sklearn_version}.pkl",
            )

    # def train_dnn_model(self):
    #     from tensorflow import keras

    #     early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10)
    #     history = self.model.fit(
    #         self.train_input,
    #         self.train_target,
    #         epochs=1000,
    #         batch_size=3,
    #         validation_split=0.2,
    #         verbose=0,
    #         callbacks=[early_stop],
    #     )
    #     prediction = self.model.predict(self.test_input).flatten()
    #     return history, prediction
