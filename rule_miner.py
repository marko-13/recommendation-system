# import
import pickle
import os
import pandas as pd
import numpy as np
import datetime

import sklearn
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier


from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import apriori
import mlxtend


def find_all_rules(df, first_form_index, algo):
    all_forms_cols = df.columns[first_form_index:]
    counter = 0
    for col in all_forms_cols:
        print(f'[{algo}] - Finding rules for: {col}')
        if algo == 'apriori':
            run_apriori(df, first_form_index, first_form_index + counter)
        elif algo == 'apriori_item_based':
            run_apriori_item_based(df, first_form_index, first_form_index + counter)
        elif algo == 'fpg':
            run_fp_growth(df, first_form_index, first_form_index + counter)
        elif algo == 'fpg_item_based':
            run_fp_growth_item_based(df, first_form_index, first_form_index + counter)
        elif algo == 'random_forest':
            try:
                # PASS BY REFERENCE: kopirati df pre prosledjivanja, to je bio bag...
                run_random_forest(df.copy(), first_form_index, first_form_index + counter)
            except ValueError as e:
                print(f'[ValueError] {e}')
        else:
            print("INVALID ALGORITHM NAME")
            exit(1)
        # print(df.columns[first_form_index + counter])
        counter += 1


def run_apriori_item_based(df, first_form_index, target_form_ind):
    input_columns = df.columns[first_form_index:]
    input_df = df[input_columns]
    label_col_name = df.columns[target_form_ind]

    res_df = apriori(input_df, min_support=0.8, use_colnames=True, max_len=4, verbose=0)
    res_df = mlxtend.frequent_patterns.association_rules(res_df)

    _save_rules(res_df, label_col_name, 'all', algo='apriori_item_based')

    res_df = extract_relevant_itemsets(res_df, label_col_name)

    _save_rules(res_df, label_col_name, 'relevant', algo='apriori_item_based')
    print("\n\n\n ZAVRSIO PRAVILA ZA FORMU " + str(label_col_name) + "    " + str(datetime.datetime.now()))


def run_fp_growth_item_based(df, first_form_index, target_form_ind):

    input_columns = df.columns[first_form_index:]
    input_df = df[input_columns]
    label_col_name = df.columns[target_form_ind]

    res_df = fpgrowth(input_df, min_support=0.8, use_colnames=True, max_len=4, verbose=0)
    res_df = mlxtend.frequent_patterns.association_rules(res_df)

    _save_rules(res_df, label_col_name, 'all', algo='fpg_item_based')

    res_df = extract_relevant_itemsets(res_df, label_col_name)

    _save_rules(res_df, label_col_name, 'relevant', algo='fpg_item_based')
    print("\n\n\n ZAVRSIO PRAVILA ZA FORMU " + str(label_col_name) + "    " + str(datetime.datetime.now()))


def run_apriori(df, first_form_index, target_form_ind):
    input_columns = df.columns[:first_form_index]

    input_df = df[input_columns]

    label_col_name = df.columns[target_form_ind]

    input_df[label_col_name] = df[label_col_name]

    res_df = apriori(input_df, min_support=0.6, use_colnames=True, max_len=16, verbose=0)
    res_df = mlxtend.frequent_patterns.association_rules(res_df)

    _save_rules(res_df, label_col_name, 'all', algo='apriori')

    res_df = extract_relevant_itemsets(res_df, label_col_name)

    _save_rules(res_df, label_col_name, 'relevant', algo='apriori')


