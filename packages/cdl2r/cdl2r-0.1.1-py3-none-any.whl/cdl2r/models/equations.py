# -*- coding: utf-8 -*-
"""Model Equations

Variables:
    k: The number of dimensions of latent vectors (factors).
    p: The number of entities in your dataset.
    q: The number of feature dimensions of an entity.
"""
from typing import List
import numpy as np


def compute_Iec(
        tar_index: int,
        com_indices: List[int],
        Ve: np.ndarray,
        Vc: np.ndarray) -> np.float64:
    """Interaction terms between Entity and Competitors.

    推定対象のエンティティと競争相手のエンティティ間の交互作用項を求める。

    Parameters:
        tar_index: 推定対象となるエンティティの行列でのインデックス
        com_indices: 競争相手のエンティティの行列でのインデックスリスト
        Ve: 推定対象のエンティティのk次元の潜在ベクトルを束ねた行列(p, k)
        Vc: 競争相手のエンティティのk次元の潜在ベクトルを束ねた行列(p, k)

    Returns:
        result: エンティティと競争相手の交互作用
    """
    return np.sum(np.dot(Vc[com_indices], Ve[tar_index]), axis=0)

def compute_Ief(
        tar_index: int,
        x: np.ndarray,
        Ve: np.ndarray,
        Vf: np.ndarray) -> np.float64:
    """Interaction terms between Entity and its Features.

    Parameters:
        tar_index: 推定対象となるエンティティの行列でのインデックス
        x: 推定対象のエンティティの特徴量ベクトル
        Ve: 推定対象のエンティティのk次元の潜在ベクトルを束ねた行列(p, k)
        Vf: エンティティの特徴量に対する重みのk次元の潜在ベクトルを束ねた
            行列(p, k)

    Returns:
        result: エンティティと特徴量の交互作用
    """
    return np.dot(np.dot(Vf, Ve[tar_index]), x)

def compute_Iff(
        x: np.ndarray,
        Vf: np.ndarray) -> np.float64:
    """Interaction terms between 2 Features.

    Parameters:
        x: 推定対象のエンティティの特徴量ベクトル
        Vf: エンティティの特徴量に対する重みのk次元の潜在ベクトルを束ねた
            行列(p, k)

    Returns:
        result: エンティティの特徴量間の交互作用
    """
    Vfx = np.multiply(Vf.T, x).T
    squared_sum = np.square(np.sum(Vfx, axis=0))
    sum_squared = np.sum(np.square(Vfx), axis=0)
    return 0.5 * np.sum(squared_sum - sum_squared)
