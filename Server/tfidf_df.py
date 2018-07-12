# Generic Imports
from collections import defaultdict
import math
import numpy as np
import pandas as pd

def tfidf_df(sameData):
	collected = {}
	for i in sameData.index:
		collected[i] = {}
		for j in sameData.columns:
			collected[i][j] = int(sameData.loc[i, j])
	return collected