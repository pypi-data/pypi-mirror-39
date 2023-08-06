# -*- coding: utf-8 -*-
"""Implementation of original models
"""
import random
from copy import deepcopy
from typing import Callable, List, Tuple
import numpy as np
import pandas as pd
from . import differentiation as diff
from ..cythonized import equations as eqn
from ..constants import LABEL, PRED_LABEL, QID, EID, FEATURES
from ..types import GroupID, EntityID, EntIndMap


class CDFMRegressor():
    """Combination Dependent Factorization Machines for regression tasks.

    Attributes:
        l2_w: L2 regularization on pointwise weights.
        l2_V: L2 regularization on pairwise weights.
        n_factors: The number of dimensions of latent vectors.
        n_iterations: The number of iteration when training.
        eta: Learning rate.
        init_scale: v ~ Normal(0.0, scale=init_scale).
        epoch_errors: Series of training loss.
        ent_ind_map: Mapping EntityID into Index.

    Parameters:
        b: Global bias.
        w: Weight vector on a feature vector.
        Ve: Matrix of latent vector of Entities.
        Vc: Matrix of latent vector of Competitors.
        Vf: Matrix of latent vector of Entity Features.

    Methods:
        fit: Fitting the model.
        predict: Make prediction.
    """

    # pylint: disable=too-many-instance-attributes, too-many-arguments
    def __init__(
            self,
            l2_w: float = 1e-2,
            l2_V: float = 1e-2,
            n_factors: int = 10,
            n_iterations: int = 1000,
            init_eta: float = 1e-2,
            init_scale: float = 1e-2) -> None:
        self.l2_w = l2_w
        self.l2_V = l2_V
        self.n_factors = n_factors
        self.n_iterations = n_iterations
        self.eta = init_eta
        self.init_scale = init_scale
        self.epoch_errors = np.zeros(n_iterations)
        self.ent_ind_map: EntIndMap = None
        self.b: np.float64 = None
        self.w: np.ndarray = None
        self.Ve: np.ndarray = None
        self.Vc: np.ndarray = None
        self.Vf: np.ndarray = None

    def _initialize_params(
            self,
            n_uniques: int,
            n_features: int) -> None:
        self.b = np.float64(0.0)
        self.w = np.zeros(n_features)
        self.Ve = np.random.normal(scale=self.init_scale, size=(n_uniques, self.n_factors))
        self.Vc = np.random.normal(scale=self.init_scale, size=(n_uniques, self.n_factors))
        self.Vf = np.random.normal(scale=self.init_scale, size=(n_features, self.n_factors))

    def _make_ent_ind_map(
            self,
            unique_entity_ids: List[EntityID]) -> None:
        self.ent_ind_map = {eid: ind for ind, eid in enumerate(unique_entity_ids)}

    def _model_equation(
            self,
            tar_index: int,
            com_indices: List[int],
            x: np.ndarray) -> np.float64:
        y_hat = eqn.cdfm_regression(self.b, self.w, self.Ve, self.Vc, self.Vf, tar_index, com_indices, x)
        return y_hat

    # pylint: disable=too-many-locals
    def fit(self,
            data: pd.DataFrame,
            verbose: bool = True,
            logger: Callable[[str], None] = print):
        """Training the model.

        Parameters:
            data: DataFrame whose columns are (LABEL, QID, EID, FEATURES).
            verbose: Whether display training processes.
            logger: How to display training processes. Default to `print`.
        """
        unique_entity_ids: List[EntityID] = list(data[EID].unique())
        grouped: List[Tuple[GroupID, pd.DataFrame]] = list(data.groupby(QID))
        features_col_idx: int = data.columns.get_loc(FEATURES)
        # Initialize model params
        self._initialize_params(len(unique_entity_ids), len(data.iloc[0][FEATURES]))
        # Make Entity Index Mapper
        self._make_ent_ind_map(unique_entity_ids)
        # START TRAINING
        for epoch_idx in range(self.n_iterations):
            # gdf is named after `Group DataFrame`.
            for _group_id, gdf in grouped:
                entity_ids: List[EntityID] = list(gdf[EID])
                n_entities: int = len(entity_ids)
                entity_indices: List[int] = [self.ent_ind_map[id_] for id_ in entity_ids]
                com_indices: List[List[int]] = [
                    [ind for ind in entity_indices if ind != tar_index]
                    for tar_index in entity_indices]
                features: List[np.ndarray] = list(gdf.iloc[:, features_col_idx])
                obs_labels: np.ndarray = gdf[LABEL].values
                # Prediction phase
                pred_labels: np.ndarray = np.array([
                    self._model_equation(tar, com, x)
                    for tar, com, x
                    in zip(entity_indices, com_indices, features)])
                # Current params
                w_cur = deepcopy(self.w)
                Ve_cur = deepcopy(self.Ve)
                Vc_cur = deepcopy(self.Vc)
                Vf_cur = deepcopy(self.Vf)
                # Param update phase
                pred_errors = obs_labels - pred_labels
                for err, tar, com, x in zip(pred_errors, entity_indices, com_indices, features):
                    stride = err / n_entities
                    coef_w = x - np.multiply(self.l2_w, w_cur)
                    coef_ve = diff.diff_Iec_ve(com, Vc_cur) \
                        + diff.diff_Ief_ve(x, Vf_cur) \
                        - np.multiply(self.l2_V, Ve_cur[tar])
                    coef_vc = diff.diff_Iec_vc(tar, Ve_cur) \
                        - np.multiply(self.l2_V, Vc_cur[com])
                    coef_vf = diff.diff_Ief_vf(tar, x, Ve_cur) \
                        + diff.diff_Iff_vf(x, Vf_cur) \
                        - np.multiply(self.l2_V, Vf_cur)
                    # Update params
                    self.b += self.eta * stride
                    self.w += self.eta * np.multiply(stride, coef_w)
                    self.Ve[tar] += self.eta * np.multiply(stride, coef_ve)
                    self.Vc[com] += self.eta * np.multiply(stride, coef_vc)
                    self.Vf += self.eta * np.multiply(stride, coef_vf)
                # Update epoch errors
                self.epoch_errors[epoch_idx] += 0.5 * np.sum(np.square(pred_errors))
            # Display epoch error
            if verbose:
                logger(f'Epoch #{epoch_idx + 1}: {self.epoch_errors[epoch_idx]}')
            # Randomize group order
            random.shuffle(grouped)

    def predict(
            self,
            data: pd.DataFrame) -> pd.DataFrame:
        """Make prediction on a given data.

        Parameters:
            data: DataFrame whose columns are (QID, EID, FEATURES).

        Returns:
            updated_data: DataFrame whose columns are (PRED_LABEL, QID, EID, FEATURES).
        """
        prediction = []
        grouped: pd.core.groupby.DataFrameGroupBy = data.groupby(QID)
        group_ids: List[GroupID] = list(grouped.groups.keys())
        for group_id in group_ids:
            group_data: pd.DataFrame = grouped.get_group(group_id)
            entity_ids: List[EntityID] = list(group_data[EID])
            entity_indices: List[int] = [self.ent_ind_map[id_] for id_ in entity_ids]
            # Prediction phase
            for i, entity_id in enumerate(entity_ids):
                tar_index = entity_indices[i]
                com_indices = [ind for ind in entity_indices if ind != tar_index]
                x: np.ndarray = group_data.iloc[i][FEATURES]
                pred_label = self._model_equation(tar_index, com_indices, x)
                prediction.append((pred_label, group_id, entity_id, x))
        return pd.DataFrame(prediction, columns=(PRED_LABEL, QID, EID, FEATURES))
