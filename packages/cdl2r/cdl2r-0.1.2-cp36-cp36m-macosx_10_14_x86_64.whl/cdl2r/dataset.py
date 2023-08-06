# -*- coding: utf-8 -*-
"""Dataset used in models

Functions:
    load_data: Loading dataset from svm-light format txt file.
        Used in CDFM-models.
"""
import os
from operator import itemgetter
from typing import Iterable, List
import numpy as np
import pandas as pd
from .constants import LABEL, QID, EID, FEATURES


def load_data(
        path: str,
        ndim: int,
        tokenizer: str = ' ',
        splitter: str = ':',
        comment_symb: str = '#',
        zero_indexed: bool = False) -> pd.DataFrame:
    """Load dataset from a given path.

    label qid:123 eid:abc 1:1.5 2:0.2 4:-0.9 ...
    """
    if not os.path.isfile(path):
        FileNotFoundError(f'{path} not found.')
    rows: List[tuple] = []
    append_to_rows = rows.append

    def _extract_first(iterable: Iterable[str]) -> str:
        first_item = itemgetter(0)
        return first_item(iterable)

    def _parse(line: str) -> tuple:
        line = line.rstrip()
        elems = _extract_first(line.split(comment_symb))
        tokens = elems.split(tokenizer)
        label = float(tokens[0])
        _, qid = tokens[1].split(splitter)
        _, eid = tokens[2].split(splitter)
        features = np.zeros(ndim, dtype=np.float64)
        for kv in tokens[3:]:
            nth_dim, raw_val = kv.split(splitter)
            dim_idx = int(nth_dim) if zero_indexed else int(nth_dim) - 1
            features[dim_idx] = np.float64(raw_val)
        return (label, qid, eid, features)

    with open(path, mode='r') as fp:
        line = fp.readline()
        while line:
            row = _parse(line)
            append_to_rows(row)
            line = fp.readline()

    return pd.DataFrame(rows, columns=(LABEL, QID, EID, FEATURES))
