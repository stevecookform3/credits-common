#!/usr/bin/env python
# -*- coding: utf-8 -*-
from credits import transform
from credits import stringify
from credits import test

"""
In this example we create a basic "Balance Transfer" transform. We then use the credits.test.check_transform() to
validate that all expected attributes/methods/behaviours are provided.
"""

class BalanceTransform(transform.Transform):
    fqdn = "credits.test.BalanceTransform"

    def __init__(self, addr_from, addr_to, amount):
        self.addr_from = addr_from
        self.addr_to = addr_to
        self.amount = amount

    def marshall(self):
        return {
            "fqdn": self.fqdn,
            "addr_to": self.addr_to,
            "addr_from": self.addr_from,
            "amount": self.amount,
        }

    @classmethod
    def unmarshall(cls, registry, payload):
        return cls(
            addr_from=payload["addr_from"],
            addr_to=payload["addr_to"],
            amount=payload["amount"],
        )

    def verify(self, state):
        balances = state["credits.test.Balances"]

        if self.addr_from not in balances:
            return None, "%s not in credits.test.Balances."

        if balances[self.addr_from] < self.amount:
            return None, "%s does not have balance to make transfer."

        return None, None  # valid transaction

    def apply(self, state):
        try:
            balances = state["credits.test.Balances"]
            balances[self.addr_from] -= self.amount
            balances[self.addr_to] = balances.get(self.addr_to, 0) + self.amount  # addr_to might not exist.
            return state, None  # return the new state.

        except Exception as e:
            return None, e.args[0]  # Something went really wrong, don't apply.

    def hash(self, hash_provider):
        return hash_provider.hexdigest(stringify.stringify(self.marshall()))

