#!/usr/bin/env python
'''
Implement data ingestion step

Author: ucaiado
Date: March 2022
'''
import json
import pathlib

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import metrics

from .diagnostics import model_predictions


# Load config.json and get path variables
path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


input_data_path = path_to_conf / pathlib.Path(config['test_data_path'])
output_model_path = path_to_conf / pathlib.Path(config['output_model_path'])


# Function for reporting
def score_model(
    input_dpath: pathlib.Path = input_data_path,
    output_path: pathlib.Path = output_model_path,
) -> plt.Figure:
    '''
    calculate a confusion matrix using the test data and the deployed model.
    write the confusion matrix to the workspace
    '''
    # compute confusion matrix
    df_data = pd.read_csv(input_dpath / 'testdata.csv')

    confusion_matrix = pd.DataFrame(
        metrics.confusion_matrix(
            y_true=df_data['exited'].values,
            y_pred=np.array(model_predictions(this_data=df_data))),
        index=['False', 'True'],
        columns=['False', 'True']
    )

    fig, ax = plt.subplots(1, 1)

    sns.heatmap(confusion_matrix, annot=True, fmt='d', cbar=False, ax=ax)

    ax.set_title('Client Exited\n')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Observed')

    fig.savefig(output_path / 'confusionmatrix.png')

    return fig


if __name__ == '__main__':
    score_model()
