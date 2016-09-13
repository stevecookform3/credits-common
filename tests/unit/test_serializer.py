#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import logbook
import pytest

from credits.serializer import JSONSerializer
from credits.serializer import MsgpackSerializer

logger = logbook.Logger(__name__)

@pytest.fixture("session")
def serializer_payload():
    return {
        "one": 1,
        "two": 2.0,
        "three": [
            1,
            2,
            {
                "one": 1,
                "two": 2,
                "three": 3,
            }
        ],
        "four": {
            "a": 1,
            "b": 2,
            "c": [3, "two", 1],
        }
    }


def test_json_serializer(serializer_payload):
    json = JSONSerializer()
    data = json.dumps(serializer_payload)

    assert isinstance(data, str)
    assert json.loads(data) == serializer_payload


def test_msgpack_serializer(serializer_payload):
    msgpack = MsgpackSerializer()
    data = msgpack.dumps(serializer_payload)

    assert isinstance(data, str)
    assert msgpack.loads(data) == serializer_payload
