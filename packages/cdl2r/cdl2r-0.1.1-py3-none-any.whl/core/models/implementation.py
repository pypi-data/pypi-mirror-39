# -*- coding: utf-8 -*-
"""Implementation of original models
"""
import random
from copy import deepcopy
from typing import List, Callable
import numpy as np
import pandas as pd
from . import equations as eqn
from . import differentiation as diff
from ..constants import LABEL, PRED_LABEL, QID, EID, FEATURES
from ..types import GroupID, EntityID, EntIndMap


class CDFMRegressor():
    """Combination Dependent Factorization Machines for regression tasks.

    Attributes:
        n_factors: The number of dimensions of latent vectors.
        n_iterations: The number of iteration when training.
        eta: Learning rate.
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

    def __init__(
            self,
            n_factors: int = 10,
            n_iterations: int = 1000,
            init_eta: float = 1e-2) -> None:
        self.n_factors = n_factors
        self.n_iterations = n_iterations
        self.eta = init_eta
        self.epoch_errors = np.zeros(n_iterations)
        self.ent_ind_map: EntIndMap = None
        self.b: float = None
        self.w: np.ndarray = None
        self.Ve: np.ndarray = None
        self.Vc: np.ndarray = None
        self.Vf: np.ndarray = None

    def _initialize_params(
            self,
            n_entities: int,
            n_features: int) -> None:
        self.b = 0.0
        self.w = np.zeros(n_features)
        self.Ve = np.random.normal(scale=1e-2, size=(n_entities, self.n_factors))
        self.Vc = np.random.normal(scale=1e-2, size=(n_entities, self.n_factors))
        self.Vf = np.random.normal(scale=1e-2, size=(n_features, self.n_factors))

    def _make_ent_ind_map(
            self,
            unique_entity_ids: List[EntityID]) -> None:
        self.ent_ind_map = {eid: ind for ind, eid in enumerate(unique_entity_ids)}

    def _model_equation(
            self,
            tar_index: int,
            com_indices: List[int],
            x: np.ndarray) -> np.float64:
        y_hat = self.b \
            + np.dot(self.w, x) \
            + eqn.compute_Iec(tar_index, com_indices, self.Ve, self.Vc) \
            + eqn.compute_Ief(tar_index, x, self.Ve, self.Vf) \
            + eqn.compute_Iff(x, self.Vf)
        return y_hat

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
        grouped: pd.core.groupby.DataFrameGroupBy = data.groupby(QID)
        group_ids: List[GroupID] = list(grouped.groups.keys())
        # Initialize model params
        self._initialize_params(len(unique_entity_ids), len(data.iloc[0][FEATURES]))
        # Make Entity Index Mapper
        self._make_ent_ind_map(unique_entity_ids)
        # START TRAINING
        for epoch_idx in range(self.n_iterations):
            for group_id in group_ids:
                group_data: pd.DataFrame = grouped.get_group(group_id)
                entity_ids: List[EntityID] = list(group_data[EID])
                entity_indices: List[int] = [self.ent_ind_map[id_] for id_ in entity_ids]
                obs_labels = group_data[LABEL].values
                pred_labels = np.zeros(len(entity_ids))
                # Current params
                Ve_cur = deepcopy(self.Ve)
                Vc_cur = deepcopy(self.Vc)
                Vf_cur = deepcopy(self.Vf)
                # Prediction phase
                for i in range(len(entity_ids)):
                    tar_index = entity_indices[i]
                    com_indices = [ind for ind in entity_indices if ind != tar_index]
                    x: np.ndarray = group_data.iloc[i][FEATURES]
                    pred_labels[i] = self._model_equation(tar_index, com_indices, x)
                # Param update phase
                pred_errors = obs_labels - pred_labels
                for i, pred_error in enumerate(pred_errors):
                    tar_index = entity_indices[i]
                    com_indices = [ind for ind in entity_indices if ind != tar_index]
                    x: np.ndarray = group_data.iloc[i][FEATURES]
                    coef_ve = diff.compute_diff_Iec_with_ve(com_indices, Vc_cur) + diff.compute_diff_Ief_with_ve(x, Vf_cur)
                    coef_vc = diff.compute_diff_Iec_with_vc(tar_index, Ve_cur)
                    coef_vf = diff.compute_diff_Ief_with_vf(tar_index, x, Ve_cur) + diff.compute_diff_Iff_with_vf(x, Vf_cur)
                    # Update params
                    self.b += self.eta * pred_error
                    self.w += self.eta * np.multiply(pred_error, x)
                    self.Ve[tar_index] += self.eta * np.multiply(pred_error, coef_ve)
                    self.Vc[com_indices] += self.eta * np.multiply(pred_error, coef_vc)
                    self.Vf += self.eta * np.multiply(pred_error, coef_vf)
                # Update epoch errors
                self.epoch_errors[epoch_idx] += np.sum(np.square(pred_errors))
            # Display epoch error
            if verbose:
                logger(self.epoch_errors[epoch_idx])
            # Randomize group order
            random.shuffle(group_ids)

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
