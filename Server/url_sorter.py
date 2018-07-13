from collections import defaultdict

from graph import Graph

def sort_urls(list_dict):
	dict_dict = defaultdict(lambda:0)
	for i in list_dict.keys():
		dict_dict[i] = defaultdict(lambda:0)
		for j in list_dict[i]:
			dict_dict[i][j] += 1
	grapher = Graph(dict_dict)
	print(grapher)