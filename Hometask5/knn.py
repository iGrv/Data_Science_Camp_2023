import pandas as pd
import numpy as np


class Scaler:
    '''
    Transforms features using min-max scaling
    '''
    def fit(self, X):
        '''
        Computes minimum and maximum of features data for scaling
        :param X: features data
        :type X: pandas DataFrame
        '''
        self.min = X.min(axis=0)
        self.max = X.max(axis=0)

    def transform(self, X):
        '''
        Scales features data according to minimum and maximum
        :param X: features data
        :type X: pandas DataFrame
        '''
        return (X - self.min) / (self.max - self.min)

    def fit_transform(self, X):
        '''
        Computes minimum and maximum of features data, and then scales them
        :param X: features data
        :type X: pandas DataFrame
        '''
        self.fit(X)
        return self.transform(X)


class KNNClassifier:
    '''
    Implements the k-nearest neighbors algorithm for classification
    :param k: number of nearest neighbors to consider, defaults to 3
    :type k: int, optional
    '''
    def __init__(self, k=3):
        self.k_number = k

    def fit(self, X, y):
        '''
        Fits training data to the classifier
        :param X: features data
        :type X: pandas DataFrame
        :param y: labels data
        :type y: pandas Series
        '''
        self.X_data = X
        self.y_data = y

    def predict(self, X):
        '''
        Computes predictions for testing data
        :param X: features data
        :type X: pandas DataFrame
        :return: predictions
        :rtype: pandas Series
        '''
        return X.apply(self._predict, axis=1)

    def score(self, X, y):
        '''
        Computes mean accuracy on test data and labels
        :param X: features data
        :type X: pandas DataFrame
        :param y: labels data
        :type y: pandas Series
        :return: score
        :rtype: float
        '''
        return np.mean(self.predict(X) == y)

    def _predict(self, x):
        '''
        Computes single prediction for a row of testing data
        :param x: row of features data
        :type x: pandas Series
        :return: prediction
        '''
        # Compute distances between x and all rows in the features data
        distances = self.X_data.apply(lambda row: self._distance(row, x), axis=1).rename("distance")

        # Sort features by computed distances and get the first k labels
        k_labels = pd.concat([self.y_data, distances], axis=1).sort_values("distance").head(self.k_number)

        # Group labels by classes and compute numbers of the labels in each class
        classes = k_labels.groupby(self.y_data.name)[self.y_data.name].count()

        # Get the class which have the highest number of labels
        return classes.sort_values(ascending=False).index[0]

    def _distance(self, x1, x2):
        '''
        Computes distance between two rows using Euclidean distance as a metric
        :param x1: row of features data
        :type x1: pandas Series
        :param x2: row of features data
        :type x2: pandas Series
        :return: distance
        :rtype: float
        '''
        return np.sqrt(np.sum((x1 - x2)**2))
