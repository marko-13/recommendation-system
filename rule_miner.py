# import
import pickle
import os
import pandas as pd

from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import apriori
import mlxtend

# def get_rules(df, first_form_ind, target_form_ind):

#     all_recs = df.values.tolist()
#     print(df)
#     print("\n\n\n\n")

#     # extract column names where ones are located in df for each row
#     mother_list = []
#     for index, row in df.iterrows():
#         child_list = []
#         col_ind = 0
#         for el in row:
#             if col_ind == first_form_ind:
#                 break
#             if el == 1:
#                 child_list.append(df.columns[col_ind])

#             col_ind += 1
#         print(df.iloc[index])
#         if df.iloc[index, :][df.columns[target_form_ind]] == 1:
#             child_list.append(df.columns[target_form_ind])

#         mother_list.append(child_list)

#     association_rules = apriori(mother_list, min_support=0.02, min_confidence=0.8, max_length=None, min_lift=0)
#     association_results = list(association_rules)

#     with open('log/rules_f1.pickle', 'wb') as f:
#         pickle.dump(association_results, f)

#     # print(all_recs)
#     print(len(association_results))
#     for i in range (5):
#         print(association_results[i])


def find_all_rules(df, first_form_index, algo):
    all_forms_cols = df.columns[first_form_index:]
    counter = 0
    for col in all_forms_cols:
        if algo == 'apriori':
            run_apriori(df, first_form_index, first_form_index + counter)
        elif algo == 'fpg':
            run_fp_growth(df, first_form_index, first_form_index + counter)
        else:
            print("INVALID ALGORITHM NAME")
            exit(1)
        # print(df.columns[first_form_index + counter])
        counter += 1


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


def _save_rules(df, form_name, file_name, algo):
    if not os.path.exists('models'):
        os.mkdir('models')

    if algo == 'fpg':
        if not os.path.exists('models/fp_growth'):
            os.mkdir('models/fp_growth')

        if not os.path.exists(f'models/fp_growth/{form_name}'):
            os.mkdir(f'models/fp_growth/{form_name}')

        df.to_csv(f'models/fp_growth/{form_name}/{file_name}.csv')

    elif algo == 'apriori':
        if not os.path.exists('models/apriori'):
            os.mkdir('models/apriori')

        if not os.path.exists(f'models/apriori/{form_name}'):
            os.mkdir(f'models/apriori/{form_name}')

        df.to_csv(f'models/apriori/{form_name}/{file_name}.csv')

    else:
        print("Could not save rules")
        exit(1)
