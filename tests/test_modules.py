'''
Implement tests to scripts implemented in src/ folder

Author: ucaiado
Date: March 2022
'''

import sys
import pathlib
import pytest
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

sys.path.append(str(pathlib.Path.cwd()))
from src import (
    ingestion,
    training,
    scoring,
    deployment,
    diagnostics
    )


@pytest.fixture
def output_path() -> pathlib.Path:
    return pathlib.Path.cwd() / 'src'


def test_ingestion(output_path: pathlib.Path):
    ingestion.merge_multiple_dataframe()

    for s_file in ['finaldata.csv', 'ingestedfiles.txt']:
        s_err = f'!!no file {s_file} located'
        assert (output_path / 'ingesteddata' / s_file).is_file(), s_err


def test_training(output_path: pathlib.Path):
    training.train_model()

    for s_file in ['trainedmodel.pkl']:
        s_err = f'!!no file {s_file} located'
        assert (output_path / 'practicemodels' / s_file).is_file(), s_err


def test_scoring(output_path: pathlib.Path):
    scoring.score_model()

    for s_file in ['latestscore.txt']:
        s_err = f'!!no file {s_file} located'
        assert (output_path / 'practicemodels' / s_file).is_file(), s_err


def test_deployment(output_path: pathlib.Path):
    deployment.store_model_into_pickle()

    for s_fl in ['latestscore.txt', 'ingestedfiles.txt', 'trainedmodel.pkl']:
        s_err = f'!!no file {s_fl} located'
        assert (output_path / 'production_deployment' / s_fl).is_file(), s_err


def test_diagnostics(output_path: pathlib.Path):
    d_tests = {}

    d_tests['count_na'] = diagnostics.count_missing_values()

    d_tests['model_predictions'] = diagnostics.model_predictions(
        pd.read_csv(output_path / 'testdata' / 'testdata.csv'))

    d_tests['dataframe_summary'] = diagnostics.dataframe_summary(
        pd.read_csv(output_path / 'ingesteddata' / 'finaldata.csv'))

    d_tests['execution_time'] = diagnostics.execution_time()

    d_tests['outdated_packages_list'] = diagnostics.outdated_packages_list()

    for s_test in d_tests:
        s_err = f'!! diagnostics.{s_test}() failed'
        b_test1 = not isinstance(d_tests[s_test], type(None))
        assert b_test1 and len(d_tests[s_test]) > 0, s_err


