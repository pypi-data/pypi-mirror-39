# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

# utility functions
import numpy as np

def mse(X1, X2):
	diff = (X1 - X2)
	E = 1 / len(X1) * np.dot(diff.T, diff)
	return E.item(0)

def sigmoid(z):
	return (1 / (1 + np.exp(-z)))