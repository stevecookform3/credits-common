#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import io

import logbook

from credits.config import Config
from credits.config import DictSource
from credits.config import JsonSource

logger = logbook.Logger(__name__)


def test_dict_source():
    config = Config()
    data = DictSource({
        "test": {
            "test": "test.test"
        }
    })
    config.add_source(data)

    assert config.get("test", "test") == "test.test"


def test_default():
    config = Config()
    data = DictSource({
        "test": {
            "test": "test.test"
        }
    })
    config.add_source(data)

    assert config.get("test", "missing", default="default") == "default"


def test_order_priority():
    config = Config()
    first = DictSource({
        "test": {
            "test": "first"
        }
    })
    second = DictSource({
        "test": {
            "test": "second"
        }
    })
    config.add_source(first)
    config.add_source(second)

    assert config.get("test", "test") == "second"


def test_type_converter():
    config = Config()
    data = DictSource({
        "test": {
            "test": "55"
        }
    })
    config.add_source(data)

    assert config.get("test", "test", int) == 55


def test_json():
    config = Config()
    json = io.StringIO(u"""{"test":{"test": "test"}}""")
    config.add_source(JsonSource(json))

    assert config.get("test", "test") == "test"
