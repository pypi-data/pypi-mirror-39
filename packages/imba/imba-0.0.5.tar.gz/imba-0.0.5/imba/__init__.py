# coding:utf-8

import pandas as pd
from sklearn.ensemble import RandomForestClassifier

class BinaryDownsampleBaggingClassifier():

    def __init__(self, model=None):
        self.models = []
        self.model  = model

    def fit(self, x, y, n_estimators=9):
        for i in range(n_estimators):
            yp = pd.concat([y[y==0].sample(len(y[y!=0])), y[y!=0]])
            xp = x.loc[yp.index, :]
            self.model.fit(xp, yp)
            self.models.append(self.model)

    def predict(self, x):
        votes = []
        for model in self.models:
            votes.append(pd.Series(model.predict(x)))
        return pd.concat(votes, axis=1).apply(pd.value_counts, axis=1).idxmax(axis=1)


    def predict_proba(self, x):
        probas = []
        for model in self.models:
            probas.append(pd.Series(model.predict_proba(x)[:,1]))
        return pd.concat(probas, axis=1).mean(axis=1)

if __name__ == '__main__':
    xt = pd.DataFrame([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1],
        [1, 1],
        ])
    yt = pd.Series([0, 0, 0, 1, 1])

    xv = pd.DataFrame([
        [0.0, 0.0],
        [0.5, 0.5],
        [1.0, 1.0],
        [2.0, 2.0],
        [3.0, 3.0],
        ])
    yv = pd.Series([0, 0, 1, 1, 1])

    base_estimator = RandomForestClassifier()

    model = BinaryDownsampleBaggingClassifier(base_estimator)
    model.fit(xt, yt)

    print(model.predict(xv))
    print(model.predict_proba(xv))
