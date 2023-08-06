# -*- coding: utf-8 -*-
"""Type annotation used in models.
"""
from typing import Dict, Union


GroupID = Union[int, str]
EntityID = Union[int, str]
EntIndMap = Dict[EntityID, int]
