#!/usr/bin/env python
'''
Implement data ingestion step

Author: ucaiado
Date: March 2022
'''
import os
import json
import pathlib

from datetime import datetime

import pandas as pd


# Load config.json and get input and output paths
path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


input_folder_path = path_to_conf / pathlib.Path(config['input_folder_path'])
output_folder_path = path_to_conf / pathlib.Path(config['output_folder_path'])


# Function for data ingestion
def merge_multiple_dataframe(
        input_path: pathlib.Path = input_folder_path,
        output_path: pathlib.Path = output_folder_path,
) -> None:
    '''
    Merge data found in input_path and save it to output_path
    '''
    # create the output folder if it does not exist
    output_path.mkdir(parents=True, exist_ok=True)

    # delete old files versions
    (output_path / 'finaldata.csv').unlink()
    (output_path / 'ingestedfiles.txt').unlink()

    # check for datasets, compile them together, and write to an output file
    df_output = pd.DataFrame()
    l_ingt = []
    for path_file in input_path.glob('*.csv'):
        df_ = pd.read_csv(path_file)
        df_output = pd.concat([df_output, df_])
        l_ingt.append({
            'file_name': path_file.name,
            'number_of_rows': df_.shape[0],
            'date_compiled': f'{datetime.now():%Y-%m-%d}',
        })

    # De-dupe the compiled data frame before saving
    df_output = df_output.drop_duplicates()

    # save files
    df_output.to_csv(output_path / 'finaldata.csv', index=False)
    pd.DataFrame(l_ingt).to_csv(output_path / 'ingestedfiles.txt', index=False)


if __name__ == '__main__':
    merge_multiple_dataframe()
