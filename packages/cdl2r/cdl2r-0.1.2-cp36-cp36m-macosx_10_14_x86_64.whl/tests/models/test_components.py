# -*- coding: utf-8 -*-
import numpy as np
from cdl2r.models import components as compos


class TestComponents(object):
    """models.equationモジュールのテスト
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

    def test_compute_Iec(self):
        """
        推定対象のエンティティID: 0
        競争相手のエンティティIDs: 1, 2
        """
        tar_index = 0
        com_indices = [1, 2]
        result = compos.compute_Iec(tar_index, com_indices, self.Ve, self.Vc)
        expected = 82.0
        assert result == expected
        assert isinstance(result, np.float64)

    def test_compute_Ief(self):
        """
        推定対象のエンティティID: 0
        """
        tar_index = 0
        result = compos.compute_Ief(tar_index, self.x, self.Ve, self.Vf)
        expected = 164.0
        assert result == expected
        assert isinstance(result, np.float64)

    def test_compute_Iff(self):
        # not using self.x
        x = np.array([1.0, -2.0, 3.0, -4.0])
        result = compos.compute_Iff(x, self.Vf)
        expected = -2774.0
        assert result == expected
        assert isinstance(result, np.float64)
