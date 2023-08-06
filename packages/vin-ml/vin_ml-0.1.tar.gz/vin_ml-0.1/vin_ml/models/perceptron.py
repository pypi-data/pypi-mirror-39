# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

import numpy as np

class model:
	def __init__(self, lr):
		self.lr = lr
		self.W = np.random.rand(3)

	# update weight if Y * (W' . X) < 0
	def fit(self, X, Y):
		X = np.array([np.append(x, 1) for x in X])
		done = False
		while not done:
			done = True
			for i, x in enumerate(X):
				if (np.dot(self.W, X[i]) >= 0) != (Y[i] == 1):
					self.W += np.dot(Y[i], X[i])
					done = False
					break
		return self.W

	# y_pred = signum(W' . x_test)
	def predict(self, x_test):
		x_test = np.array([np.append(x, 1) for x in x_test])
		y_pred = []
		for i, x in enumerate(x_test):
			y_pred.append(1 if np.dot(self.W, x_test[i]) >= 0 else -1)
		return np.array(y_pred)

	# find accuracy over test dataset
	def evaluate(self, x_test, y_test):
		y_pred = self.predict(x_test)
		return np.count_nonzero(y_pred == y_test) / len(y_pred) * 100