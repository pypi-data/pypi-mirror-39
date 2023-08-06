"""
The main Mona python client module. Exposes all functions relevant for client
handling, mainly including context configuration and exporting mechanism.
"""
# TODO(itai): Consider adding capability for several context ids in parallel,
# allowing exporting to several ARCs.

import atexit
import os
import logging
import uuid
from contextlib import contextmanager

from fluent import asyncsender as sender
from werkzeug.local import Local, LocalManager
from .mona_configuration import configuration

CONTEXT_SEPARATOR = '.'

MONA_HOST = os.environ.get('MONA_HOST') or 'localhost'
MONA_PORT = os.environ.get('MONA_PORT') or 24224
MONA_USER_ID = os.environ['MONA_USER_ID']

sender.setup('mona.client', host=MONA_HOST, port=MONA_PORT)

_GLOBAL_SENDER = sender.get_global_sender()

# TODO(itai): Also support asyncio with context variables. This only handles
# threads and greenlets.
_LOCAL = Local()
_LOCAL_MANAGER = LocalManager([_LOCAL])
_LOCAL.contexts = []

_LOCAL.protected_contexts = []
"""
List of sub_contexts indices (to map to LOCAL.contexts) currently opened with a
context manager and that should therefore never be manually closed.

This is done to assure that if you are in a "with" block, you can be certain
that the context you opened in the "with" statement is still open.
"""

_LOGGER = logging.getLogger('mona-logger')

_global_init_message = {}
"""A message to be sent on each new main context after init."""


def _get_local_list_attr(name):
    return getattr(_LOCAL, name, [])


def _get_protected_contexts():
    return _get_local_list_attr('protected_contexts')


def _get_contexts():
    return _get_local_list_attr('contexts')


def _set_protected_contexts(new_id):
    amount_of_contexts = new_id.count(CONTEXT_SEPARATOR) + 1
    start_from_index = len(_LOCAL.contexts) - amount_of_contexts
    _LOCAL.protected_contexts = _get_protected_contexts() + list(
        range(start_from_index, start_from_index + amount_of_contexts))
    return amount_of_contexts


@contextmanager
def new_mona_context(context_id=''):
    """Returns a new context manager for a head context"""
    reset()
    init(context_id)

    _set_protected_contexts(context_id)

    try:
        yield get_full_context_id()

    finally:
        _LOCAL.contexts = []
        _LOCAL.protected_contexts = []


@contextmanager
def new_mona_sub_context(context_id=''):
    """Returns a new context manager for a sub_context"""
    if configuration['disable_all']:
        yield ''
        return
    context_id = init_sub_context(context_id)
    _set_protected_contexts(context_id)

    try:
        yield context_id

    finally:
        # Remove this sub-context and all its sub-contexts from protected
        first_sub_context = _get_split_contexts(context_id)[0]
        sub_context_index = _LOCAL.contexts.index(first_sub_context)
        _LOCAL.protected_contexts = [
            x for x in _get_protected_contexts() if x < sub_context_index
        ]

        # Now close it.
        close_sub_context(context_id.split(CONTEXT_SEPARATOR)[0])


def get_full_context_id():
    """
    Returns the full context id for the current ARC. This is a string
    containing the main context id and all the sub context ids delimited by
    CONTEXT_SEPARATOR.
    """
    return CONTEXT_SEPARATOR.join(_get_contexts())


def _get_split_contexts(full_id):
    return full_id.split(CONTEXT_SEPARATOR)


def _set_contexts_from_string(contexts_string):
    """
    Sets the current contexts according to the given string, or using a uuid if
    no string was provided.
    """
    if contexts_string:
        _LOCAL.contexts = _get_split_contexts(contexts_string)
    else:
        _LOCAL.contexts = [str(uuid.uuid1())]


def init(contexts_string=''):
    """
    Inits the current context with a new context, completely forgetting the old
    contexts (like when using reset()).
    NOTE: Considered part of the advanced API. Use new_mona_context unless you
    know what you are doing.
    """
    if configuration['disable_all']:
        return ''
    if _get_protected_contexts():
        raise Exception("Tried to init inside a context manager")

    _set_contexts_from_string(contexts_string)
    _LOGGER.info('Mona context after initing: %s', get_full_context_id())

    if _global_init_message:
        export(_global_init_message)

    return get_full_context_id()


def init_sub_context(sub_context_id=''):
    """
    Inits a new sub context, with the given name if provided, or a uuid if not.
    NOTE: Considered part of the advanced API. Use new_mona_sub_context unless
    you know what you are doing.
    """
    if configuration['disable_all']:
        return ''
    if not _LOCAL.contexts:
        raise Exception("Tried to create subcontext before init")
    sub_context_id = sub_context_id or str(uuid.uuid1())
    _LOCAL.contexts = _get_contexts() + _get_split_contexts(sub_context_id)
    _LOGGER.info('Mona context after initing sub context: %s',
                 get_full_context_id())
    return sub_context_id


def close_sub_context(sub_context_id=''):
    """
    Closes the given sub context, or the last one if none is provided.
    NOTE: Considered part of the advanced API. Use new_mona_sub_context unless
    you know what you are doing.
    """
    if configuration['disable_all']:
        return ''
    sub_context_index = _LOCAL.contexts.index(
        sub_context_id) if sub_context_id else len(_LOCAL.contexts) - 1
    if sub_context_index < 1:
        raise Exception("Tried to close non-existing subcontext")

    if sub_context_index <= max(_get_protected_contexts()):
        raise Exception(
            """Tried to close sub context from within it's own context. \
            When using a context manager ('with statement') close is \
            triggered implicitly...""")

    _LOCAL.contexts = _LOCAL.contexts[:sub_context_index]

    _LOGGER.info('Mona context after closing sub context: %s',
                 get_full_context_id())

    return get_full_context_id()


def export(message):
    """
    This funciton holds the main funtionality of the client. Using any json
    message as the input parameter, this function will send out the message to
    Mona's systems.
    """
    if configuration['disable_all']:
        return
    if not _LOCAL.contexts:
        raise Exception('Tried to export out of context')
    _LOGGER.info('Exporting mona message')
    _GLOBAL_SENDER.emit(
        'message', {
            'user_id': MONA_USER_ID,
            'context': get_full_context_id(),
            'message': message
        })


def reset():
    """
    Resets the client to hold no context.
    NOTE: Considered part of the advanced API. Use new_mona_context unless you
    know what you are doing.
    """
    if configuration['disable_all']:
        return

    _LOGGER.info('reseting mona context to empty')
    _LOCAL.contexts = []


def set_global_init_message(message):
    """
    Sets a message to be exported to mona for every inited main context. This
    is useful, for example, for sending mona environment data, such as telling
    mona all ARCs created are of the testing environment.
    """
    global _global_init_message
    _global_init_message = message


atexit.register(sender.close)
