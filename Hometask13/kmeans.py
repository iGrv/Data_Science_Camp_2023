import numpy as np


class KMeans:
    '''
    Implements the k-means clustering algorithm
    :param k: number of clusters and their centroids, defaults to 2
    :type k: int, optional
    :param max_iter: maximum number of algorithm iterations, defaults to 100
    :type max_iter: int, optional
    :param random_state: random generation number for centroid initialization, defaults to None
    :type random_state: int or None
    '''
    def __init__(self, k=2, max_iter=100, random_state=None):
        self.k_number = k
        self.max_iter = max_iter
        np.random.seed(random_state)

    def fit(self, X):
        '''
        Computes the k-means clustering
        :param X: training samples data
        :type X: numpy ndarray of shape `(m, n)`
        '''
        # Get the number of samples and the number of features
        self.m, self.n = X.shape

        # Initialize random centroids, assign centroid labels
        # to each sample and compute starting cost
        centroids = self._init_centroids(X)
        labels = self._closest_centroids(X, centroids)
        cost = self._cost(X, labels, centroids)

        iter_number = 0  # Used for limit by max_iter
        while True:

            # Compute new centroids, assign new labels and compute new cost
            new_centoids = self._mean_centroids(X, labels, centroids)
            new_labels = self._closest_centroids(X, new_centoids)
            new_cost = self._cost(X, new_labels, new_centoids)

            # Exit the loop if cost no longer decreases or iter_number reaches max_iter
            if new_cost == cost or iter_number > self.max_iter:
                break
            else:
                centroids = new_centoids
                labels = new_labels
                cost = new_cost
            iter_number += 1  # Increment the number of iteration

        # Save computed centroids, labels and cost for further using
        self.centroids = centroids
        self.labels = labels
        self.final_cost = cost

    def fit_predict(self, X):
        '''
        Computes the centroids and assigns the centroids to each sample
        :param X: samples data
        :type X: numpy ndarray of shape `(m, n)`
        :return: labels (assignments)
        :rtype: numpy ndarray of shape `(m,)`
        '''
        self.fit(X)
        return self.labels

    def _cost(self, X, y, centroids):
        '''
        Computes the cost based on distances between samples and centroids
        :param X: samples data
        :type X: numpy ndarray of shape `(m, n)`
        :param y: labels (centroid assignments)
        :type y: numpy ndarray of shape `(m,)`
        :param centroids: centroids data
        :type centroids: numpy ndarray of shape `(k, n)`
        :return: computed cost
        :rtype: float
        '''
        # Compute sum of squares of distances between samples and assigned
        # to them centroids and divide it on number of samples
        return (1 / self.m) * sum(
            np.sum(self.__all_distances(X[y == i], centroids[i].reshape(1, -1))**2)
            for i in range(centroids.shape[0])
        )

    def _init_centroids(self, X):
        '''
        Initializes the k random centroids among the samples
        :param X: samples data
        :type X: numpy ndarray of shape `(m, n)`
        :return: centroids data
        :rtype: numpy ndarray of shape `(k, n)`
        '''
        # Choose indexes in range 0 to k randomly and select samples by chosen indexes
        indexes = np.random.choice(self.m, self.k_number, replace=False)
        return X[indexes, :]

    def _closest_centroids(self, X, centroids):
        '''
        Assigns the centroids to each sample by choosing the closest centroid
        :param X: samples data
        :type X: numpy ndarray of shape `(m, n)`
        :param centroids: centroids data
        :type centroids: numpy ndarray of shape `(k, n)`
        :return: labels (assignments)
        :rtype: numpy ndarray of shape `(m,)`
        '''
        # Compute the distances from samples to each centroid and
        # select the centroid with lowest distance for each sample
        distances = self.__all_distances(X, centroids)
        return np.apply_along_axis(np.argmin, 1, distances)

    def _mean_centroids(self, X, y, centroids):
        '''
        Calculates new centroids as means (centers) of samples assigned to the centroids
        :param X: samples data
        :type X: numpy ndarray of shape `(m, n)`
        :param y: labels (centroid assignments)
        :type y: numpy ndarray of shape `(m,)`
        :param centroids: centroids data
        :type centroids: numpy ndarray of shape `(k, n)`
        :return: new centroids data
        :rtype: numpy ndarray of shape `(k, n)`
        '''
        # Calculate the feature means of samples assigned to each centroid
        return np.array([

            # If there are no samples assigned to the centroid, the just set the same centroid
            np.mean(X[y == i], axis=0) if i in y else self.centroids[i]
            for i in range(centroids.shape[0])
        ])

    def __all_distances(self, X, centroids):
        '''
        Computes the distances between samples and all centroids (uses Euclidean distance as a metric)
        :param X: samples data
        :type X: numpy ndarray of shape `(m, n)`
        :param centroids: centroids data
        :type centroids: numpy ndarray of shape `(k, n)`
        :return: distances to all centroids
        :rtype: numpy ndarray of shape `(m, k)`
        '''
        return np.apply_along_axis(lambda x: self.__distances(x, centroids), 1, X)

    def __distances(self, x, centroids):
        '''
        Computes the distances between single sample and all centroids (uses Euclidean distance as a metric)
        :param x: single sample
        :type x: numpy ndarray of shape `(n,)`
        :param centroids: centroids data
        :type centroids: numpy ndarray of shape `(k, n)`
        :return: distances to all centroids
        :rtype: numpy ndarray of shape `(k,)`
        '''
        return np.apply_along_axis(lambda c: np.sqrt(np.sum((x - c)**2)), 1, centroids)
