# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

import numpy as np
from numpy.linalg import inv
from vin_ml.utils import mse

# linear regression model
class model:
	def __init__(self, regularization=0):
		self.regularization = regularization

	# inv(X' . X + lambda . I) . X' . Y
	def fit(self, X, Y):
		self.W = np.dot(np.dot(inv(np.dot(X.T, X) + self.regularization * np.eye(X.shape[1])), X.T), Y)
		return self.W

	# (W' . X)
	def predict(self, x_test):
		return np.dot(x_test, self.W)

	# 1 / len(x_test) * (y_pred - y_test) * (y_pred - y_test)
	def loss(self, X, Y):
		y_pred = self.predict(X)
		return mse(y_pred, Y)