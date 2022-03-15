#!/usr/bin/env python
'''
Implement mode training step

Author: ucaiado
Date: March 2022
'''
import pickle
import os
import json

import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pathlib
import joblib


# Load config.json and get path variables
path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


input_folder_path = path_to_conf / pathlib.Path(config['output_folder_path'])
output_folder_path = path_to_conf / pathlib.Path(config['output_model_path'])


# Function for training the model
def train_model(
        input_path: pathlib.Path = input_folder_path,
        output_path: pathlib.Path = output_folder_path,
    ) -> None:
    '''
    Fit a LogisticRegression with data from input_path and save it as pickle
    file in the output_path
    '''

    # create the output folder if it does not exist
    output_path.mkdir(parents=True, exist_ok=True)

    # delete old file version
    (output_path / 'trainedmodel.pkl').unlink()

    # use this logistic regression for training
    regr = LogisticRegression(
        C=1.0,
        class_weight=None,
        dual=False,
        fit_intercept=True,
        intercept_scaling=1,
        l1_ratio=None,
        max_iter=100,
        multi_class='auto',
        n_jobs=None,
        penalty='l2',
        random_state=0,
        solver='liblinear',
        tol=0.0001,
        verbose=0,
        warm_start=False)

    # recover data to train the model
    # NOTE: The dataset's final column, "exited", is the target variable for
    # our predictions. The first column, "corporation", will not be used in
    # modeling. The other three numeric columns will all be used as predictors
    # in your ML mode
    df_data = pd.read_csv(input_path / 'finaldata.csv')
    df_y = df_data.pop('exited')
    df_x = df_data.drop(['corporation'], axis=1)

    # fit the logistic regression to your data
    model = regr.fit(df_x, df_y.astype(int))


    # write the trained model to your workspace in a file called
    # trainedmodel.pkl
    joblib.dump(model, output_path / 'trainedmodel.pkl')
