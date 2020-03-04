# imports
from flask_cors import CORS
from numpy import take

import movie_recommendation as mr
import recommendation_engine as re
import insurance_recommendation as ir
import rule_miner as rm
import form_nn
import form_nn_item_based
import datetime
import cold_start_recommender as csr
import form_based_recommender as fbr

from insurance_recommendation import *
import os
import pickle
import numpy as np

from flask import Flask, request
import flask
from flask import render_template
import json
import math
from itertools import islice
import requests
import urllib.request

app = Flask(__name__)
cors = CORS(app)

df_glob, first_form_index_glob = run_data_preprocessing_pipeline()

forms_glob = []


@app.route("/")
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)


@app.route("/postforms", methods=['POST'])
def get_forms():
    data = request.get_json()
    print(data['x'])

    result_html = ""

    dict_res = give_all_predictions(df_glob, first_form_index_glob, data['x'])
    dict_res = {k: v for k, v in sorted(dict_res.items(), key=lambda item: item[1], reverse=True)}

    list_keys = list(dict_res.keys())
    global forms_glob
    forms_glob = list_keys[:5]
    n_items = []
    message = "Hello"

    return render_template('index.html', message=message)


@app.route("/sendinfo", methods=['GET'])
def send_info():

    print(forms_glob)
    print(flask.jsonify(forms_glob))

    return flask.jsonify(list_of_data=forms_glob)

@app.route("/getbusinesssegmet", methods=['GET'])
def get_business_segment():
    business_seg = []

    file_name = 'data/BC - AI ORIGINAL.csv'
    df = pd.read_csv(file_name, delimiter=',')

    col_to_list = df['BusinessSegment'].tolist()

    for val in col_to_list:
        try:
            if math.isnan(val):
                print(val)
                val = 'nan'
                continue
        except:
            pass
        if val not in business_seg:
            business_seg.append(val)


    print(business_seg)
    print(flask.jsonify(business_seg))

    return flask.jsonify(list_of_data=business_seg)


@app.route("/gettype", methods=['GET'])
def get_type():
    type_l = []

    file_name = 'data/BC - AI ORIGINAL.csv'
    df = pd.read_csv(file_name, delimiter=',')

    col_to_list = df['Type'].tolist()

    for val in col_to_list:
        try:
            if math.isnan(val):
                print(val)
                val = 'nan'
        except:
            pass
        if val not in type_l:
            type_l.append(val)


    print(type_l)
    print(flask.jsonify(type_l))

    return flask.jsonify(list_of_data=type_l)


@app.route("/getinsuredstate", methods=['GET'])
def get_insured_state():
    ins_state = []

    file_name = 'data/BC - AI ORIGINAL.csv'
    df = pd.read_csv(file_name, delimiter=',')

    col_to_list = df['InsuredState'].tolist()

    for val in col_to_list:
        try:
            if math.isnan(val):
                print(val)
                val = 'nan'
        except:
            pass
        if val not in ins_state:
            ins_state.append(val)

    print(ins_state)
    print(flask.jsonify(ins_state))

    return flask.jsonify(list_of_data=ins_state)


@app.route("/getbrokercompany", methods=['GET'])
def get_broker_company():
    broker_c = []

    file_name = 'data/BC - AI ORIGINAL.csv'
    df = pd.read_csv(file_name, delimiter=',')

    col_to_list = df['BrokerCompany'].tolist()

    for val in col_to_list:
        try:
            if math.isnan(val):
                print(val)
                val = 'nan'
        except:
            pass
        if val not in broker_c:
            broker_c.append(val)


    print(broker_c)
    print(flask.jsonify(broker_c))

    return flask.jsonify(list_of_data=broker_c)


