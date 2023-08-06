from elasticsearch.client.utils import query_params
from elasticmock.utilities import get_random_id
from elasticmock.fake_elasticsearch import FakeElasticsearch as BaseFakeElasticsearch


class Transport(object):
    def perform_request(self, *args, **kwargs):
        pass


# overrides index function in FakeElasticsearch class
class FakeElasticsearch(BaseFakeElasticsearch):

    transport = Transport()

    @query_params('consistency', 'op_type', 'parent', 'refresh', 'replication',
                  'routing', 'timeout', 'timestamp', 'ttl', 'version', 'version_type')
    def index(self, index, doc_type, body, id=None, params=None):
        if index not in self.__documents_dict:
            self.__documents_dict[index] = list()

        if id is None:
            id = get_random_id()

        version = 1

        self.__documents_dict[index].append({
            '_type': doc_type,
            '_id': id,
            '_source': body,
            '_index': index,
            '_version': version
        })

        return {
            '_type': doc_type,
            '_id': id,
            'created': True,
            'result': 'created',
            '_version': version,
            '_index': index
        }
