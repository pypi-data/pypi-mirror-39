import collections
import logging

from django.conf import settings
from .connection import connection
from elasticsearch.exceptions import NotFoundError, ConnectionError
from elasticsearch_dsl import Search
from threading import Thread
from functools import wraps


logger = logging.getLogger(__name__)


def run_async(func):
    """
    run_async(func) function decorator, intended to make "func" run in a separate thread (asynchronously).

    :return: The created Thread object.
    """
    @wraps(func)
    def async_func(*args, **kwargs):
        run_func_async = kwargs.get('async', True)
        if not run_func_async:
            return func(*args, **kwargs)

        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl

    return async_func


def is_sync_feature_on():
    """
    Checks if Elasticsearch syncing (django -> ES) feature is on.

    :return: True if sync feature is on. Otherwise, False.
    """
    return settings.ES_SYNC_FEATURE


def create_mappings(classes):
    """
    Creates the indices in Elasticsearch with their mappings (schema) and
    adds autocomplete support to the specified fields.

    :param classes:
    :return: No return value (Void)
    """
    for Cls in classes:
        Cls.init()


def index_data(models, async=False):
    """
    Index all needed objects.

    :param models: Models that should be indexed.
    :param async: index data to Elasticsearch asynchronously.
    :return: No return value (Void)
    """
    for model in models:
        for obj in model.objects.all():
            try:
                if not obj.can_index():
                    continue
            except AttributeError:
                # In case instance doesn't have can_index function
                pass
            obj.indexing(new=True, async=async)


def update_nested_dict(orig_dict, new_dict):
    """
    Updates the orig_dict with nested.

    :param orig_dict: The original dict to update
    :param new_dict: A new dict to combine it with the orig_dict
    :return: A combined dict between orig_dict and new_dict
    """
    for key, val in new_dict.items():
        if isinstance(val, collections.Mapping):
            tmp = update_nested_dict(orig_dict.get(key, {}), val)
            orig_dict[key] = tmp
        elif isinstance(val, list):
            old_val = orig_dict.get(key, [])
            new_val = [v for v in val if v not in old_val]
            orig_dict[key] = old_val + new_val
        else:
            orig_dict[key] = new_dict[key]
    return orig_dict


@run_async
def index_obj(func, args, kwargs, async=True):
    """
    Indexes (create/update) object to Elasticsearch.

    :param func: indexing func that returns the fields dict
    :param args: args for func
    :param kwargs: kwargs for func
    :return: object as dict
    """
    attrs = {}
    IndexClass, new_attrs = func(*args, **kwargs)
    new_instance = kwargs.get('new', False)
    index_name = IndexClass._index._name

    try:
        if not new_instance:
            try:
                # If the object exists in Elasticsearch just update it
                es_obj = connection.get_connection().get(index=index_name, doc_type=IndexClass._doc_type.name,
                                                         id=new_attrs['meta']['id'])
                attrs = es_obj['_source']
            except NotFoundError:
                # The object doesn't exist in Elasticsearch so ignore this exception and a new object will be created.
                pass

        update_nested_dict(attrs, new_attrs)

        obj = IndexClass(**attrs)
        obj.save()
        return obj.to_dict(include_meta=True)

    except ConnectionError:
        # Log and return connection error when trying to connect to Elasticsearch with no luck.
        logging.error(
            'ES indexing failed for -> index_name: {} | object_id: {} '.format(index_name, new_attrs['meta']['id']))
        return {}


def es_indexing(func):
    """
    A decorator function that gets the attributes from 'indexing' function in the class model
    and syncs the object with Elasticsearch.

    :param func: The 'indexing' function
    :return: A dictionary that represents the synced object.
    """
    def func_wrapper(*args, **kwargs):
        if not is_sync_feature_on():
            return

        run_func_async = kwargs.get('async', True)
        return index_obj(func, args, kwargs, async=run_func_async)

    return func_wrapper


@run_async
def delete_es_document(document_id, index_name, async=True):
    """
    Deletes a document from Elasticsearch index.
    In case the deletion process is failed it will log an error.

    :param document_id: object id
    :param index_name: ES index name
    :param async: delete object from Elasticsearch asynchronously.
    :return: Void
    """
    if not is_sync_feature_on():
        return

    try:
        Search(index=index_name, using=connection.get_connection()).query('match', _id=str(document_id)).delete()
    except ConnectionError:
        logging.error('ES deleting failed for -> index_name: {} | object_id: {} '.format(index_name, document_id))
