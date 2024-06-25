from sklearn.preprocessing import StandardScaler, PolynomialFeatures


class DataPreprocessor:
    """
    Data pre-processing: train_input and test_input
    """

    def __init__(self, train_input, test_input):
        self.train_input = train_input
        self.test_input = test_input
        self.train_scaled = None
        self.test_scaled = None

    def preprocess(self, model_type="other", scaler=StandardScaler()):
        # model_type에 다항식 및 standard 사용하기.
        if "PolynomialFeatures" in model_type.lower() or "Ridge" in model_type.lower():
            poly = PolynomialFeatures(degree=2, include_bias=False)
            self.train_input = poly.fit_transform(self.train_input)
            self.test_input = poly.transform(self.test_input)

            self.train_scaled = scaler.fit_transform(self.train_input)
            self.test_scaled = scaler.transform(self.test_input)

        else:
            self.train_scaled = self.train_input
            self.test_scaled = self.test_input

        return self.train_scaled, self.test_scaled
