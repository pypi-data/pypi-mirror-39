# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize
import math

plt.ion()

# Support Vector Machine Model
class model:
	# kernal, e.g. (X' . X) for linear SVM
	def __init__(self, kernal):
		self.kernal = kernal

	# svm equation to be minimized
	# 1 / 2 * (W'  W) - (summation of lambdas)
	# where W = summation of lambda*y*x
	# lambdas are lagrange multipliers
	def svm_equation(self, lambdas, x_train, y_train):
		ret = 0
		N = len(x_train)
		for i in range(N):
			for j in range(N):
				ret += lambdas[i] * lambdas[j] * y_train[i] * y_train[j] * self.kernal(x_train[i], x_train[j])
		ret /= 2
		for i in range(N):
			ret -= lambdas[i]
		return ret
	
	# constraint --> summation of lambda*y = 0
	def svm_constraint(self, lambdas, y_train):
		total = 0
		for l, y in zip(lambdas[:-1], y_train):
			total += l * y
		return total

	def fit(self, x_train, y_train):
		# bounds fro lambda values
		bounds = np.array([(0, 100000)] * (len(x_train) + 1))
		cons = ({'type':'eq', 'fun':self.svm_constraint, 'args':[y_train]})
		# one more lambda for mu (for constaint)
		self.lambdas = minimize(self.svm_equation, np.random.rand(len(x_train) + 1), args=(x_train, y_train), bounds=bounds, constraints=cons).x
		# list of support vectors
		self.support_vectors = np.empty((0, len(x_train[0])), int)
		# list of (lambda * y)
		self.multipliers = np.empty((0), int)
		# save support vectors and multipliers where lambda != 0
		for i, l in enumerate(self.lambdas[:-1]):
			if not l or l < 1e-5: continue
			self.support_vectors = np.append(self.support_vectors, [x_train[i]], axis=0)
			self.multipliers = np.append(self.multipliers, [l * y_train[i]], axis=0)
		# Y = W' . X + B
		# B is bias
		self.bias = 0
		for i, l in enumerate(self.lambdas[:-1]):
			if not l or l < 1e-5: continue
			self.bias = y_train[i] - np.sum(np.array([self.multipliers]).T * self.kernal(self.support_vectors, np.array([x_train[i]])))
			break

	# y_pred = signum(W' . X + B)
	def predict(self, x_test):
		out = self.bias + np.sum(np.array([self.multipliers] * len(x_test)).T * self.kernal(self.support_vectors, x_test), axis=0)
		return np.array([1 if ele >= 0 else -1 for ele in out])

	# find accuracy over test dataset
	def evaluate(self, x_test, y_test):
		out = self.bias + np.sum(np.array([self.multipliers] * len(x_test)).T * self.kernal(self.support_vectors, x_test), axis=0)
		return np.count_nonzero(np.array([1 if ele >= 0 else -1 for ele in out]) == y_test) / len(x_test) * 100

	def plot_data(self, x, y, type):
		y_pred = self.predict(x)
		done_p = False
		done_n = False
		for i in range(len(x)):
			if y[i] == 1:
				plt.scatter(x[i][0], x[i][1], color='blue' if type == 'train' else 'red', marker='x', label=type+"ing data, y=+1" if not done_p else "")
				done_p = True
			else:
				plt.scatter(x[i][0], x[i][1], color='blue' if type == 'train' else 'red', marker='+', label=type+"ing data, y=-1" if not done_n else "")
				done_n = True
		plt.legend()
		plt.pause(1e-10)

	def plot_decision_boundary(self):
		delta = 0.025
		x1, x2 = np.meshgrid(np.arange(-0.1, 1.1, delta), np.arange(-0.1, 1.1, delta))
		X = np.empty((0, 2))
		for i in range(x1.shape[0]):
			for j in range(x1.shape[1]):
				X = np.append(X, np.array([[x1[i][j], x2[i][j]]]), axis=0)
		out = self.bias + np.sum(np.array([self.multipliers] * len(X)).T * self.kernal(self.support_vectors, X), axis=0)
		out2 = np.empty((0, x1.shape[1]))
		ptr = 0
		for i in range(x1.shape[0]):
			row = np.array([])
			for j in range(x1.shape[1]):
				row = np.append(row, out[ptr])
				ptr += 1
			out2 = np.append(out2, [row], axis=0)
		cont = plt.contour(x1, x2, out2, [0])
		cont.collections[0].set_label('Predicted Boundary')
		cont = plt.contourf(x1, x2, out2, [-1, 0, 1], alpha=0.3)
		plt.legend()
		plt.pause(1e-10)