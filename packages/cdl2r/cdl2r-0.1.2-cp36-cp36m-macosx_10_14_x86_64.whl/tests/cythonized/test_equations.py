# -*- coding: utf-8 -*-
import numpy as np
from cdl2r.cythonized import equations as eqn


class TestEquations(object):
    """Testing cythonized equations module.
    """

    def setup_method(self, method):
        self.b = np.float64(0.0)
        self.w = np.ones(4)
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
        pass

    def test_cdfm_regression(self):
        """CDFM Regression without proximity.
        """
        tar_index = 0
        com_indices = [1, 2]
        x = np.ones(4)
        result = eqn.cdfm_regression(self.b, self.w,
                                     self.Ve, self.Vc, self.Vf,
                                     tar_index, com_indices, x)
        expected = np.float64(0.0 + 4.0 + 82.0 + 164.0 + 705.0)
        assert result == expected
        assert isinstance(result, np.float64)
