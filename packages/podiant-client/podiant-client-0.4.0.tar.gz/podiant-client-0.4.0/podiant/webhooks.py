from .api import Client
from .exceptions import UnknownError
import json


class WebhookMetaCollection(object):
    def __init__(self, data):
        for key, value in data.items():
            setattr(self, key, value)


class Webhook(object):
    def __init__(self, stream):
        data = json.loads(stream.decode('utf-8'))

        self.meta = WebhookMetaCollection(
            data.get('meta', {})
        )

        try:
            client = Client(data['meta']['access_token'])
            assert data['type'] == 'events'
            self.id = data['id']

            obj = data['attributes'].pop('object')
            assert 'type' in obj
            assert 'id' in obj

            collection = getattr(client, obj['type'])
            self.object = collection.filter(id=obj['id'])

            for key, value in data['attributes'].items():
                setattr(self, key, value)
        except (AssertionError, KeyError):
            raise UnknownError(
                'Data does not conform to expected Webhook object.'
            )
