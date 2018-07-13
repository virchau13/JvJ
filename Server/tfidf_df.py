# Generic Imports
from collections import defaultdict
from functools import reduce
import math
import numpy as np
import pandas as pd

from kmeans import KMeans_Generator

def tfidf_df(sameData, queryer):
	kmeans_stuff = KMeans_Generator(3, sameData)
	collected = defaultdict(lambda:0)
	count = 0
	for i in sameData.index:
		count += 1
		collected[i] = defaultdict(lambda:0)
		collected[i]["data"] = defaultdict(lambda:0)
		for j in sameData.columns:
			if int(sameData.loc[i, j]):
				collected[i]["data"][j] = int(sameData.loc[i, j])
		collected[i]["cluster"] = int(kmeans_stuff[i])
		collected[i]["importance"] = count
	return collected