@app.route("/getbrokerstate", methods=['GET'])
def get_broker_state():
    broker_s = []

    file_name = 'data/BC - AI ORIGINAL.csv'
    df = pd.read_csv(file_name, delimiter=',')

    col_to_list = df['BrokerState'].tolist()

    for val in col_to_list:
        try:
            if math.isnan(val):
                print(val)
                val = 'nan'
        except:
            pass
        if val not in broker_s:
            broker_s.append(val)


    print(broker_s)
    print(flask.jsonify(broker_s))

    return flask.jsonify(list_of_data=broker_s)


@app.route("/getunderwriterteam", methods=['GET'])
def get_underwriter_team():
    underw_t = []

    file_name = 'data/BC - AI ORIGINAL.csv'
    df = pd.read_csv(file_name, delimiter=',')

    col_to_list = df['UnderwriterTeam'].tolist()

    for val in col_to_list:
        try:
            if math.isnan(val):
                print(val)
                val = 'nan'
        except:
            pass
        if val not in underw_t:
            underw_t.append(val)


    print(underw_t)
    print(flask.jsonify(underw_t))

    return flask.jsonify(list_of_data=underw_t)


@app.route("/getbusinessclassification", methods=['GET'])
def get_business_classification():
    bussines_class = []

    file_name = 'data/BC - AI ORIGINAL.csv'
    df = pd.read_csv(file_name, delimiter=',')

    col_to_list = df['BusinessClassification'].tolist()

    for val in col_to_list:
        try:
            if math.isnan(val):
                print(val)
                val = 'nan'
        except:
            pass
        if val not in bussines_class:
            bussines_class.append(val)


    print(bussines_class)
    print(flask.jsonify(bussines_class))

    return flask.jsonify(list_of_data=bussines_class)


def give_all_predictions(df, first_form_index, user_input):
    
    all_forms = df.columns[first_form_index:].tolist()

    dict_res = {}
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
        # temp_l = float(np.asarray(ann_pred))
        # print(type(temp_l))
        print(f"[ANN(true, false)] = {ann_pred}")

        # Apriori
        flag, apriori_conf = csr.checks_given_form(form, 'apriori', user_input)
        print(f'[APRIORI] = {apriori_conf}')

        # FP Growth
        flag, fpg_conf = csr.checks_given_form(form, 'fpg', user_input)
        print(f'[FP GROWTH] = {fpg_conf}')
        dict_res[form] = fpg_conf

        # Random forest prediction
        input_vec = csr._create_vector_for_random_forest(df.columns[:first_form_index].tolist(), user_input)
        rf_pred = csr.random_forest_predict(input_vec, form)
        print(f'[RANDOM FOREST] = {rf_pred}')

    return dict_res


def give_all_predictions_item_based(df, first_form_index, user_input):
    all_forms = df.columns[first_form_index:].tolist()

    for form in all_forms:
        print('\n\n\n===============')
        print(form + " item based")
        print('===============')
        form_index = df.columns.get_loc(form)


        # # ANN prediction item based
        nn = form_nn_item_based.construct_nn(110, form)
        nn = form_nn_item_based.load_nn(nn)
        input_vec = form_nn_item_based.column_names_to_vector(df, user_input, first_form_index, form_index)
        input_vec = np.array([input_vec])
        ann_pred = nn.predict(input_vec)
        # temp_l = float(np.asarray(ann_pred))
        # print(type(temp_l))
        print(f"[ANN(true, false)] = {ann_pred}")

        # Apriori item based
        flag, apriori_conf = fbr.checks_given_form(form, 'apriori_item_based', user_input)
        print(f'[APRIORI ITEM BASED] = {apriori_conf}')

        # FP Growth
        flag, fpg_conf = fbr.checks_given_form(form, 'fpg_item_based', user_input)
        print(f'[FP GROWTH ITEM BASED] = {fpg_conf}')


