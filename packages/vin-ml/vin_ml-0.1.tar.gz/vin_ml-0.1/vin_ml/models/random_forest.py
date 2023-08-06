# Author: Vinayak Sachdeva
# Btech, MNIT Jaipur

from math import log2
import numpy as np
import pydotplus as pdp
from math import inf

NODE_FILL_COLOR = ["red", "green", "blue", "green", "grey"]
FONT_COLOR = ["white", "blue", "white", "blue", "white"]

def most_common(L):
  return max(set(L), key=list(L).count)

# this is recurive implementation of decision tree, with current root node as instance of this model, childrens are also instance of this model
class model:
	def __init__(self, data, feature_index, target, levels, features, most_frequent_target_value):
		# childrens of this node after classifying data by maximum IGR
		self.children = {}
		# entropy at this node
		self.entropy = 0
		self.is_leaf = False
		# Target feature value
		self.target_value = ""
		# Maximum IGR feature name
		self.max_igr_feature = ""
		# Target feature name
		self.target = target
		# data contains all the data to be trained on decision tree
		# a 2D array, with a row containing single instance (values) of data
		self.data = data.copy()
		# feature index, dictionary with key as feature name and value as index column of that feature in 2D data (0-based)
		self.feature_index = feature_index.copy()
		# dictionary with key as feature name and value as a list of values which that feature can take
		self.levels = levels.copy()
		# list of all features
		self.features = features.copy()
		self.most_frequent_target_value = most_frequent_target_value
		if not len(data):
			self.is_leaf = True
			self.target_value = most_frequent_target_value
			# print("No Data, Set Target Value to", self.target_value)
			return
		if not len(features):
			self.is_leaf = True
			self.target_value = most_common(data[:, -1].flatten())
			# print("No Data, Set Target Value to", self.target_value)
			return
		# find entropy of whole dataset at this node
		if len(self.data):
			self.entropy = self.find_entropy_whole_dataset(self.data, self.target)
		if (self.entropy == 0):
			# if node has entropy 0 w.r.t. target, then this is leaf node
			self.is_leaf = True
			self.target_value = self.data[0][feature_index[target]]
			# print("Set Target Value to", self.target_value)
		# else:
			# print("H (", self.target, ") =", self.entropy)

	# entroy of data w.r.t. some feature
	def find_entropy_whole_dataset(self, data, feature):
		# negative summation of log probablities multiplied with probability
		count = {}
		for level in self.levels[feature]:
			count[level] = 0
		data_length = len(data)
		entropy = 0
		for row in data:
			count[row[self.feature_index[feature]]] += 1
		for level in self.levels[feature]:
			probability = count[level] / data_length
			if not probability:
				continue
			entropy += -1 * probability * log2(probability)
		return entropy

	# filter data with the feature value, take only that subset of data which has specified feature value
	def filter_data(self, feature, value):
		filtered_data = []
		for row in self.data:
			if row[self.feature_index[feature]] == value:
				filtered_data.append(row)
		return filtered_data

	# calculates remaining entropy of feature2 after dividing data with feature1 
	def find_entropy_wrt_feature(self, data, feature1, feature2):
		count = {}
		for level in self.levels[feature1]:
			count[level] = 0
		for row in data:
			count[row[self.feature_index[feature1]]] += 1 
		data_length = len(data)
		entropy = 0
		for level in self.levels[feature1]:
			probability = count[level] / data_length
			filtered_data = self.filter_data(feature1, level)
			if not probability:
				continue
			entropy += probability * self.find_entropy_whole_dataset(filtered_data, feature2)
		return entropy

	def find_information_gain(self, feature1, feature2):
		return self.entropy - self.find_entropy_wrt_feature(self.data, feature1, feature2)

	def find_information_gain_ratio(self, feature):
		entropy_wrt_feature = self.find_entropy_whole_dataset(self.data, feature)
		return self.find_information_gain(feature, self.target) / entropy_wrt_feature if entropy_wrt_feature != 0 else inf

	# build tree
	def build(self):
		if self.is_leaf:
			return self
		information_gain_ratio = {}
		# find igr w.r.t. each feature
		for feature in self.features:
			information_gain_ratio[feature] = self.find_information_gain_ratio(feature)
			# print("IG (", feature, ") =", information_gain_ratio[feature])
		#select feature with maximum igr
		max_igr, self.max_igr_feature = max(zip(information_gain_ratio.values(), information_gain_ratio.keys()))
		# print("Best Feature: ", self.max_igr_feature)
		max_igr_feature_index = self.feature_index[self.max_igr_feature]
		# divide data and its properties w.r.t. each level of maximum igr feature and recursively build tree
		for level in self.levels[self.max_igr_feature]:
			if level not in np.array(self.data)[:, self.feature_index[self.max_igr_feature]]:
				continue
			# print("On Branch", self.max_igr_feature, "=", level)
			filtered_data = np.array(self.filter_data(self.max_igr_feature, level))
			if filtered_data.size:
				filtered_data = np.delete(filtered_data, [max_igr_feature_index, max_igr_feature_index], axis = 1)
			features = np.delete(np.array(self.features), [max_igr_feature_index, max_igr_feature_index])
			feature_index = {feature:index for feature, index in self.feature_index.items() if index != max_igr_feature_index}
			feature_index = {feature:(index if index < max_igr_feature_index else index - 1) for feature, index in feature_index.items()}
			self.children[level] = model(filtered_data, feature_index, self.target, self.levels, features, self.most_frequent_target_value).build()
		return self

	# dfs over tree to predict query
	def predict(self, query):
		if self.is_leaf:
			return self.target_value
		return self.children[query[self.max_igr_feature]].predict(query)

	# create real nodes into 'graph' variable using dfs
	def plot(self, graph, parent=None, parent_label=None, parent_child_edge=None, query=None, root=None):
		if self.is_leaf:
			if query and query[parent] == parent_child_edge:
				if query and self.target_value == query[self.target]:
					graph.add_node(pdp.Node(parent_label + parent_child_edge + self.target_value, label=self.target_value, shape="box", style="filled", fillcolor="skyblue", fontcolor="black"))
				else:
					graph.add_node(pdp.Node(parent_label + parent_child_edge + self.target_value, label=self.target_value, shape="box", style="filled", fillcolor="pink", fontcolor="black"))
				graph.add_edge(pdp.Edge(parent_label, parent_label + parent_child_edge + self.target_value, label=parent_child_edge, fontsize="14", color="black", fontcolor="purple"))
			else:
				graph.add_node(pdp.Node(parent_label + parent_child_edge + self.target_value, label=self.target_value, shape="box", style="filled", fillcolor="yellow", fontcolor="black"))
				graph.add_edge(pdp.Edge(parent_label, parent_label + parent_child_edge + self.target_value, label=parent_child_edge, fontsize="14", color="brown", fontcolor="purple"))
		else:
			index = root.feature_index[self.max_igr_feature]%len(NODE_FILL_COLOR)
			if parent_label:
				if query and query[parent] == parent_child_edge:
					graph.add_node(pdp.Node(parent_label + parent_child_edge + self.max_igr_feature, label=self.max_igr_feature, style="filled", fillcolor="black", fontcolor="white", color="white"))
					graph.add_edge(pdp.Edge(parent_label, parent_label + parent_child_edge + self.max_igr_feature, label=parent_child_edge, fontsize="14", color="black", fontcolor="purple"))
				else:
					graph.add_node(pdp.Node(parent_label + parent_child_edge + self.max_igr_feature, label=self.max_igr_feature, style="filled", fillcolor=NODE_FILL_COLOR[index], fontcolor=FONT_COLOR[index], color="white"))
					graph.add_edge(pdp.Edge(parent_label, parent_label + parent_child_edge + self.max_igr_feature, label=parent_child_edge, fontsize="14", color="brown", fontcolor="purple"))
				for level in self.levels[self.max_igr_feature]:
					if level not in self.children:
						continue
					if query and level == query[self.max_igr_feature]:
						self.children[level].plot(graph, parent=self.max_igr_feature, parent_label=parent_label + parent_child_edge + self.max_igr_feature, parent_child_edge=level, query=query, root=root)
					else:
						self.children[level].plot(graph, parent=self.max_igr_feature, parent_label=parent_label + parent_child_edge + self.max_igr_feature, parent_child_edge=level, root=root)
			else:
				if query:
					graph.add_node(pdp.Node(self.max_igr_feature, label=self.max_igr_feature, style="filled", fillcolor="black", fontcolor="white", color="white"))
				else:
					graph.add_node(pdp.Node(self.max_igr_feature, label=self.max_igr_feature, style="filled", fillcolor=NODE_FILL_COLOR[index], fontcolor=FONT_COLOR[index], color="white"))
				for level in self.levels[self.max_igr_feature]:
					if level not in self.children:
						continue
					if query and level == query[self.max_igr_feature]:
						self.children[level].plot(graph, parent=self.max_igr_feature, parent_label=self.max_igr_feature, parent_child_edge=level, query=query, root=root)
					else:
						self.children[level].plot(graph, parent=self.max_igr_feature, parent_label=self.max_igr_feature, parent_child_edge=level, root=root)

