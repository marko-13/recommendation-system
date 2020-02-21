# imports
import pandas as pd
import numpy as np


def run_data_preprocessing_pipeline():
    '''
    Returns a pandas dataframe of the preprocessed input and the column
    index of the first form.
    '''
    file_name = 'data/BC - AI ORIGINAL.csv'

    df = load_and_drop_data(file_name)

    df = decompose_columns(df)

    cols = list(df.columns)

    first_form_index = cols.index('MJIL 1000 08 10')

    df, first_form_index = remove_unbalanced_columns(df, first_form_index)


    # print(first_form_index)

    # print(df[df.columns[first_form_index]])

    df.to_csv('data/cleansed.csv', index=False)

    return df, first_form_index


def remove_unbalanced_columns(df, first_form_index):
    for column in df.columns:
        pom = df.groupby(column)[column].nunique()
        # print(df[column])
        num_ones = 0
        num_zeros = 0
        for el in df[column]:
            if el == 0:
                num_zeros +=1
            else:
                num_ones += 1

        if num_ones > num_zeros:
            flag = num_zeros / num_ones
        else:
            flag = num_ones / num_zeros

        cols1 = list(df.columns)

        cur_ind = cols1.index(column)

        print("Flag: " + str(flag))
        if flag <= 0.005 and first_form_index > cur_ind:
            print("Removing column based on unbalanced data: " + str(column))
            with open('log/report.txt', 'a+') as f:
                f.write(f"Column: {column} is dropped because of unbalanced data.\n")
            df.drop(column, inplace=True, axis=1)
            first_form_index -= 1

    return  df, first_form_index


def load_and_drop_data(filename):
    df = pd.read_csv(filename, delimiter=',')
    # print(df)

    columns_to_drop = ['LineOfBusiness', 'ERMSDealNumber', 'InceptionDate', 'ExpiryDate', 'Paper', 'IsAdmitted',
                       'InsuredName', 'BrokerCompanyAddress', 'BrokerContact', 'DealComponentID']


    # if all values are in row drop that row
    for column in df.columns:
        # print(df[column])
        nominal_values = df.groupby(column)[column].nunique().index.tolist()
        # print(nominal_values)
        if len(nominal_values) == 1:
            columns_to_drop.append(str(column))

            with open('log/report.txt', 'a+') as f:
                f.write(f"Column: {column} is dropped because it has only one distinct value.\n")


    df.drop(columns_to_drop, inplace=True, axis=1)

    # print(df)
    return df


def decompose_columns(df):
    '''
    Runs column decomposition on nominal columns in the dataframe.

    Replaces said columns with True/False columns for every distinct
    nominal value.
    '''

    decomp_columns = [
        'BusinessSegment',
        'Type',
        'InsuredState',
        'BrokerCompany',
        'BrokerState',
        'UnderwriterTeam',
        'BusinessClassification'
        ]

    for col in decomp_columns:
        try:
            print(f'Trying {col}')
            new_cols = _decompose_column(df, col)
            df = _replace_column_with_decomposed(df, col, new_cols)
        except ValueError:
            print(f'---Failed {col}')

    return df

def _decompose_column(df, column_name):
    '''
    Decomposes a nominal column with N distinct inputs into N
    true/false columns. Essentialy creates a pandas dataframe
    representing a 1-hot encoding of the nominal column.

    Args:
        df (pandas.Dataframe): The pandas dataframe of the dataset
        column_name (str): The name of the column to decompose.

    Returns:
        pandas.Dataframe: A dataframe of only the decomposed column.
    '''

    if column_name not in df.columns:
        raise ValueError(f'Column "{column_name}" does not exist in this dataframe.')
    
    nominal_values = df.groupby(column_name)[column_name].nunique().index.tolist()

    num_vals = len(nominal_values)

    column_map = {nominal_values[i]: i for i in range(len(nominal_values))}

    rows = []

    for nom_val in df[column_name]:
        row = np.zeros(num_vals, dtype="int32")

        # NOTE: How to handle NULL values? Do we treat them as a new
        # column or just ignore them (as we are now)?
        try:        
            index = column_map[nom_val]
            row[index] = 1
        except KeyError:
            pass

        rows.append(row)

    # Add original column name as prefix to new columns
    nominal_values = [column_name + "_" + nom_val for nom_val in nominal_values]

    ret_df = pd.DataFrame(rows, columns=nominal_values)

    return ret_df


def _replace_column_with_decomposed(df, column_name, df_decomposed):
    '''
    Takes in a column name and replaces it with the columns 
    provided in df_decomposed.
    '''

    # Get the index of the soon-to-be removed column
    insert_index = df.columns.get_loc(column_name) + 1

    num_replacement_cols = len(df_decomposed.columns)

    print(f"Inserting {num_replacement_cols} columns in place of '{column_name}'")

    ind_range = list(range(num_replacement_cols))

    ind_range.reverse()

    # print(ind_range)

    for i in ind_range:
        # Insert column into original dataframe
        df.insert(loc=insert_index, column=df_decomposed.columns[i], value=df_decomposed[df_decomposed.columns[i]])

    # Remove the original column
    return df.drop(df.columns[insert_index - 1], axis=1)
