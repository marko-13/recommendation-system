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


    # bot = csr.Recommender_bot(df, first_form_index)
    # selected_cols = bot.console_user_input()
    # print(selected_cols)
    selected_cols = ['BusinessSegment_Naughton Amusement', 'Type_Renewal', 'InsuredState_WI', 'BrokerCompany_AmWINS Access Insurance Services, LLC', 'BrokerState_OH', 'UnderwriterTeam_Brokerage Casualty - SouthEast', 'BusinessClassification_91581 Contractors - subcontracted work - in connection with construction, reconstruction, erection or repair - not buildings', 'Occurrence: General Liability', 'Limit Damage to Premises Rented to You', 'Limit Products / Completed Operations Aggregate', 'Limit Personal / Advertising Injury', 'Limit Per Project Aggregate', 'Limit Per Location Aggregate', 'Hired / Non-Owned Auto Liability', 'Other', 'Terrorism']

    print("\n\n\nPOCEO RECOMMENDATION FPG: " + str(datetime.datetime.now()))
    # Run cold start recommender
    rec_forms = csr.find_all_forms(df, 'fpg', selected_cols, first_form_index)
    print("\n\n\nGOTOV RECOMMENDATION FPG: " + str(datetime.datetime.now()))
    print(rec_forms)

    print("\n\n\nPOCEO RECOMMENDATION APRIORI: " + str(datetime.datetime.now()))
    # Run cold start recommender
    rec_forms = csr.find_all_forms(df, 'apriori', selected_cols, first_form_index)
    print("\n\n\nGOTOV RECOMMENDATION APRIORI: " + str(datetime.datetime.now()))
    print(rec_forms)
