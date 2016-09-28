#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function

from hashlib import sha256

import logbook
from base58 import b58encode

logger = logbook.Logger(__name__)


class AddressProvider(object):
    """
    AddressProvider is an abstraction allowing any string to be converted into an "Address".
    Address should have hash like properties of providing deterministic output for a given input and being
    non-reversable.
    """

    def get_address(self):
        raise NotImplementedError()


class CreditsAddressProvider(AddressProvider):
    def __init__(self, value):
        """
        An AddressProvider using an in-house algorithm based off double sha256 and base58 encoding.

        :type input_str: str
        """
        self.value = value

    def get_address(self):
        """
        Generate an address from self.input_str. This is typically performed using a verifying key.

        :rtype: str
        """
        # Py2/3
        value = self.value
        if not isinstance(value, bytes):
            value = value.encode()

        digest = b"\x00" + sha256(value).digest()[:20]
        checksum = sha256(digest).digest()[:4]
        address = digest + checksum

        return b58encode(address)
