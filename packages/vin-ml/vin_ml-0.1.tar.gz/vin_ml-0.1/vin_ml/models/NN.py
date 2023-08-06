# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

from numpy import dot
import numpy as np

# gradient at last (output) node, for sigmoid (use accordingly)
def grad(Y, y):
	return (Y - y) * y * (1 - y)

# softmax for output layer e^x / [summation of e^x]
def softmax(X):
	base = np.sum(np.exp(X))
	return np.exp(X) / base

# multiple activation functions
def activate(X, activation_func="sigmoid"):
	if activation_func == "sigmoid":
		return 1 / (1 + np.exp(-X))
	elif activation_func == "tanh":
		return np.tanh(X)
	elif activation_func == "sin":
		return np.sin(X)
	elif activation_func == "cos":
		return np.cos(X)

# initialize random weights
def random_weights(neurons_per_layer, bias):
	W = []
	for layer in range(1, len(neurons_per_layer)):
		W.append(np.random.randn(neurons_per_layer[layer], neurons_per_layer[layer - 1] + (1 if bias else 0)))
	return W

# Neural Network Model
class model:
	def __init__(self, number_of_layers, alpha, neurons_per_layer, activations_per_layer, bias=True, W=[]):
		# total number of layer of NN, excluding input layer and including hidden and output layer
		self.number_of_layers = number_of_layers
		# learning rate
		self.alpha = alpha
		# boolean (to use bias at each layer or not)
		self.bias = bias
		# list of number of neaurons at each layer
		self.neurons_per_layer = neurons_per_layer.copy()
		# activation functions to be used at each layer
		self.activation_func = activations_per_layer.copy()
		# weights, if already trained
		if W: self.W = W
		# weights, if randomly needed
		else: self.W = random_weights(self.neurons_per_layer, self.bias)

	# forward propagation
	def forward(self, X):
		# actiavte(z)
		self.a = []
		# (W' . X)
		self.z = []
		# delta at each layer
		self.delta = []
		# initial input
		self.a.append(X)
		for layer in range(self.number_of_layers):
			if self.bias:
				self.a[layer] = np.append(self.a[layer], np.ones((1, 1)), axis=0)
			self.z.append(dot(self.W[layer], self.a[layer]))
			# print(activate(self.z[layer], self.activation_func[layer]).shape)
			self.a.append(activate(self.z[layer], self.activation_func[layer]))
		if self.activation_func[-1] == "sigmoid":
			return self.a[-1]
		else:
			# for tanh
			return (self.a[-1] + 1) / 2

	# backward propagation
	def backward(self, Y, y):
		# find gradient at last (output) layer
		gradient = grad(Y, y)
		self.delta = [np.array([]) for layer in range(self.number_of_layers + 1)]
		# find delta at each layer and then update weights
		if self.bias:
			self.delta[self.number_of_layers] = np.append(gradient, np.ones((1, 1)), axis=0)
			for layer in range(self.number_of_layers - 1, -1, -1):
				if self.activation_func[layer] == "sigmoid":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * self.a[layer] * (1 - self.a[layer])
				elif self.activation_func[layer] == "tanh":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * (1- self.a[layer] * self.a[layer])
				elif self.activation_func[layer] == "sin":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * np.cos(self.a[layer])
				elif self.activation_func[layer] == "cos":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * (-np.sin(self.a[layer]))
			for layer in range(self.number_of_layers):
				self.W[layer] = self.W[layer] + self.alpha * dot(self.delta[layer + 1][:-1], np.transpose(self.a[layer]))
		else:
			self.delta[self.number_of_layers] = gradient
			for layer in range(self.number_of_layers - 1, -1, -1):
				if self.activation_func[layer] == "sigmoid":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * self.a[layer] * (1 - self.a[layer])
				elif self.activation_func[layer] == "tanh":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * (1- self.a[layer] * self.a[layer])
				elif self.activation_func[layer] == "sin":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * np.cos(self.a[layer])
				elif self.activation_func[layer] == "cos":
					self.delta[layer] = dot(np.transpose(self.W[layer]), self.delta[layer + 1][:-1]) * (-np.sin(self.a[layer]))
			for layer in range(self.number_of_layers):
				self.W[layer] = self.W[layer] + self.alpha * dot(self.delta[layer + 1], np.transpose(self.a[layer]))
