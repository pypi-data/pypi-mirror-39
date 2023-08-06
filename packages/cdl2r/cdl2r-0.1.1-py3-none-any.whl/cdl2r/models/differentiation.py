# -*- coding: utf-8 -*-
"""Differentiation of model equation components
"""
from typing import List
import numpy as np


def diff_Iec_ve(
        com_indices: List[int],
        Vc: np.ndarray) -> np.ndarray:
    """The result of partial differentiation of Iec with ve.

    Returns:
        partial_Iec_with_ve: Its shape is (k, ).
    """
    return np.sum(Vc.take(com_indices, axis=0), axis=0)

def diff_Iec_vc(
        tar_index: int,
        Ve: np.ndarray) -> np.ndarray:
    """The result of partial differentiation of Iec with ve.

    Returns:
        partial_Iec_with_vc: Its shape is (k, ).
    """
    return Ve[tar_index]

def diff_Ief_ve(
        x: np.ndarray,
        Vf: np.ndarray) -> np.ndarray:
    """The result of partial differentiation of Ief with ve.

    Returns:
        partial_Iec_with_ve: Its shape is (k, ).
    """
    return np.sum(np.multiply(Vf.T, x).T, axis=0)

def diff_Ief_vf(
        tar_index: int,
        x: np.ndarray,
        Ve: np.ndarray) -> np.ndarray:
    """The result of partial differentiation of Ief with vf.

    Returns:
        partial_Ief_with_vf: Its shape is (q, k)
    """
    return np.outer(x, Ve[tar_index])

def diff_Iff_vf(
        x: np.ndarray,
        Vf: np.ndarray) -> np.ndarray:
    """The result of partial differentiation of Iff with vf.

    Returns:
        partial_Iff_with_vf: Its shape is (q, k).
    """
    summation = np.sum((Vf.T * x).T, axis=0)
    first_term = np.outer(x, summation)
    second_term = (Vf.T * np.square(x)).T
    return first_term - second_term
