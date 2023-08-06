"""
A module for handling multithreading with mona contexts.
"""

from threading import Thread
from . import mona_main_client

# TODO(itai): Add support for asyncio and greentlets if users require those.


class MonaThread(Thread):
    """
    A thread which takes care of using the same mona context as its parent
    thread.
    """

    def __init__(self, group=None, target=None, *args, **kwargs):
        self._full_context_id = ""

        def new_target(*args, **kwargs):
            with mona_main_client.new_mona_context(self._full_context_id):
                target(*args, **kwargs)

        super().__init__(group=group, target=new_target, *args, **kwargs)

    def start(self):
        self._full_context_id = mona_main_client.get_full_context_id()
        super().start()
