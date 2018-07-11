# Generic Imports
from collections import defaultdict
import math
import pandas as pd
import numpy as np

def tfidf_df(someData):
	word_occurences = defaultdict(lambda:0)
	