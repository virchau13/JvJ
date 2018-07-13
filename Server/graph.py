# The graph
class Graph():
	def __init__(self, dict_dict):
		self.graph = {}
		for i in dict_dict.keys():
			self.new_node(i)
			for j in dict_dict.keys():
				if dict_dict[j][i]:
					if j != i:
						self.new_edge(j, i, dict_dict[j][i])

	def __repr__(self):
		print("Nodes:")
		print(self.graph.keys())
		print("Edges:")
		for i in self.graph.keys():
			print(i + ": " + str(self.importance(i)))
		return "------"

	def new_node(self, name):
		self.graph[name] = {}

	def new_edge(self, from_node, to_node, weight):
		self.graph[to_node][from_node] = weight

	def delete_edge(self, from_node, to_node):
		del self.graph[to_node][from_node]

	def delete_node(self, name):
		del self.graph[name]
		for i in self.graph.keys():
			del self.graph[i][name]

	def importance(self, name):
		counter = 0
		for i in self.graph[name].keys():
			counter += i
		return counter