"""
A module for handling reqeusts with mona contexts in wsgi apps.
"""
from . import mona_main_client


class MonaMiddleware():
    """
    A wsgi middleware for initing the mona context according to the context in
    the received request.
    """

    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response):
        with mona_main_client.new_mona_context(environ.get("HTTP_MONA_ID")):
            return self._app(environ, start_response)