def run_fp_growth(df, first_form_ind, target_form_ind):
    '''
    The fpgrowth function expects data in a one-hot encoded 
    pandas DataFrame.
    '''

    # Extract input data into a seperate dataframe
    input_columns = df.columns[:first_form_ind]
    
    input_df = df[input_columns]

    # Get the label column from the original dataframe
    label_col_name = df.columns[target_form_ind]

    # Append the target column to the input dataframe
    input_df[label_col_name] = df[label_col_name]
    # input_df[label_col_name] = df[label_col_name].values

    # Run FP Growth
    res_df = fpgrowth(input_df, min_support=0.6, use_colnames=True, max_len=16, verbose=0)

    res_df = mlxtend.frequent_patterns.association_rules(res_df)
    # for ind, r in res_df.iterrows():
    #     print(r)

    # Save all the rules found
    # res_df.to_csv(f'log/fp_growth_{label_col_name}_all.csv')
    _save_rules(res_df, label_col_name, 'all', algo='fpg')

    # Extract relevant rules
    res_df = extract_relevant_itemsets(res_df, label_col_name)

    # Save only the relevant rules
    # res_df.to_csv(f'log/fp_growth_{label_col_name}_relevant.csv')
    _save_rules(res_df, label_col_name, 'relevant', algo='fpg')
    

def run_random_forest(df, first_form_ind, target_form_ind):

    feature_cols = df.columns[:first_form_ind].tolist()

    df = df[feature_cols + [df.columns.tolist()[target_form_ind]]]

    features = df.columns[:-1]

    class_feature = df.columns[-1]

    clf = RandomForestClassifier(n_jobs=2, random_state=0)

    class_vals = np.array(df[class_feature].tolist())

    clf.fit(df[features].values, class_vals)

    form_name = df.columns.tolist()[-1]

    _save_rules(df, form_name, "", 'random_forest', clf)


def extract_relevant_itemsets(rules_df, form_name):
    '''
    Extracts rules that contain the form occurence
    from the FP growth results dataframe. 
    '''
    rel_rows = []
    for index, row in rules_df.iterrows():
        # print(row[1])
        if form_name in row[1]:
            # print(form_name)
            # print(row[1])
            rel_rows.append(row)

    return pd.DataFrame(rel_rows)


def _save_rules(df, form_name, file_name, algo, obj_to_save=None):
    if not os.path.exists('models'):
        os.mkdir('models')

    if algo == 'fpg':
        if not os.path.exists('models/fp_growth'):
            os.mkdir('models/fp_growth')

        if not os.path.exists(f'models/fp_growth/{form_name}'):
            os.mkdir(f'models/fp_growth/{form_name}')

        df.to_csv(f'models/fp_growth/{form_name}/{file_name}.csv')

    elif algo == 'fpg_item_based':
        if not os.path.exists('models/fpg_item_based'):
            os.mkdir('models/fpg_item_based')

        if not os.path.exists(f'models/fpg_item_based/{form_name}'):
            os.mkdir(f'models/fpg_item_based/{form_name}')

        df.to_csv(f'models/fpg_item_based/{form_name}/{file_name}.csv')

    elif algo == 'apriori':
        if not os.path.exists('models/apriori'):
            os.mkdir('models/apriori')

        if not os.path.exists(f'models/apriori/{form_name}'):
            os.mkdir(f'models/apriori/{form_name}')

        df.to_csv(f'models/apriori/{form_name}/{file_name}.csv')

    elif algo == 'apriori_item_based':
        if not os.path.exists('models/apriori_item_based'):
            os.mkdir('models/apriori_item_based')

        if not os.path.exists(f'models/apriori_item_based/{form_name}'):
            os.mkdir(f'models/apriori_item_based/{form_name}')

        df.to_csv(f'models/apriori_item_based/{form_name}/{file_name}.csv')

    elif algo == 'random_forest':
        if not os.path.exists('models/random_forest'):
            os.mkdir('models/random_forest')

        if not os.path.exists(f'models/random_forest/{form_name}'):
            os.mkdir(f'models/random_forest/{form_name}')

        if obj_to_save:
            with open(f'models/random_forest/{form_name}/r_forest.pickle', 'wb') as f:
                pickle.dump(obj_to_save, f)

    else:
        print("Could not save rules")
        exit(1)
