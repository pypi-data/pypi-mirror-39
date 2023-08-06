#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Cart API module for interacting with carts."""
import logging
from uuid import uuid4 as uuid
import time
from json import dumps
import requests


class CartAPI(object):
    """Cart api object for manipulating carts."""

    def __init__(self, cart_api_url, **kwargs):
        """Constructor for cart api."""
        self.cart_api_url = cart_api_url
        self.session = kwargs.get('session', requests.Session())

    def setup_cart(self, yield_files):
        """Setup a cart from the cloudevent object return url to the download."""
        cart_url = '{}/{}'.format(self.cart_api_url, uuid())
        resp = self.session.post(
            cart_url,
            data=dumps({
                'fileids': [file_obj for file_obj in yield_files()]
            }),
            headers={'Content-Type': 'application/json'}
        )
        assert resp.status_code == 201
        return cart_url

    def wait_for_cart(self, cart_url, timeout=120):
        """Wait for cart completion to finish."""
        while timeout > 0:
            resp = self.session.head(cart_url)
            resp_status = resp.headers['X-Pacifica-Status']
            resp_message = resp.headers['X-Pacifica-Message']
            resp_code = resp.status_code
            if resp_code == 204 and resp_status != 'staging':
                break
            if resp_code == 500:  # pragma: no cover
                logging.error(resp_message)
                break
            time.sleep(1)
            timeout -= 1
        assert resp_status == 'ready'
        assert resp_code == 204
        return cart_url
