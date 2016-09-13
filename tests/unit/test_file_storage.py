#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

import datetime
import json
import os
import shutil

import pytest

from credits.block import Block
from credits.merkle import MerkleMap
from credits.proof import SingleKeyProof
from credits.serializer import JSONSerializer
from credits.state import State
from credits.storage import FileStorage
from credits.transaction import Transaction
from credits.transform import BalanceTransferTransform


@pytest.fixture("session")
def storage_path():
    return "./tmp_storage"


@pytest.fixture
def storage(request, storage_path, serializer):
    request.addfinalizer(lambda: shutil.rmtree(storage_path))
    return FileStorage(storage_path, serializer)


@pytest.fixture
def state0input():
    return {"foo": 0, "bar": 1, "baz": 2}

@pytest.fixture
def state0output():
    return {
        "fqdn": "works.credits.core.State",
        "height": 0,
        "previous_block_hash": None,
        "states": {
            "works.credits.test.MockState": {
                "fqdn": "works.credits.core.MerkleMap",
                "pointers": {
                    "bar": 0,
                    "baz": 1,
                    "foo": 2
                },
                "values": [
                    1,
                    2,
                    0
                ]
            }
        }
    }

@pytest.fixture
def state0hash():
    return "5d9c9421102d01eb76b1566ec03c19cf5292f24e65affb2a4fce943417cdba84"


@pytest.fixture
def block0output():
    return {
        "commits": {},
        "fqdn": "works.credits.core.Block",
        "height": 0,
        "previous_commits": {},
        "state_hash": "5d9c9421102d01eb76b1566ec03c19cf5292f24e65affb2a4fce943417cdba84",
        "timestamp": "1991-12-02T00:00:00",
        "transactions": [
            {
                "fqdn": "works.credits.core.Transaction",
                "proofs": {
                    "foo": {
                        "address": "foo",
                        "challenge": "bar",
                        "fqdn": "works.credits.core.SingleKeyProof",
                        "nonce": 0,
                        "signature": None,
                        "verifying_key": None
                    }
                },
                "transform": {
                    "amount": 10,
                    "fqdn": "works.credits.core.BalanceTransform.1.0.0",
                    "from_address": "foo",
                    "to_address": "bar"
                }
            }
        ]
    }


@pytest.fixture
def state(state0input):
    merkle_map = MerkleMap.from_dict(state0input)

    state = State(0, None)
    state.register_state("works.credits.test.MockState", merkle_map)

    return state


@pytest.fixture
def block0hash():
    return "f21ed20f783a295ecdbbe755991828a3425afec07003d943fea7545c4f27f6bb"


@pytest.fixture
def block(state, hash_provider):
    state_hash = state.hash(hash_provider)
    timestamp = datetime.datetime(1991, 12, 2)
    transactions = [
        Transaction(
            transform=BalanceTransferTransform("foo", "bar", 10),
            proofs={
                "foo": SingleKeyProof("foo", 0, "bar"),
            },
        )
    ]
    return Block(0, state_hash, timestamp, transactions, None)


def test_storage_state_write(hash_provider, storage, storage_path, state, state0output):
    # Dump state to disk.
    storage.set_state(state, hash_provider)

    # Read from tmp storage and assert dumped json is expected.
    with open(os.path.join(storage_path, "state_00000000000000000000000000000000.json")) as f:
        raw_state = json.loads(f.read())

    assert raw_state == state0output


def test_storage_state_write_crash_on_existing(hash_provider, storage, state):
    # Dump state to disk.
    storage.set_state(state, hash_provider)

    with pytest.raises(Exception):
        storage.set_state(state, hash_provider)  # Raises exception because file already exists.


def test_storage_state_read(registry, hash_provider, state, storage, state0output):
    # Dump state to disk.
    storage.set_state(state, hash_provider)

    # Recover it.
    assert storage.get_state_by_height(registry, 0).marshall() == state0output
    assert storage.get_state_by_height(registry, -1).marshall() == state0output


def test_storage_state_read(registry, hash_provider, state, storage, state0output, state0hash):
    # Dump state to disk.
    storage.set_state(state, hash_provider)

    # Recover it.
    assert storage.get_state_by_hash(registry, state0hash).marshall() == state0output


def test_storage_state_read_crash_on_nonexistant_state(registry, storage):
    # Recover it.
    with pytest.raises(IOError):
        storage.get_state_by_height(registry, 9001)  # IOError, this file doesn't exist.


def test_storage_block_write(hash_provider, storage, storage_path, block, block0output):
    # Dump block to disk.
    storage.set_block(block, hash_provider)

    # Read from tmp storage and assert dumped json is expected.
    with open(os.path.join(storage_path, "block_00000000000000000000000000000000.json")) as f:
        raw_block = json.loads(f.read())

    assert raw_block == block0output


def test_storage_block_write_crash_on_existing(hash_provider, storage, block):
    # Dump block to disk.
    storage.set_block(block, hash_provider)

    with pytest.raises(Exception):
        storage.set_block(block, hash_provider)  # Raises exception because file already exists.


def test_storage_block_read(registry, hash_provider, block, storage, block0output):
    # Dump block to disk.
    storage.set_block(block, hash_provider)

    # Recover it.
    assert storage.get_block_by_height(registry, 0).marshall() == block0output
    assert storage.get_block_by_height(registry, -1).marshall() == block0output


def test_storage_block_read_crash_on_nonexistant_block(registry, storage):
    # Recover it.
    with pytest.raises(IOError):
        storage.get_block_by_height(registry, 9001)  # IOError, this file doesn't exist.


def test_storage_block_read(registry, hash_provider, block, storage, block0output, block0hash):
    # Dump block to disk.
    storage.set_block(block, hash_provider)

    # Recover it.
    assert storage.get_block_by_hash(registry, block0hash).marshall() == block0output
