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
from typing import Any
from flask.testing import FlaskClient

sys.path.append(str(pathlib.Path.cwd()))
from src import (
    ingestion,
    training,
    scoring,
    deployment,
    diagnostics,
    reporting,
    app as app_src
    )


@pytest.fixture
def output_path() -> pathlib.Path:
    return pathlib.Path.cwd() / 'src'


@pytest.fixture()
def client():
    app_src.app.config.update({
        "TESTING": True,
    })
    return app_src.app.test_client()


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
        pd.read_csv('testdata/testdata.csv'))

    d_tests['dataframe_summary'] = diagnostics.dataframe_summary(
        pd.read_csv('ingesteddata/finaldata.csv'))

    d_tests['execution_time'] = diagnostics.execution_time()

    d_tests['outdated_packages_list'] = diagnostics.outdated_packages_list()

    for s_test in d_tests:
        s_err = f'!! diagnostics.{s_test}() failed'
        b_test1 = not isinstance(d_tests[s_test], type(None))
        assert b_test1 and len(d_tests[s_test]) > 0, s_err


def test_reporting(output_path: pathlib.Path):
    reporting.score_model()

    for s_file in ['confusionmatrix.png']:
        s_err = f'!!no file {s_file} located'
        assert (output_path / 'practicemodels' / s_file).is_file(), s_err


def test_app(output_path: pathlib.Path, client: FlaskClient):

    # test prediction end-point
    s_api_file = 'testdata/testdata.csv'
    response = client.post(f"/prediction?dataset_path={s_api_file}")

    assert response.status_code == 200
    assert b'predictions' in response.data

    # test prediction end-point
    s_api_file = 'testdata/testdata.csv'
    response = client.post(f"/prediction?dataset_path={s_api_file}")

    assert response.status_code == 200
    assert b'predictions' in response.data

    # test scoring end-point
    response = client.get(f"/scoring")

    assert response.status_code == 200
    assert b'score' in response.data

    # test prediction end-point
    response = client.get(f"/summarystats")

    assert response.status_code == 200
    assert b'summary' in response.data

    # test prediction end-point
    response = client.get(f"/diagnostics")

    assert response.status_code == 200
    assert b'missing_values' in response.data
