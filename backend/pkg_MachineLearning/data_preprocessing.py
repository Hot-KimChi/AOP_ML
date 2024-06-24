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

    def preprocess(self, model_type="other", scaler=StandardScaler(), poly_degree=None):
        # model_type에 'randomforest' 또는 'tree' 키워드가 포함되면 스케일링 및 다항식 변환 생략
        if "randomforest" in model_type.lower() or "tree" in model_type.lower():
            self.train_scaled = self.train_input
            self.test_scaled = self.test_input
        else:
            # 다항식 변환 적용 (poly_degree가 주어졌을 경우)
            if poly_degree is not None:
                poly = PolynomialFeatures(degree=poly_degree, include_bias=False)
                self.train_input = poly.fit_transform(self.train_input)
                self.test_input = poly.transform(self.test_input)

            # 스케일링 적용 (scaler가 주어졌을 경우)
            if scaler is not None:
                self.train_scaled = scaler.fit_transform(self.train_input)
                self.test_scaled = scaler.transform(self.test_input)
            else:
                self.train_scaled = self.train_input
                self.test_scaled = self.test_input

        return self.train_scaled, self.test_scaled
