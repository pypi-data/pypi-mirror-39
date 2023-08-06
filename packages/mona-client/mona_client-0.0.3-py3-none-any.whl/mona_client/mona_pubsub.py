from google.cloud import pubsub_v1
from . import mona_main_client


class MonaPublisherClient(pubsub_v1.PublisherClient):
    def publish(self, topic, data, **attrs):
        attrs = attrs or {}
        attrs['mona-id'] = mona_main_client.get_full_context_id()
        return super().publish(topic, data, **attrs)


def init_mona_from_pubsub_message(msg):
    """
    Inits current mona eontext to the context of the publisher of the given
    message. Considered part of the advanced api - do not use if you don't know
    what you are doing.
    """
    return mona_main_client.init(msg.attributes['mona-id'])


def with_mona_from_pubsub_message(msg):
    """
    Inits current mona eontext to the context of the publisher of the given
    message and returns the context manager.
    """
    return mona_main_client.new_mona_context(msg.attributes['mona-id'])
