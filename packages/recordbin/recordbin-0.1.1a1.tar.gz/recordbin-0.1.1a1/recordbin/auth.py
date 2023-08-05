"""
Recordbin Request Authentication.

This class is used internally by requests to authenticated all calls.
`__call__` will be called on all requests to ensure token is injected into requests header.
"""

from __future__ import absolute_import
import requests


class RecordBinAuth(requests.auth.AuthBase):
    def __init__(self, token):
        """
        Authentication

        Args:
            token (``str``): Auth Token. Optional.
                If not set, it will look for
                environment variable ``RECORDBIN_TOKEN``
        """
        self.token = token

    def __call__(self, request):
        auth_token = {"Authorization": "AppToken {}".format(self.token)}
        request.headers.update(auth_token)
        return request
