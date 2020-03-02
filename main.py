# imports
import movie_recommendation as mr
import recommendation_engine as re
import insurance_recommendation as ir
import rule_miner as rm
import form_nn
import datetime
import cold_start_recommender as csr
from insurance_recommendation import *
import os
import pickle
import numpy as np

def give_all_predictions(df, first_form_index, user_input):
    
    all_forms = df.columns[first_form_index:].tolist()

    for form in all_forms:

        print('\n\n\n===============')
        print(form)
        print('===============')

        # ANN prediction
        nn = form_nn.construct_nn(first_form_index, form)
        nn = form_nn.load_nn(nn)
        input_vec = form_nn.column_names_to_vector(df, user_input, first_form_index)
        input_vec = np.array([input_vec])
        ann_pred = nn.predict(input_vec)
        print(f"[ANN] - {ann_pred}")

        # Apriori
        flag, apriori_conf = csr.checks_given_form(form, 'apriori', user_input)
        print(f'[APRIORI] - {apriori_conf}')

        # FP Growth
        flag, fpg_conf = csr.checks_given_form(form, 'fpg', user_input)
        print(f'[FP GROWTH] - {fpg_conf}')

        # Random forest prediction
        input_vec = csr._create_vector_for_random_forest(df.columns[:first_form_index].tolist(), user_input)
        rf_pred = csr.random_forest_predict(input_vec, form)
        print(f'[RANDOM FOREST] - {rf_pred}')


def move_me_pls(df, first_form_index, target_form_index, user_input):
    import lime
    import lime.lime_tabular
    feature_names = df.columns.tolist()[:first_form_index]
    
    target_form_name = df.columns.tolist()[target_form_index]

    with open(f'models/random_forest/{target_form_name}/r_forest.pickle', 'rb') as f:
        clf = pickle.load(f)

        print(type(df[feature_names].values))
        explainer = lime.lime_tabular.LimeTabularExplainer(df[feature_names].values, feature_names=feature_names, class_names=['False, True'], discretize_continuous=True)

        input_vec = form_nn.column_names_to_vector(df, user_input, first_form_index)

        exp = explainer.explain_instance(np.array(input_vec), clf.predict_proba, num_features=2, top_labels=1)

        print(exp)



if __name__ == "__main__":

    df, first_form_index = run_data_preprocessing_pipeline()


    # print("\n\n\nPOCEO ANN: " + str(datetime.datetime.now()))
    # # Train the ANN
    # form_nn.run_training_for_all_forms(df, first_form_index)
    # print("\n\n\nGOTOV ANN: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO FPG: " + str(datetime.datetime.now()))
    # # Run FP Growth
    # rm.find_all_rules(df, first_form_index, algo='fpg')
    # print("\n\n\nGOTOV FPG: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO APRIORI: " + str(datetime.datetime.now()))
    # # Run apriori
    # rm.find_all_rules(df, first_form_index, algo='apriori')
    # print("\n\n\nGOTOV APRIORI: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO RANDOM FOREST: " + str(datetime.datetime.now()))
    # # Run random forest
    # rm.find_all_rules(df, first_form_index, 'random_forest')
    # print("\n\n\nGOTOV RANDOM FOREST: " + str(datetime.datetime.now()))


    # bot = csr.Recommender_bot(df, first_form_index)
    # # selected_cols = bot.console_user_input()
    selected_cols = ['BusinessSegment_Naughton Motorsports', 'Type_New', 'InsuredState_LA', 'BrokerCompany_Socius Insurance Services, Inc.', 'BrokerState_MO', 'UnderwriterTeam_Brokerage Casualty - SouthEast', 'BusinessClassification_53374 Food Products Mfg. - dry', 'Occurrence: Owners & Contractors Protective', 'Limit Damage to Premises Rented to You', 'Each Common Cause Liquor Liability', 'Other', 'Terrorism']
    # give_all_predictions(df, first_form_index, selected_cols)

    move_me_pls(df, first_form_index, first_form_index, selected_cols)
