#!/usr/bin/env python
'''
Implement deployment step

Author: ucaiado
Date: March 2022
'''
import json
import pathlib
import subprocess


# Load config.json and correct path variable
path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


input_data_path = path_to_conf / pathlib.Path(config['output_folder_path'])
input_model_path = path_to_conf / pathlib.Path(config['output_model_path'])
output_folder_path = path_to_conf / \
    pathlib.Path(config['prod_deployment_path'])


# function for deployment
def store_model_into_pickle(
    input_dpath: pathlib.Path = input_data_path,
    input_mpath: pathlib.Path = input_model_path,
    output_path: pathlib.Path = output_folder_path,
) -> None:
    '''
    Copy files from input_mpath and input_dpath to output_path
    '''
    # NOTE: copy the latest pickle file, the latestscore.txt value, and the
    # ingestfiles.txt file into the deployment directory

    # create the output folder if it does not exist
    output_path.mkdir(parents=True, exist_ok=True)

    # delete old file version
    for this_file in output_path.glob('*'):
        this_file.unlink(missing_ok=True)

    # copy files from source path to new location
    l_path_seq = [input_model_path, input_dpath, input_mpath]
    l_files_seq = ['latestscore.txt', 'ingestedfiles.txt', 'trainedmodel.pkl']
    for this_path, this_file in zip(l_path_seq, l_files_seq):
        s_cmd = f'cp {this_path / this_file} {output_path}/'
        subprocess.call(s_cmd, shell=True)
