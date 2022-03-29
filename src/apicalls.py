#!/usr/bin/env python
'''
Implement the app interface

Author: ucaiado
Date: March 2022
'''
import requests
import pathlib
import joblib
import json


# Specify a URL that resolves to your workspace
URL = "http://0.0.0.0:8000/"


path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


output_folder_path = path_to_conf / pathlib.Path(config['output_model_path'])


# Call each API endpoint and store the responses
def create_api_returns(
        output_path: pathlib.Path = output_folder_path,
        s_url: str = URL):
    '''
    Create apireturn file with all returns from API
    '''
    # delete old output file version
    (output_path / 'apireturns.txt').unlink(missing_ok=True)

    # collect responses
    s_fname = 'testdata/testdata.csv'
    d_responses = {}
    d_responses[1] = requests.post(f'{s_url}prediction?dataset_path={s_fname}')
    d_responses[2] = requests.get(f'{s_url}scoring')
    d_responses[3] = requests.get(f'{s_url}summarystats')
    d_responses[4] = requests.get(f'{s_url}diagnostics')

    # combine all API responses and write the responses to your workspace
    with (output_path / 'apireturns.txt').open('a') as fw:
        for ii in d_responses:
            fw.write(json.dumps(d_responses[ii].json(), indent=4) + '\n')


if __name__ == '__main__':
    create_api_returns()


