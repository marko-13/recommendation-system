# imports
import pandas as pd
from surprise import Dataset
from surprise import KNNWithMeans
from surprise import SVD
from surprise.model_selection import GridSearchCV


def load_data():
    data = Dataset.load_builtin('ml-100k')
    # similarity options
    sim_options = {"name": "msd", "user_based": False}

    param_grid = {
        "n_epochs": [5, 10],
        "lr_all": [0.002, 0.005],
        "reg_all": [0.4, 0.6]
    }

    # algorithm
    algo = KNNWithMeans(sim_options=sim_options)

    # computation
    training_set = data.build_full_trainset()

    algo.fit(training_set)

    # GRID SEACH, MATRIX FACTORIZATION
    print("Divide matrix in grids")
    gs = GridSearchCV(SVD, param_grid=param_grid, measures=["rmse"], cv=3)
    gs.fit(data)

    print(gs.best_score['rmse'])