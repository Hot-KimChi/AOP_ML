from sklearn.model_selection import cross_validate
import numpy as np


class ModelEvaluator:
    """
    모델을 훈련시키는 algorithm
    """

    def __init__(
        self, model, train_input, train_target, test_input, test_target, selected_ML
    ):
        self.model = model
        self.train_input = train_input
        self.train_target = train_target
        self.test_input = test_input
        self.test_target = test_target
        self.selected_ML = selected_ML
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
        self.train_model()
        self.evaluate_test_set()

    def print_scores(self, scores):
        print(
            f"\n{self.selected_ML} - Train R^2:",
            np.round_(np.mean(scores["train_score"]), 3),
        )
        print(
            f"{self.selected_ML} - Train_validation R^2:",
            np.round_(np.mean(scores["test_score"]), 3),
        )

    def train_model(self):
        self.model.fit(self.train_input, self.train_target)

    def evaluate_test_set(self):
        test_score = np.round_(self.model.score(self.test_input, self.test_target), 3)
        print(f"{self.selected_ML} - Test R^2:", test_score)
        self.prediction = np.round_(self.model.predict(self.test_input), 2)

    def train_dnn_model(self):
        from tensorflow import keras

        early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10)
        history = self.model.fit(
            self.train_input,
            self.train_target,
            epochs=1000,
            batch_size=3,
            validation_split=0.2,
            verbose=0,
            callbacks=[early_stop],
        )
        prediction = self.model.predict(self.test_input).flatten()
        return history, prediction
