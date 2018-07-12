# Generic Imports
from collections import defaultdict
import math

# tf function
def tf(dict_dict):
	tf_values = defaultdict(lambda:0)
	for i in dict_dict.keys():
		for j in dict_dict[i].keys():
			tf_values[j] += dict_dict[i][j]
	return tf_values

# idf function
def idf(dict_dict):
	idf_values = defaultdict(lambda:0)
	for i in dict_dict.keys():
		for j in dict_dict[i].keys():
			idf_values[j] += 1
	listlength = len(dict_dict.keys())
	for i in idf_values.keys():
		idf_values[i] = math.log(listlength / (idf_values[i] + 1))
	return idf_values

# tfidf function
def tfidf(pd_df):
	dict_dict = {}
	for i in pd_df.index:
		dict_dict[i] = {}
		for j in pd_df.columns:
			if int(pd_df.loc[i, j]):
				dict_dict[i][j] = int(pd_df.loc[i, j])

	tfidf_values = defaultdict(lambda:0)
	tf_val = tf(dict_dict)
	idf_val = idf(dict_dict)
	for i in tf_val.keys():
		tfidf_values[i] = tf_val[i] * idf_val[i]
	return tfidf_values