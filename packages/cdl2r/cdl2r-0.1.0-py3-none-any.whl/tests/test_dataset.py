# -*- coding: utf-8 -*-
"""Testing dataset module
"""
from os.path import abspath, dirname, join
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from cdl2r.dataset import load_data
from cdl2r.constants import LABEL, QID, EID, FEATURES


def test_load_data() -> None:
    """Testing dataset.load_data

    Test Cases:
        - DataFrameの各カラムの型と値が等しいかどうか
        - NumPyを型にしている場合はndarrayとして格納されているかどうか
    """
    test_dir = dirname(abspath(__file__))
    data_path = join(test_dir, 'resources', 'sample_dataset.txt')
    df = load_data(data_path, ndim=4)
    expected_df = pd.DataFrame([
        (0.5, '1', 'x', np.array([0.1, -0.2, 0.3, 0.0], dtype=np.float64)),
        (0.0, '1', 'y', np.array([-0.1, 0.2, 0.0, 0.4], dtype=np.float64)),
        (-0.5, '1', 'z', np.array([0.0, -0.2, 0.3, -0.4], dtype=np.float64)),
        (0.5, '2', 'y', np.array([0.1, -0.2, 0.3, 0.0], dtype=np.float64)),
        (0.0, '2', 'z', np.array([-0.1, 0.2, 0.0, 0.4], dtype=np.float64)),
        (-0.5, '2', 'w', np.array([0.0, -0.2, 0.3, -0.4], dtype=np.float64))
    ], columns=(LABEL, QID, EID, FEATURES))
    assert assert_frame_equal(df, expected_df) is None
    assert isinstance(df.iloc[0, 3], np.ndarray)
