# imports

import movie_recommendation as mr
import recommendation_engine as re
import insurance_recommendation as ir

from insurance_recommendation import *


def main():

    file_name = 'data/BC - AI ORIGINAL.csv'

    df = load_and_drop_data(file_name)

    df = decompose_columns(df)


    df.to_csv('data/cleansed.csv', index=False)


if __name__ == "__main__":
    # print("INITIAL")

    # print("\n\nMOVIE RECOMMENDATIONS BASED ON SCORE")
    # mr.score_based_recommender(mr.load_clean_rank_dataset()[0])
    
    # print("\n\nMOVIE RECOMMENDATIONS BASED ON DESCRIPTION, TF-IFD")
    # mr.description_based_recommender(mr.load_clean_rank_dataset()[1])

    # # print("\n\nPRE DATASET")
    # # re.load_data()

    # print("INSURANCE DATASET")
    # ir.load_and_drop_data('data/BC - AI ORIGINAL.csv')

    main()