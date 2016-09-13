#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import pytest

from credits.merkle import MerkleMap


def test_default():
    m = MerkleMap.from_dict({"test": 100}, 0)
    assert m["non_existant"] == 0
    assert m["test"] == 100
    m["non_existant"] += 100
    assert m["non_existant"] == 100
