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

    # Need non-decomposed columns for random forest
    df_non_decomposed, first_form_index = run_data_preprocessing_pipeline_apyoi()

    # FIND RULES FOR RANDOM FOREST

    rm.find_all_rules(df_non_decomposed, first_form_index, 'random_forest')

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

    # ============
    # MAIN PROGRAM
    # ============

    # bot = csr.Recommender_bot(df, first_form_index)
    # selected_cols = bot.console_user_input()
    # print(selected_cols)

    # selected_cols = ['BusinessSegment_Naughton Motorsports', 'Type_New', 'InsuredState_LA', 'BrokerCompany_Socius Insurance Services, Inc.', 'BrokerState_MO', 'UnderwriterTeam_Brokerage Casualty - SouthEast', 'BusinessClassification_53374 Food Products Mfg. - dry', 'Occurrence: Owners & Contractors Protective', 'Limit Damage to Premises Rented to You', 'Each Common Cause Liquor Liability', 'Other', 'Terrorism']


    # print("\n\n\nPOCEO RECOMMENDATION FPG: " + str(datetime.datetime.now()))
    # # Run cold start recommender
    # rec_forms = csr.find_all_forms(df, 'fpg', selected_cols, first_form_index)
    # print("GOTOV RECOMMENDATION FPG: " + str(datetime.datetime.now()))
    # print(rec_forms)

    # print("\n\n\nPOCEO RECOMMENDATION APRIORI: " + str(datetime.datetime.now()))
    # # Run cold start recommender
    # rec_forms = csr.find_all_forms(df, 'apriori', selected_cols, first_form_index)
    # print("GOTOV RECOMMENDATION APRIORI: " + str(datetime.datetime.now()))
    # print(rec_forms)

    # print("\n\n\nPOCEO RECOMMENDATION ANN: " + str(datetime.datetime.now()))
    # # Run cold start recommender
    # rec_forms = csr.find_all_forms(df, 'ann', selected_cols, first_form_index)
    # print("GOTOV RECOMMENDATION ANN: " + str(datetime.datetime.now()))
    # print(rec_forms)

    # ============
    #   END MAIN
    # ============

    # Hardcoded NN test:

    # input_cols = ['BusinessSegment_Naughton Motorsports', 'Type_New', 'InsuredState_LA', 'BrokerCompany_Socius Insurance Services, Inc.', 'BrokerState_MO', 'UnderwriterTeam_Brokerage Casualty - SouthEast', 'BusinessClassification_53374 Food Products Mfg. - dry', 'Occurrence: Owners & Contractors Protective', 'Limit Damage to Premises Rented to You', 'Each Common Cause Liquor Liability', 'Other', 'Terrorism']
    # top_recommendation_by_fpg = 'MPIL 1083 04 15'

    # nn = form_nn.construct_nn(first_form_index, top_recommendation_by_fpg)
    # nn = form_nn.load_nn(nn)

    # input_vec = form_nn.column_names_to_vector(df, input_cols, first_form_index)

    # input_vec = np.array([input_vec])

    # print(input_vec.shape)

    # print(nn.predict(input_vec))