# imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


def load_clean_rank_dataset():
    movie_credits = pd.read_csv('dataset/tmdb_5000_credits.csv')
    movies_incomplete = pd.read_csv('dataset/tmdb_5000_movies.csv')

    print("Credits shape: ", movie_credits.shape)
    print("Movies incomplete shape: ", movies_incomplete.shape)

    movie_credits_renamed = movie_credits.rename(index=str, columns={"movie_id": "id"})
    movies_dirty = movies_incomplete.merge(movie_credits_renamed, on='id')
    movies_dirty.head()

    movies_clean = movies_dirty.drop(columns=['homepage', 'title_x', 'title_y', 'status', 'production_countries'])
    movies_clean.head()

    # voting based on IMDB formula
    V = movies_clean['vote_count']
    R = movies_clean['vote_average']
    C = movies_clean['vote_average'].mean()
    m = movies_clean['vote_count'].quantile(0.70)

    movies_clean['weighted_average'] = (V / (V + m) * R) + (m / (m + V) * C)

    movies_ranked = movies_clean.sort_values('weighted_average', ascending=False)
    movies_ranked[['original_title', 'vote_count', 'vote_average', 'weighted_average', 'popularity']].head(20)

    print(movies_ranked)
    return  movies_ranked, movies_clean


def score_based_recommender(movies_ranked):
    w_avg = movies_ranked.sort_values('weighted_average', ascending=False)

    plt.figure(figsize=(16, 6))

    ax = sns.barplot(x=w_avg['weighted_average'].head(10), y=w_avg['original_title'].head(10), data=w_avg, palette='deep')

    plt.xlim(6.75, 8.35)
    plt.title('"Best" Movies by TMDB Votes', weight='bold')
    plt.xlabel('Weighted Average Score', weight='bold')
    plt.ylabel('Movie Title', weight='bold')

    plt.savefig('best_movies_by_score.png')

def description_based_recommender(movies_clean):
    tfv = TfidfVectorizer(min_df=3, max_features=None,
                          strip_accents='unicode', analyzer='word', token_pattern=r'\w{1,}',
                          ngram_range=(1, 3), use_idf=1, smooth_idf=1, sublinear_tf=1,
                          stop_words='english')

    # Filling NaNs with empty string
    movies_clean['overview'] = movies_clean['overview'].fillna('')

    # Fitting the TF-IDF on the 'overview' text
    tfv_matrix = tfv.fit_transform(movies_clean['overview'])

    print(tfv_matrix.shape)

    # ----------------------------------------------------------
    # Compute the sigmoid kernel
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)

    # Reverse mapping of indices and movie titles
    indices = pd.Series(movies_clean.index, index=movies_clean['original_title']).drop_duplicates()

    def give_rec(title, sig=sig):
        # Get the index corresponding to original_title
        idx = indices[title]

        # Get the pairwsie similarity scores
        sig_scores = list(enumerate(sig[idx]))

        # Sort the movies
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

        # Scores of the 10 most similar movies
        sig_scores = sig_scores[1:11]

        # Movie indices
        movie_indices = [i[0] for i in sig_scores]

        # Top 10 most similar movies
        return movies_clean['original_title'].iloc[movie_indices]


if __name__ == "__main__":
    print("INITIAL")
    score_based_recommender(load_clean_rank_dataset()[0])
    description_based_recommender(load_clean_rank_dataset()[1])
