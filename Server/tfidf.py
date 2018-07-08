# Generic Imports
from collections import defaultdict
import math

# tf function
def tf(dict_list):
	tf_values = defaultdict(lambda:0)
	for i in dict_list:
		for j in i.keys():
			tf_values[j] += i[j]
	return tf_values

# idf function
def idf(dict_list):
	idf_values = defaultdict(lambda:0)
	for i in dict_list:
		for j in i.keys():
			idf_values[j] += 1
	listlength = len(dict_list)
	for i in idf_values.keys():
		idf_values[i] = math.log(listlength / (idf_values[i] + 1))
	return idf_values

# tfidf function
def tfidf(dict_list):
	tfidf_values = defaultdict(lambda:0)
	tf_val = tf(dict_list)
	idf_val = idf(dict_list)
	for i in tf_val.keys():
		tfidf_values[i] = tf_val[i] * idf_val[i]
	return tfidf_values

if __name__ == "__main__":
	thingy = [
		{
			"hi" : 1,
			"bye" : 2,
		},
		{
			"hi" : 3,
			"mine" : 4,
		}
	]
	print(tfidf(thingy))