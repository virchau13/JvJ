# Generic Imports
from collections import defaultdict
import math
import numpy as np
import pandas as pd

from kmeans import KMeans_Generator

def tfidf_df(sameData):
	kmeans_stuff = KMeans_Generator(3, sameData)
	collected = {}
	count = 0
	for i in sameData.index:
		count += 1
		collected[i]["data"] = {}
		for j in sameData.columns:
			if int(sameData.loc[i, j]):
				collected[i]["data"][j] = int(sameData.loc[i, j])
		collected[i]["cluster"] = kmeans_stuff[i]
		collected[i]["initialRanking"] = count
	return collected