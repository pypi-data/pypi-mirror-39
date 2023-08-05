"""

RecordBin Class
***********************

>>> recordbin = RecordBin(url='http://ww-recordbin.herokuapp.com', token='authtoken')
>>> recordbin.post(data={})
{'id':'12345-5678-534343', 'data': {'Column': 'Value'}, ...}

For more information on Token Auth see :doc:`authentication`.

"""

import requests
from concurrent.futures import ThreadPoolExecutor

from .auth import RecordBinAuth
from .hooks import response_hook


class RecordBin:

    API_VERSION = "v1"

    @property
    def api_url(self):
        return f"{self.base_url}/api/{self.API_VERSION}"

    @property
    def record_post_url(self):
        return f"{self.api_url}/records/"

    def __init__(self, url, token):
        """
        Args:
            url(``str``): Url of RecordBin (eg. http://ww-recordbin.herokuapp.com/)
            token(``str``): Valid RecordBin Token (eg. '1a23b5-5c67d8-12af31e2424')
        """
        session = requests.Session()
        session.post
        session.auth = RecordBinAuth(token=token)
        session.hooks["response"] = [response_hook]
        self.base_url = url
        self.session = session

    def _post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    def post(self, data):
        """
        Creates a new RecordBin Record

        >>> response = recordbin.post(data={'username': 'gtalarico'})
        >>> record = response.result()

        Args:
            data(``dict``): RecordBin Payload. Must be a python dictionary.

        Returns:
            response (``future``): Python concurrent.futures.Future Class.
                This allows call to run async. To get result you can pool for
                simply call ``response.result(timeout=5)`` which wait up to 5 seconds
                and then return the Response Object.

        """
        url = self.record_post_url
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self._post, url=url, json=data)
        return future
