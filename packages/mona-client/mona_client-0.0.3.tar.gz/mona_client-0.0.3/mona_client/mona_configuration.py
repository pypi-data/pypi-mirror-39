"""
Module in charge of providing updated configurations for the Mona client
according to a given configuration file under the env var
MONA_CLIENT_CONFIG_FILE.
"""
import json
import os
import atexit
import logging

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

_MONA_CLIENT_CONFIG_FILE_PATH = os.environ.get(
    'MONA_CLIENT_CONFIG_FILE') or './mona_client_config.json'

DEFAULT_CONFIGURATION = {'disable_all': False}

configuration = {}

LOGGER = logging.getLogger('mona-logger')


def _read_config_file():
    # TODO(itai): Consider getting host and port from config file as well.
    # Might not be something we want to enable (changing host and port during
    # run).
    LOGGER.info('Updating mona configiuration file.')
    global configuration
    configuration.update(DEFAULT_CONFIGURATION)
    try:
        with open(_MONA_CLIENT_CONFIG_FILE_PATH) as f:
            configuration.update(json.load(f))
            # TODO(itai): Log this action and the new state.
    except Exception:
        LOGGER.warning(
            "Couldn't read mona configuration file, using default "
            "configuration",
            exc_info=True)
    finally:
        LOGGER.info('New mona configuration: %s', str(configuration))


class _ConfigFileChangeHandler(PatternMatchingEventHandler):
    def __init__(self):
        super(_ConfigFileChangeHandler,
              self).__init__(patterns=[_MONA_CLIENT_CONFIG_FILE_PATH])

    def on_any_event(self, event):

        _read_config_file()


OBSERVER = Observer()
OBSERVER.schedule(
    _ConfigFileChangeHandler(),
    os.path.split(_MONA_CLIENT_CONFIG_FILE_PATH)[0],
    recursive=True)
OBSERVER.start()
atexit.register(OBSERVER.stop)

_read_config_file()
