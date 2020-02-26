# imports
import movie_recommendation as mr
import recommendation_engine as re
import insurance_recommendation as ir
import rule_miner as rm
import form_nn
import datetime
import cold_start_recommender as csr

from insurance_recommendation import *


if __name__ == "__main__":

    df, first_form_index = run_data_preprocessing_pipeline()

    # df1, first_form_index1 = run_data_preprocessing_pipeline_apyoi()

    # rm.get_rules(df, first_form_index, first_form_index+1)

    # print("\n\n\nPOCEO ANN: " + str(datetime.datetime.now()))
    # # Train the ANN
    # form_nn.run_training_for_all_forms(df, first_form_index)
    # print("\n\n\nGOTOV ANN: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO FPG: " + str(datetime.datetime.now()))
    # # Run FP Growth
    # rm.find_all_rules(df, first_form_index, algo='fpg')
    # print("\n\n\nGOTOV FPG: " + str(datetime.datetime.now()))
    #
    # print("\n\n\nPOCEO APRIORI: " + str(datetime.datetime.now()))
    # # Run apriori
    # rm.find_all_rules(df, first_form_index, algo='apriori')
    # print("\n\n\nGOTOV APRIORI: " + str(datetime.datetime.now()))


    print("\n\n\nPOCEO RECOMMENDATION: " + str(datetime.datetime.now()))
    # Run cold start recommender
    rec_forms = csr.find_all_forms(df, 'fpg', ['General Aggregate Coverage Limits',
                                                               'Occurrence: General Liability'], first_form_index)
    print("\n\n\nGOTOV RECOMMENDATION: " + str(datetime.datetime.now()))
    print(rec_forms)