def move_me_pls(df, first_form_index, target_form_index, user_input):
    import lime.lime_tabular
    feature_names = df.columns.tolist()[:first_form_index]
    
    target_form_name = df.columns.tolist()[target_form_index]

    nn = form_nn.construct_nn(first_form_index, target_form_name)
    nn = form_nn.load_nn(nn)
    nn = form_nn.load_nn(nn)

    print(type(df[feature_names].values))
    explainer = lime.lime_tabular.LimeTabularExplainer(df[feature_names].values, feature_names=feature_names, class_names=['True', 'False'], discretize_continuous=True)

    input_vec = form_nn.column_names_to_vector(df, user_input, first_form_index)

    exp = explainer.explain_instance(np.array(input_vec), nn.predict_proba, num_features=2, top_labels=1)

    print(exp)


if __name__ == "__main__":

    df, first_form_index = run_data_preprocessing_pipeline()

    app.run(debug=True)

    # ------------------------------------------------------------------------------------------------------------------
    # TRAIN MODELS AND GET RULES FUNCTIONS

    # print("\n\n\nPOCEO ANN: " + str(datetime.datetime.now()))
    # # Train the ANN
    # form_nn.run_training_for_all_forms(df, first_form_index)
    # print("\n\n\nGOTOV ANN: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO ANN ITEM BASED: " + str(datetime.datetime.now()))
    # # Train the ANN item based
    # form_nn_item_based.run_training_for_all_forms(df, first_form_index)
    # print("\n\n\nGOTOV ANN ITEM BASED: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO FPG: " + str(datetime.datetime.now()))
    # # Run FP Growth
    # rm.find_all_rules(df, first_form_index, algo='fpg')
    # print("\n\n\nGOTOV FPG: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO FPG ITEM BASED: " + str(datetime.datetime.now()))
    # # Run FP Growth item based
    # rm.find_all_rules(df, first_form_index, algo='fpg_item_based')
    # print("\n\n\nGOTOV FPG ITEM BASED: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO APRIORI: " + str(datetime.datetime.now()))
    # # Run apriori
    # rm.find_all_rules(df, first_form_index, algo='apriori')
    # print("\n\n\nGOTOV APRIORI: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO APRIORI ITEM BASED: " + str(datetime.datetime.now()))
    # # Run apriori
    # rm.find_all_rules(df, first_form_index, algo='apriori_item_based')
    # print("\n\n\nGOTOV APRIORI ITEM BASED: " + str(datetime.datetime.now()))

    # print("\n\n\nPOCEO RANDOM FOREST: " + str(datetime.datetime.now()))
    # # Run random forest
    # rm.find_all_rules(df, first_form_index, 'random_forest')
    # print("\n\n\nGOTOV RANDOM FOREST: " + str(datetime.datetime.now()))

    # ------------------------------------------------------------------------------------------------------------------
    # COLD START FUNCTIONS
    # bot = csr.Recommender_bot(df, first_form_index)
    # selected_cols = bot.console_user_input()
    # selected_cols = ['BusinessSegment_Naughton Motorsports', 'Type_New', 'InsuredState_LA', 'BrokerCompany_Socius Insurance Services, Inc.', 'BrokerState_MO', 'UnderwriterTeam_Brokerage Casualty - SouthEast', 'BusinessClassification_53374 Food Products Mfg. - dry', 'Occurrence: Owners & Contractors Protective', 'Limit Damage to Premises Rented to You', 'Each Common Cause Liquor Liability', 'Other', 'Terrorism']
    # dict_res = give_all_predictions(df, first_form_index, selected_cols)

    # ------------------------------------------------------------------------------------------------------------------
    # ITEM BASED FUNCTIONS
    # bot_item_based = fbr.Recommender_bot_item_based(df, first_form_index)
    # selected_cols_item_based = bot_item_based.console_user_input()
    # selected_cols_item_based = ['MJIL 1000 08 10', 'MDIL 1001 08 11', 'MEIL 1225 10 11']
    # give_all_predictions_item_based(df, first_form_index, selected_cols_item_based)

    # ------------------------------------------------------------------------------------------------------------------
    # LIME EXPLANATION FUNCTION
    # move_me_pls(df, first_form_index, first_form_index, selected_cols)




