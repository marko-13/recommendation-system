# imports

import movie_recommendation as mr
import recommendation_engine as re
import insurance_recommendation as ir

# Importujmo samo sve odmah... 
from insurance_recommendation import *

def main():

    file_name = 'data/BC - AI ORIGINAL.csv'

    df = load_and_drop_data(file_name)

    decomp_columns = [
        'BusinessSegment',
        'Type',
        'InsuredState',
        'BrokerCompany',
        'BrokerState',
        'UnderwriterTeam',
        'BusinessClassification'
        ]

    for col in decomp_columns:
        try:
            print(f'Trying {col}')
            new_cols = decompose_column(df, col)
            df = replace_column_with_decomposed(df, col, new_cols)
        except ValueError:
            print(f'---Failed {col}')
            pass

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