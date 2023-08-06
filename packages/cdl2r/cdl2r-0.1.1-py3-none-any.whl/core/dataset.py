# -*- coding: utf-8 -*-
"""Dataset used in models

Functions:
    load_data: Loading dataset from svm-light format txt file.
        Used in CDFM-models.
"""
import os
from typing import List
import numpy as np
import pandas as pd
from .constants import LABEL, QID, EID, FEATURES


def load_data(
        path: str,
        ndim: int,
        tokenizer: str = ' ',
        splitter: str = ':',
        zero_indexed: bool = False) -> pd.DataFrame:
    """Load dataset from a given path.

    label qid:123 eid:abc 1:1.5 2:0.2 4:-0.9 ...
    """
    if not os.path.isfile(path):
        FileNotFoundError(f'{path} not found.')
    rows: List[tuple] = []
    append_to_rows = rows.append

    def _parse(line: str) -> tuple:
        line = line.rstrip()
        tokens = line.split(tokenizer)
        label = np.float32(tokens[0])
        _, qid = tokens[1].split(splitter)
        _, eid = tokens[2].split(splitter)
        features = np.zeros(ndim, dtype=np.float32)
        for kv in tokens[3:]:
            nth_dim, raw_val = kv.split(splitter)
            dim_idx = int(nth_dim) if zero_indexed else int(nth_dim) - 1
            features[dim_idx] = np.float32(raw_val)
        return (label, qid, eid, features)

    with open(path, mode='r') as fp:
        line = fp.readline()
        while line:
            row = _parse(line)
            append_to_rows(row)
            line = fp.readline()

    return pd.DataFrame(rows, columns=(LABEL, QID, EID, FEATURES))
