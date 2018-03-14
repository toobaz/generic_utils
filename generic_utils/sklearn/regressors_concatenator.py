import numpy as np

class RegressorsConcatenator:
    """
    Run a sequence of (sklearn) regression models, each on the residuals from
    the previous one.
    
    Only supports fit, predict, score.
    """
    def __init__(self, models):
        self._models = models

    def fit(self, X, y):
        self._fitted = []
        for idx, model in enumerate(self._models):
            fitted = model.fit(X, y)
            self._fitted.append(fitted)
            if idx == len(self._models) - 1:
                break
            pred = model.predict(X)
            # Take the residuals (but do not modify inplace)
            y = y - pred
        return self

    def predict(self, X):
        predicted = np.zeros(len(X))

        for idx, model in enumerate(self._fitted):
            predicted += model.predict(X)
        return predicted

    def score(self, X, y):
        pred_y = self.predict(X)
        return 1 - ((y - pred_y) ** 2).sum() / ((y - y.mean())**2).sum()


class DecisionGraftRegressor(RegressorsConcatenator):
    """
    A concatenation of multiple DecisionTreeRegressor, each receiving as input
    the residuals of the previous one.
    """
    def __init__(self, n, **kwargs):
        models = [DecisionTreeRegressor(**kwargs) for i in range(n)]
        RegressorsConcatenator.__init__(self, models)
