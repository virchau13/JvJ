import pandas as pd
import sklearn
import numpy as np
import matplotlib as plt

import sys
import os

sys.path.append(os.path.abspath("./scraper"))
from wordfilter import scraper, scraper_df
from sklearn.cluster import KMeans

def KMeans_Generator(clusters, dataframe):
    mat = dataframe.values
    km = KMeans(n_clusters=3)
    km.fit(mat)
    
    return km

if __name__ == "__main__":
	print(KMeans_Generator(3, scraper_df("sgcodecampus")).labels_)