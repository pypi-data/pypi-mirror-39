# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

import numpy as np
from vin_ml.utils import sigmoid, mse
from scipy.optimize import fmin_cg

# -1 / N * [summation of log of sigmoid(W' . X)]
def logisitic_loss(W, X, Y):
	if (W.ndim == 1): W = W.reshape((len(W), 1))
	N = len(X)
	J = -1 / N * np.sum(np.log(sigmoid((Y * np.dot(X, W)))))
	return J.item(0)

# 1 / N * (summation of (-Y . X . sigmoid(-Y . W' . X)))
def logistic_gradient(W, X, Y):
	W = W.reshape((len(W), 1))
	N = len(X)
	delta = 1 / N * np.dot(-(Y * X).T, sigmoid(-Y * np.dot(X, W)))
	return np.ndarray.flatten(delta)

# logistic regression model
class model:
	def fit(self, X, Y):
		# logistic loss optimizer (gradient descent)
		self.W = fmin_cg(f = logisitic_loss, x0 = np.zeros(len(X[0])), fprime = logistic_gradient, args = (X, Y)).reshape((len(X[0]), 1))
		return self.W

	# threshold over sigmoid(W' . X)
	def predict(self, X):
		y_pred = sigmoid(np.dot(X, self.W))
		y_pred = np.array([[1 if ele >= 0.5 else -1 for ele in y_pred]]).T
		return y_pred

	# find accuracy over test dataset
	def evaluate(self, X, Y):
		y_pred = self.predict(X)
		return np.count_nonzero(Y == y_pred) / len(X) * 100

	# find mean square loss over test dataset
	def loss(self, X, Y):
		y_pred = self.predict(X)
		return mse(y_pred, Y)