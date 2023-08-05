import contextlib
import requests
import warnings
import logging
from urllib3.exceptions import InsecureRequestWarning

logger = logging.getLogger(__name__)

try:
    from functools import partialmethod
except ImportError:
    class partialmethod(partial):
        def __get__(self, instance, owner):
            if instance is None:
                return self
            return partial(self.func, instance, *(self.args or ()), **(self.keywords or {}))

@contextlib.contextmanager
def disable_ssl_verification(session=requests.Session):
    logger.warn('Disabling SSL verification')
    originalRequest = session.request
    session.request = partialmethod(originalRequest, verify=False)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', InsecureRequestWarning)
        yield
    session.request = originalRequest