# imports
import pandas as pd


class Recommender_bot():

    def __init__(self):
        pass


    # Finds all forms based on rules from selected algorithm
    def find_all_forms(self, df, algo, columns, first_form_index):
        # columns contains names of all columns whose values are True(1)
        all_forms_cols = df.columns[first_form_index:]

        # dict where key is form name and value is summed up confidence from all occurrences in rules
        confidence_dict = {}
        for col in all_forms_cols:
            flag, confidence_sum = self.checks_given_form(col, algo, columns)
            if flag:
                confidence_dict[col] = confidence_sum

        return confidence_dict


    # checks if given form is suitable
    def checks_given_form(self, form_name, algo, columns):
        # columns contains names of all columns whose values are True(1)

        if algo == 'apriori':
            df = pd.read_csv(f"models/apriori/{form_name}/relevant.csv", delimiter=',')
        elif algo == 'fpg':
            df = pd.read_csv(f"models/fp_growth/{form_name}/relevant.csv", delimiter=',')
        else:
            print("INVALID ALGORITHM")
            exit(1)

        confidence_sum = 0
        for ind, row in df.iterrows():
            if form_name in row[1]:
                # DO CHECKING
                flag, confidence = self.check_if_form_is_suitable(row, form_name)
                if flag:
                    confidence_sum += confidence

        return flag, confidence_sum


    def check_if_form_is_suitable(self, row, form_name, columns):
        print(row)

        flag_ok = True
        for wanted_column in columns:
            if wanted_column not in row[1]:
                flag_ok = False
                return flag_ok, 0

        conf = 0
        # ovde se nalaze confidence
        row[5]

        location_counter = 0
        for el in row[1]:
            if el == form_name:
                break
            location_counter += location_counter

        conf = row[5][location_counter]

        return flag_ok, conf