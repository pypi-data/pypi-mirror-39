#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The Downloader internal Module."""
import tarfile
import requests
from .cloudevent import CloudEvent
from .cartapi import CartAPI
from .policy import TransactionInfo


class Downloader(object):
    """Downloader Class."""

    def __init__(self, location, cart_api_url, **kwargs):
        """Create the downloader given directory location."""
        self.location = location
        self.auth = kwargs.get('auth', {})
        self.cart_api = CartAPI(cart_api_url, auth=self.auth)

    def _download_from_url(self, cart_url, filename):
        """Download the cart from the url."""
        resp = requests.get(
            '{}?filename={}'.format(cart_url, filename),
            stream=True, **self.auth
        )
        cart_tar = tarfile.open(name=None, mode='r|', fileobj=resp.raw)
        cart_tar.extractall(self.location)
        cart_tar.close()

    def transactioninfo(self, transinfo, filename='data'):
        """Handle transaction info and download the cart."""
        self._download_from_url(
            self.cart_api.wait_for_cart(
                self.cart_api.setup_cart(
                    TransactionInfo.yield_files(transinfo)
                )
            ),
            filename
        )

    def cloudevent(self, cloudevent, filename='data'):
        """Handle a cloudevent and return a cart url."""
        self._download_from_url(
            self.cart_api.wait_for_cart(
                self.cart_api.setup_cart(
                    CloudEvent.yield_files(cloudevent)
                )
            ),
            filename
        )
