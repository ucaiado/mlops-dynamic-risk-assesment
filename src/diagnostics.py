#!/usr/bin/env python
'''
Implement diagnostics step

Author: ucaiado
Date: March 2022
'''
import json
import pathlib
import subprocess
from typing import List

import timeit
import joblib

import pandas as pd

# Load config.json and get environment variables
path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


input_data_path = path_to_conf / pathlib.Path(config['output_folder_path'])
input_deployment_path = path_to_conf / \
    pathlib.Path(config['prod_deployment_path'])
output_folder_path = path_to_conf / pathlib.Path(config['test_data_path'])


# function for deployment

def _prepare_data(df_data):
    '''drop unused columns'''
    return df_data.drop(['corporation', 'exited'], axis=1)


def _measure_time(s_cmd):
    '''compute the time to run the script passed'''
    f_start = timeit.default_timer()
    subprocess.call(s_cmd, shell=True)
    f_timing = timeit.default_timer() - f_start

    return f_timing


# Function to get model predictions
def model_predictions(
    df_data: pd.DataFrame,
    input_mpath: pathlib.Path = input_deployment_path,
) -> List[int]:
    '''Read the deployed model and a given dataset, calculate predictions'''
    df_x = _prepare_data(df_data)
    model = joblib.load(input_mpath / 'trainedmodel.pkl')
    return list(model.predict(df_x))


# Function to get summary statistics
def dataframe_summary(df_data: pd.DataFrame):
    '''calculate summary statistics'''
    df_x = _prepare_data(df_data)
    df_x.agg(['mean', 'median', 'std'])

    l_out = []
    for (s_key, d_st) in df_x.agg(['mean', 'median', 'std']).to_dict().items():
        d_st['feature'] = s_key
        l_out.append(d_st)

    return l_out


# Function to get timings
def execution_time(
    input_data_path: pathlib.Path = input_deployment_path,
):
    '''calculate timing of training.py and ingestion.py'''
    l_rtn = []
    path_root = input_data_path.parents[0]
    l_rtn.append(_measure_time(f'python {path_root}/ingestion.py'))
    l_rtn.append(_measure_time(f'python {path_root}/training.py'))

    assert len(l_rtn) == 2

    return l_rtn


# Function to check dependencies
def outdated_packages_list():
    '''get a list of deprected packages'''
    s_cmd = 'pip list --outdated'
    result = subprocess.run(s_cmd, shell=True, capture_output=True, text=True)
    s_aux = result.stdout
    l_out = [row.replace('  ', ' ').split() for row in s_aux.split('\n')]
    l_out = [dict(zip(l_out[0], row)) for row in l_out[2:]]

    assert 'Package' in l_out[0]

    return l_out


if __name__ == '__main__':
    model_predictions()
    dataframe_summary()
    execution_time()
    outdated_packages_list()
