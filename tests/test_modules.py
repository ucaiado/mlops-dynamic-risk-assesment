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
    )


@pytest.fixture
def output_path() -> pathlib.Path:
    return pathlib.Path.cwd() / 'src' / 'output'


def test_ingestion(output_path: pathlib.Path):
    ingestion.merge_multiple_dataframe()

    for s_file in ['finaldata.csv', 'ingestedfiles.txt']:
        s_err = f'!!no file {s_file} located'
        assert (output_path / s_file).is_file(), s_err