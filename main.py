# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

import movie_recommendation as mr


if __name__ == "__main__":
    print("INITIAL")

    print("\n\nMOVIE RECOMMENDATIONS BASED ON SCORE")
    mr.score_based_recommender(mr.load_clean_rank_dataset()[0])

    print("\n\nMOVIE RECOMMENDATIONS BASED ON DESCRIPTION, TF-IFD")
    mr.description_based_recommender(mr.load_clean_rank_dataset()[1])

    print("\n\nPRE DATASET")
