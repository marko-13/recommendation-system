from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import SGD

import numpy as np

import pickle

import os

def save_nn(model, report=None):

    if not os.path.exists('models'):
        os.mkdir('models')

    if not os.path.exists('models/nn'):
        os.mkdir('models/nn')

    if not os.path.exists(f'models/nn/{model._net_name}'):
        os.mkdir(f'models/nn/{model._net_name}')

    model.save_weights(f'models/nn/{model._net_name}/weights.h5')
    
    if report is not None:
        with open(f'models/nn/{model._net_name}/history_dict', 'wb') as file_pi:
            pickle.dump(report.history, file_pi)

def load_nn(model):
    model.load_weights(f'models/nn/{model._net_name}/weights.h5')

    return model

def construct_nn(input_dim, form_name):
    
    model = Sequential()

    # Name the model by the form it predicts
    model._net_name = form_name

    model.add(Dense(128, input_dim=input_dim, activation='relu'))
    model.add(Dense(64, input_dim=128, activation='relu'))
    model.add(Dense(1, input_dim=64, activation='sigmoid'))

    return model


def train_nn(model, X_train, y_train):

    dataset_len = len(X_train)

    X_train = np.array(X_train, np.float32)
    y_train = np.array(y_train, np.float32)

    sgd = SGD(lr=0.001, momentum=0.9)

    model.compile(loss='mean_squared_error', optimizer=sgd)

    report = model.fit(X_train, y_train, epochs=100, batch_size=8, verbose=1, shuffle=True, validation_split=0.15)

    return model, report


def run_training_for_all_forms(df, first_form_index):

    cols_to_train = list(df.columns.values[first_form_index:])

    # print(cols_to_train)

    # y = df.iloc[:, first_form_index:]

    X = df.iloc[:, :first_form_index]
    
    all_inputs = []

    # Extract inputs
    for ind, row in X.iterrows():
        curr_row = []

        for el in row:
            curr_row.append(el)

        all_inputs.append(curr_row)

    # print(len(all_inputs[0]))

    # Extract labels for each form:
    for col_name in cols_to_train:
        curr_col = df[col_name]
        labels = curr_col.values

        # the first_form_index represents the input length
        model = construct_nn(first_form_index, col_name)

        model, report = train_nn(model, all_inputs, labels)

        save_nn(model, report)