#!/usr/bin/env python
'''
Implement scoring step

Author: ucaiado
Date: March 2022
'''
import json
import pathlib
import joblib

import pandas as pd
from sklearn import metrics


# Load config.json and get path variables
path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


input_folder_path = path_to_conf / pathlib.Path(config['test_data_path'])
output_folder_path = path_to_conf / pathlib.Path(config['output_model_path'])


# Function for model scoring
def score_model(
    input_path: pathlib.Path = input_folder_path,
    output_path: pathlib.Path = output_folder_path,
    b_save_score: bool = True
) -> None:
    '''
    Score model in output_path using test data from input_path and save the
    output in the same model folder
    '''
    # NOTE: take a trained model, load test data, and calculate an F1 score
    # for the model relative to the test data it should write the result to
    # the latestscore.txt file

    # load test data and model
    if 'csv' not in input_path.name:
        df_data = pd.read_csv(input_path / 'testdata.csv')
    else:
        df_data = pd.read_csv(input_path)
    df_y = df_data.pop('exited')
    df_x = df_data.drop(['corporation'], axis=1)
    model = joblib.load(output_path / 'trainedmodel.pkl')

    df_pred = model.predict(df_x)
    f_score = metrics.f1_score(df_pred, df_y)

    if b_save_score:
        # delete old output file version
        (output_path / 'latestscore.txt').unlink(missing_ok=True)
        # save the data
        (output_path / 'latestscore.txt').write_text(f'{f_score:4f}')

    # return the score
    return f_score
