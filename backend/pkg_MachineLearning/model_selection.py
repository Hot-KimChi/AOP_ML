from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    HistGradientBoostingRegressor,
    VotingRegressor,
)
from sklearn.linear_model import Ridge, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor


class ModelSelector:
    """
    모델 선택 및 초기화 관련 코드를 모듈화
    """

    def __init__(self, model_type):
        self.model_type = model_type.strip()
        self.model = None

    def select_model(self, train_scaled):
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
            self.model = VotingRegressor(
                estimators=[("ridge", model1), ("random", model2), ("neigh", model3)]
            )
        elif self.model_type == "LinearRegression":
            self.model = LinearRegression()
        elif self.model_type == "PolynomialFeatures with linear regression":
            self.model = LinearRegression()
        elif self.model_type == "Ridge regularization(L2 regularization)":
            self.model = Ridge(alpha=0.1)
        elif self.model_type in [
            "DecisionTreeRegressor(scaled data)",
            "DecisionTreeRegressor(No scaled data)",
        ]:
            self.model = DecisionTreeRegressor(max_depth=10, random_state=42)
        elif self.model_type == "DL_DNN":
            self.model = self.build_dnn(train_scaled)
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

        return self.model

    def build_dnn(self, train_scaled):
        import tensorflow as tf
        from tensorflow import keras

        def build_dnn_model():
            dense1 = keras.layers.Dense(
                100,
                activation="relu",
                input_shape=(train_scaled.shape[1],),
                name="hidden",
            )
            dense2 = keras.layers.Dense(10, activation="relu")
            dense3 = keras.layers.Dense(1)
            model = keras.Sequential([dense1, dense2, dense3])
            optimizer = tf.keras.optimizers.Adam(0.001)
            model.compile(loss="mse", optimizer=optimizer, metrics=["mae", "mse"])
            return model

        return build_dnn_model()
