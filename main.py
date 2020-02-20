# imports

import movie_recommendation as mr
import recommendation_engine as re
import insurance_recommendation as ir


if __name__ == "__main__":
    print("INITIAL")

    print("\n\nMOVIE RECOMMENDATIONS BASED ON SCORE")
    mr.score_based_recommender(mr.load_clean_rank_dataset()[0])
    
    print("\n\nMOVIE RECOMMENDATIONS BASED ON DESCRIPTION, TF-IFD")
    mr.description_based_recommender(mr.load_clean_rank_dataset()[1])

    # print("\n\nPRE DATASET")
    # re.load_data()

    print("INSURANCE DATASET")
    ir.load_and_drop_data('data/BC - AI ORIGINAL.csv')
