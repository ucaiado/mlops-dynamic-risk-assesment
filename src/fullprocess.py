#!/usr/bin/env python
'''
Trigger the ML pipeline

Author: ucaiado
Date: March 2022
'''

import pathlib
import json
import pandas as pd
import logging

try:
    from . import (
        scoring,
        ingestion,
        training,
        apicalls,
        reporting,
        deployment)
except:
    import scoring
    import ingestion
    import training
    import apicalls
    import reporting
    import deployment


# Load config.json and get environment variables
path_to_conf = pathlib.Path.cwd() / 'src'
with open(path_to_conf / 'config.json', 'r') as f:
    config = json.load(f)


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


output_folder_path = path_to_conf / pathlib.Path(config['output_folder_path'])
input_folder_path = path_to_conf / pathlib.Path(config['input_folder_path'])
prod_depl_path = path_to_conf / pathlib.Path(config['prod_deployment_path'])


# Check and read new data
def check_and_read_new_data(
        input_path: pathlib.Path = input_folder_path,
        prod_path: pathlib.Path = prod_depl_path,
) -> dict:
    '''
    Check and ingest new data
    '''
    # first, read ingestedfiles.txt
    df_ingestedfiles = pd.read_csv(prod_path / 'ingestedfiles.txt')

    # second, determine whether the source data folder has files that aren't
    # listed in ingestedfiles.txt
    l_last = [path_file.name for path_file in input_path.glob('*.csv')]
    l_diff = list(set(l_last) - set(df_ingestedfiles['file_name']))

    # Deciding whether to proceed, part 1
    logger.info(f"[check_and_read_new_data] There is "
                f"{len(l_diff)} new files")
    if len(l_diff) > 0:
        ingestion.merge_multiple_dataframe()
        return True

    return False


# Checking for model drift
def check_for_model_drift(
        has_new_data: bool,
        prod_path: pathlib.Path = prod_depl_path,
        output_path: pathlib.Path = output_folder_path,
) -> None:
    '''
    Redeploy model if there is a model drift
    '''
    # if you found new data, you should proceed. otherwise, do end here
    if not has_new_data:
        return

    # check whether the score from the deployed model is different from the
    # score from the model that uses the newest ingested data
    f_f1_old = float((prod_path / 'latestscore.txt').read_text().strip())
    f_f1_new = scoring.score_model(
        input_path=(output_path / 'finaldata.csv'),
        output_path=prod_path,
        b_save_score=False)

    # Deciding whether to proceed, part 2
    # if you found model drift, you should proceed. otherwise, do end the
    # process here
    logger.info(f"[check_for_model_drift] Old score: {f_f1_old}, "
                f"New score: {f_f1_new}")
    if (f_f1_old - f_f1_new) < -1e-6:
        return

    # Re-deployment
    # if you found evidence for model drift, re-run the deployment.py script
    logger.info("[check_for_model_drift] Re-depoying model")
    training.train_model()
    scoring.score_model()
    deployment.store_model_into_pickle()

    # Diagnostics and reporting
    # run diagnostics.py and reporting.py for the re-deployed model
    logger.info("[check_for_model_drift] Diagnosing the new model")
    reporting.score_model()
    apicalls.create_api_returns()  # NOTE: api should be running


if __name__ == '__main__':
    NEW_DATA = check_and_read_new_data()
    check_for_model_drift(NEW_DATA)
