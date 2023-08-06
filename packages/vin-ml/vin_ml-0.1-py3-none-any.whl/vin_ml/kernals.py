# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

# KERNALS used in svm demo
import numpy as np

def linear(x, y):
	return np.dot(x, y.T)

def polynomial(x, y, p = 2):
	return (1 + np.dot(x, y.T)) ** p

# add more kernals as per usage