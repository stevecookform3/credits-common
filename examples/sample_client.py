#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from credits.key import ED25519SigningKey
from credits.address import CreditsAddressProvider
from credits.proof import SingleKeyProof
from credits.transaction import Transaction


# create a key for Alice using default key provider
alice_key = ED25519SigningKey.new()

# create Alice's address using default address provider
alice_address = CreditsAddressProvider(alice_key.to_string()).get_address()

# Saving the key to disk by marshalling it
with open("alice_key.json", "w") as out:
    out.write(alice_key.marshall()

# Loading it would be also simple when you'll need it
# with open("alice_key.json") as keyfile:
#    payload = json.load(keyfile)
#    alice_key = ED25519SigningKey.unmarshall(None, payload)

# create transform to send credits from Alice to Bob
transform = BalanceTransform(amount=100, addr_from=alice_address, addr_to="bob_address")

# sign the needed proof with Alice' key
proof = SingleKeyProof(alice_address, 1, transform.get_challenge()).sign(alice_key)

# form a transaction
transaction = Transaction(transform, {alice_address: proof})

# POST your transaction to the node in your network
requests.post("https://public.credits.works/api/v1/node/<your_node_name>/api/v1/transaction",
    headers={"Authorization": "<your_api_key>"},
    data={"transaction": json.dumps(transaction.marshall())}
)

