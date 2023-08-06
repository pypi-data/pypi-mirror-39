"""
A wrapper for the commonly used "requests" module to send out requests
containing mona contexts.
"""
from . import mona_main_client
import importlib

SPEC = importlib.util.find_spec('requests')
requests = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(requests)

orig_request = requests.request


def _add_mona_id_to_kwargs(kwargs):
    kwargs.setdefault('headers', {})
    kwargs['headers']['mona-id'] = mona_main_client.get_full_context_id()


def _wrapped_request(method, url, **kwargs):
    _add_mona_id_to_kwargs(kwargs)
    return orig_request(method, url, **kwargs)


class MonaSession(requests.Session):
    def request(self, method, url, **kwargs):
        _add_mona_id_to_kwargs(kwargs)
        return super(MonaSession, self).request(method, url, **kwargs)


requests.Session = MonaSession

requests.request = _wrapped_request

# See https://github.com/requests/requests/blob/master/requests/api.py for
# reference on the requests.api patched below.


def _get(url, params=None, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return _wrapped_request('get', url, params=params, **kwargs)


requests.get = _get


def _options(url, **kwargs):
    kwargs.setdefault('allow_redirects', True)
    return _wrapped_request('options', url, **kwargs)


requests.options = _options


def _head(url, **kwargs):
    kwargs.setdefault('allow_redirects', False)
    return _wrapped_request('head', url, **kwargs)


requests.head = _head


def _post(url, data=None, json=None, **kwargs):
    return _wrapped_request('post', url, data=data, json=json, **kwargs)


requests.post = _post


def _put(url, data=None, **kwargs):
    return _wrapped_request('put', url, data=data, **kwargs)


requests.put = _put


def _patch(url, data=None, **kwargs):
    return _wrapped_request('patch', url, data=data, **kwargs)


requests.patch = _patch


def _delete(url, **kwargs):
    return _wrapped_request('delete', url, **kwargs)


requests.delete = _delete