import pandas as pd
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class DataCleaning:

    def __init__(self, data):
        self.data = data
        self.duration = data['Duration']
        self.clean_data = None

    def selectFeatures(self):
        X = self.data.drop(['Duration'], axis=1)
        y = self.data['Duration']
        selector = SelectKBest(f_regression, k=10)
        selector.fit(X, y)
        cols = selector.get_support(indices=True)
        self.data = X.iloc[:, cols]

    def addDuration(self):
        self.data['Duration'] = self.duration

    def removeOutliers(self):
        zscore = np.abs(self.data - self.data.mean()) / self.data.std()
        threshold = 3
        self.data = self.data[(zscore < threshold).all(axis=1)]

    def getdata(self):
        return self.data
