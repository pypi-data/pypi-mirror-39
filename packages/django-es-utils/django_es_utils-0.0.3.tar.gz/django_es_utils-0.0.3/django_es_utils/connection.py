import sys

from django.conf import settings
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import connections
from .mock import FakeElasticsearch


def is_testing():
    if len(sys.argv) < 2:
        return False
    return sys.argv[1] == 'test'


class Connection(object):
    def __init__(self):
        try:
            self._conn = connections.get_connection(alias='default')
        except KeyError:
            # if there is no existing connection create new one
            if is_testing():
                # fake Elasticsearch with unittests
                self._conn = FakeElasticsearch()
                connections.add_connection(alias='default', conn=self._conn)
            else:
                try:
                    http_auth = {'http_auth': (settings.ELASTICSEARCH_USERNAME, settings.ELASTICSEARCH_PASSWORD,)} \
                        if settings.ELASTICSEARCH_USERNAME else {}
                except AttributeError:
                    http_auth = {}
                self._conn = connections.create_connection(alias='default', hosts=[settings.ELASTICSEARCH_HOST],
                                                           **http_auth)

    def get_connection(self):
        return self._conn

    def get_object(self, index, doc_type, id, **kwargs):
        try:
            return self._conn.get(index=index, doc_type=doc_type, id=id, **kwargs)
        except NotFoundError:
            return {}


connection = Connection()
