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


from sklearn.tree import DecisionTreeRegressor

class DecisionGraftRegressor(RegressorsConcatenator):
    """
    A concatenation of multiple DecisionTreeRegressor, each receiving as input
    the residuals of the previous one.
    """
    def __init__(self, n, **kwargs):
        models = [DecisionTreeRegressor(**kwargs) for i in range(n)]
        RegressorsConcatenator.__init__(self, models)

class SandwichRegressor(RegressorsConcatenator):
    """
    Repeat multiple times a given concatenation of models, each receiving as
    input the residuals of the previous one.
    Differently from RegressorsConcatenar, it accepts model classes and
    and initialization args, not instances.
    "model_ts" is an iterable of (model_klass, model_kwargs) tuples.
    """
    def __init__(self, model_ts, n):
        models = [item(**kwargs) for i in range(n)
                                 for (item, kwargs) in model_ts]]
        RegressorsConcatenator.__init__(self, models)
