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
    # df = dataframe
    km = KMeans(n_clusters=5)
    km.fit(mat)
    # df['cluster'] = km.fit_predict(dataframe)
    # df = df.sort_values("cluster")
    cluster_numbers = km.fit_predict(dataframe)
    cluster_dict = {}
    df_sites = dataframe.index.values
    for site in range(len(cluster_numbers)):
        cluster_dict[df_sites[site]] = cluster_numbers[site]
    return cluster_dict

if __name__ == "__main__":
	print(KMeans_Generator(3, scraper_df("sgcodecampus")))



    