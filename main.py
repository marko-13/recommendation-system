# imports

import movie_recommendation as mr
import recommendation_engine as re
import insurance_recommendation as ir
import rule_miner as rm
import form_nn

from insurance_recommendation import *



if __name__ == "__main__":

    df, first_form_index = run_data_preprocessing_pipeline()

    # df1, first_form_index1 = run_data_preprocessing_pipeline_apyoi()

    # rm.get_rules(df, first_form_index, first_form_index+1)

    # Train the ANN
    # form_nn.run_training_for_all_forms(df, first_form_index)

    # Run FP Growth
    rm.run_fp_growth(df, first_form_index, first_form_index + 1)