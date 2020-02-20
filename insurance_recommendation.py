# imports
import pandas as pd

def load_and_drop_data(filename):
    df = pd.read_csv(filename, delimiter=',')
    print(df)

    columns_to_drop = ['LineOfBusiness', 'ERMSDealNumber', 'InceptionDate', 'ExpiryDate', 'Paper', 'IsAdmitted',
                       'InsuredName', 'BrokerCompanyAddress', 'BrokerContact', 'DealComponentID']

    df.drop(columns_to_drop, inplace=True, axis=1)

    print(df)