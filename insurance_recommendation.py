# imports
import pandas as pd
import numpy as np


def load_and_drop_data(filename):
    df = pd.read_csv(filename, delimiter=',')
    # print(df)

    columns_to_drop = ['LineOfBusiness', 'ERMSDealNumber', 'InceptionDate', 'ExpiryDate', 'Paper', 'IsAdmitted',
                       'InsuredName', 'BrokerCompanyAddress', 'BrokerContact', 'DealComponentID']

    df.drop(columns_to_drop, inplace=True, axis=1)

    # print(df)

    return df


def decompose_column(df, column_name):
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


def replace_column_with_decomposed(df, column_name, df_decomposed):
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
