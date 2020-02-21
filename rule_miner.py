# import
from apyori import apriori

def get_rules(df, first_form_ind):
    print(df)
    all_recs = df.values.tolist()

    # test = []
    # for index, row in df.iterrows():
    #     arr = []
    #
    #     for col in df.columns:
    #         arr.append(row[col])
    #         if col == 'InsuredState_CA':
    #             break
    #     test.append(arr)
    #
    # print(test)
    # for i in range(first_form_ind):
    #     print(" ")

    association_rules = apriori(all_recs)
    association_results = list(association_rules)

    print(all_recs)
    print(association_results)

    # for item in association_results:
    #     # first index of the inner list
    #     # Contains base item and add item
    #     pair = item[0]
    #     items = [x for x in pair]
    #     print("Rule: " + str(items[0]) + " -> " + str(items[1]))
    #
    #     # second index of the inner list
    #     print("Support: " + str(item[1]))
    #
    #     # third index of the list located at 0th
    #     # of the third index of the inner list
    #
    #     print("Confidence: " + str(item[2][0][2]))
    #     print("Lift: " + str(item[2][0][3]))
    #     print("=====================================")
