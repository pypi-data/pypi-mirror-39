# -*- coding: utf-8 -*-
import numpy as np
from cdl2r.models import differentiation as diff


class TestDifferentiation(object):
    """models.differentiationモジュールのテスト
    """

    def setup_method(self, method):
        print(f'method: {method.__name__}')
        self.x = np.ones(4)
        self.Ve = np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
        ])
        self.Vc = np.array([
            [1.0, 2.0, 3.0],
            [4.0, 5.0, 6.0],
            [7.0, 8.0, 9.0],
        ])
        self.Vf = np.array([
            [1.0,  2.0,  3.0],  # 6
            [4.0,  5.0,  6.0],  # 15
            [7.0,  8.0,  9.0],  # 24
            [10.0, 11.0, 12.0]  # 33
            # 22    26    30
            # sum_squared = 2060
            # squared_sum = 650
        ])

    def teardown_method(self, method):
        print(f'method: {method.__name__}')

    def test_diff_Iec_ve(self):
        """
        推定対象のエンティティID: 0
        競争相手のエンティティIDs: 1, 2
        """
        com_indices = [1, 2]
        result = diff.diff_Iec_ve(com_indices, self.Vc)
        expected = np.array([11.0, 13.0, 15.0])
        assert (result == expected).all()
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float64

    def test_diff_Iec_vc(self):
        """
        推定対象のエンティティID: 0
        競争相手のエンティティIDs: 1, 2
        """
        tar_index = 0
        result = diff.diff_Iec_vc(tar_index, self.Ve)
        expected = np.array([1.0, 2.0, 3.0])
        assert (result == expected).all()
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float64

    def test_diff_Ief_ve(self):
        """
        推定対象のエンティティID: 0
        """
        result = diff.diff_Ief_ve(self.x, self.Vf)
        expected = np.array([22, 26, 30])
        assert (result == expected).all()
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float64

    def test_diff_Ief_vf(self):
        """
        推定対象のエンティティID: 0
        """
        tar_index = 0
        result = diff.diff_Ief_vf(tar_index, self.x, self.Vf)
        expected = np.array([
            [1.0, 2.0, 3.0],
            [1.0, 2.0, 3.0],
            [1.0, 2.0, 3.0],
            [1.0, 2.0, 3.0]
        ])
        assert (result == expected).all()
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float64

    def test_diff_Iff_vf(self):
        # not using self.x
        x = np.array([1.0, -2.0, 3.0, -4.0])
        result = diff.diff_Iff_vf(x, self.Vf)
        expected = np.array([
            [ -27.0,  -30.0,  -33.0],
            [  36.0,   36.0,   36.0],
            [-141.0, -156.0, -171.0],
            [ -56.0,  -64.0,  -72.0],
        ])  # culculated by hand
        assert (result == expected).all()
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float64
