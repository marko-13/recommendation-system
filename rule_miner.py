# import
from apyori import apriori
import pickle


def get_rules(df, first_form_ind, target_form_ind):

    all_recs = df.values.tolist()
    print(df)
    print("\n\n\n\n")

    # extract column names where ones are located in df for each row
    mother_list = []
    for index, row in df.iterrows():
        child_list = []
        col_ind = 0
        for el in row:
            if col_ind == first_form_ind:
                break
            if el == 1:
                child_list.append(df.columns[col_ind])

            col_ind += 1
        print(df.iloc[index])
        if df.iloc[index, :][df.columns[target_form_ind]] == 1:
            child_list.append(df.columns[target_form_ind])

        mother_list.append(child_list)

    association_rules = apriori(mother_list, min_support=0.02, min_confidence=0.8, max_length=20, min_lift=0)
    association_results = list(association_rules)

    with open('log/rules_f1.pickle', 'wb') as f:
        pickle.dump(association_results, f)

    # print(all_recs)
    print(len(association_results))
    for i in range (5):
        print(association_results[i])
