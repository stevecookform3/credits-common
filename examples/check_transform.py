#!/usr/bin/env python
# -*- coding: utf-8 -*-
from credits import transform
from credits import stringify
from credits import test

from balance_transform.py import BalanceTransform


# Construct the Transform with these.
kwargs = {
    "addr_from": "alice_address",
    "addr_to": "bob_address",
    "amount": 100,
}

# This is an initial state that both verify and apply will use
state = {
    "credits.test.Balances": {
        "alice_address": 1000,
    }
}

# This is how state should look after the Transform has applied to it.
state_expected = {
    "credits.test.Balances": {
        "alice_address": 900,
        "bob_address": 100,  # This key is added as a result of transform.apply()
    }
}

# This call should succeed without assertion errors or exceptions
test.check_transform(
    cls=BalanceTransform,
    dependencies=[],
    kwargs=kwargs,
    state=state,
    state_expected=state_expected,
)
