# imports
import pandas as pd


class Recommender_bot():

    def __init__(self, df, first_form_index):
        
        user_input_columns = df.columns[:first_form_index]

        print(len(user_input_columns))

        # Group input data columns:

        self.user_input_fields = {}
        ind_of_last_decomposed_col = -1

        for index, col in enumerate(user_input_columns):

            if len(col.split('_')) == 1:
                ind_of_last_decomposed_col = index
                break

            col_type = col.split('_')[0]

            # If the column type is already in the dict,
            # skip it
            if col_type in self.user_input_fields:
                continue

            # print(f"Creating entry for {col_type}")

            self.user_input_fields[col_type] = []

            for curr_col in user_input_columns:

                # print(f'{curr_col}')

                if not curr_col.startswith(col_type):
                    continue

                col_type_option = curr_col.split('_')[1]

                # print(f'--- INSERTING {col_type_option}')
                
                # print(f'----- APPENDING with {col_type}:{col_type_option}')
                option_list = self.user_input_fields[col_type]
                # print(type(option_list))
                # print(option_list)
                self.user_input_fields[col_type].append(col_type_option)

        # Insert non-decomposed columns into the dict
        for col in user_input_columns[ind_of_last_decomposed_col:]:
            self.user_input_fields[col] = ["False", "True"]

        for k, v in self.user_input_fields.items():
            print(f'{k} -> []')

    def input_cold_start(self):
        pass        

    def console_user_input(self):
        '''
        Presents the user with a series of questions. Marks the column names which
        he selected and returns them.
        '''
        print("==============\nPlease fill in the form:")

        true_columns = []

        for form_field in self.user_input_fields:
            user_input = -1
            while user_input == -1 or user_input >= len(self.user_input_fields[form_field]):

                print(f'--- Select option for {form_field}')

                for index, option in enumerate(self.user_input_fields[form_field]):
                    print(f'[{index}] - {option}')

                user_input = int(input())
            
            if self.user_input_fields[form_field] == ["False", "True"]:
                # If it's a true/false column
                if user_input == 1:
                    true_columns.append(form_field)
            else:
                # If it's a multiple choice column
                col_name = form_field + "_" + self.user_input_fields[form_field][user_input]
                true_columns.append(col_name)
        
        print("========\nUser selection:")
        print(true_columns)

        return true_columns


# ---------------------------------------------------------------FUNS---------------------------------------------------


# Finds all forms based on rules from selected algorithm
def find_all_forms(df, algo, columns, first_form_index):
    # columns contains names of all columns whose values are True(1)
    all_forms_cols = df.columns[first_form_index:]

    # dict where key is form name and value is summed up confidence from all occurrences in rules
    confidence_dict = {}
    for col in all_forms_cols:
        flag, confidence_sum = checks_given_form(col, algo, columns)
        if flag:
            confidence_dict[col] = confidence_sum

    confidence_dict = {k: v for k, v in sorted(confidence_dict.items(), key=lambda item: item[1], reverse=True)}
    return confidence_dict


# checks if given form is suitable
def checks_given_form(form_name, algo, columns):
    # columns contains names of all columns whose values are True(1)

    if algo == 'apriori':
        df = pd.read_csv(f"models/apriori/{form_name}/relevant.csv", delimiter=',')
    elif algo == 'fpg':
        df = pd.read_csv(f"models/fp_growth/{form_name}/relevant.csv", delimiter=',')
    else:
        print("INVALID ALGORITHM")
        exit(1)

    confidence_sum = 0

    flag = False
    for ind, row in df.iterrows():

        if form_name in row[2]:
            flag, confidence = check_if_form_is_suitable(row, form_name, columns)
            if flag:
                confidence_sum += confidence

    # print("CONFIDENCE SUM: " + str(confidence_sum) + "\n\n")
    if confidence_sum != 0:
        flag = True
    return flag, confidence_sum


def check_if_form_is_suitable(row, form_name, columns):
    # print(row)

    flag_ok = True
    index_first_curly = row[1].index('{')
    index_second_curly = row[1].index('}')

    cut_row = row[1][index_first_curly+1: index_second_curly]
    row_split = cut_row.split(', ')
    pom = []
    for r in row_split:
        pom.append(r[1: -1])

    for wanted_column in pom:
        if wanted_column not in columns:
            # print(wanted_column)
            # print(columns)
            # print("\n\n")
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

    conf = row[8]
    # print(row[1])
    # print(row[2])
    # print("CONF: " + str(conf))
    # print("\n\n")

    return flag_ok, conf