from .connection import connection
from elasticsearch_dsl import Document, Object, Text, Keyword, Date, Integer, Boolean


class ESDocument(Document):

    type = Text()

    # filtration and sorting fields will be in these 'metadata'
    metadata = Object(properties={
        'filters': Object(properties={
            'type': Text(),
            'status': Text(),
            'visibility': Text(),
            'hidden': Boolean()
        }),
        'sorting': Object(properties={
            'name': Text(fields={'keyword': Keyword()}),
            'type': Text(fields={'keyword': Keyword()}),
            'start_date': Date(fields={'keyword': Keyword()}),
            'clicks': Integer(fields={'keyword': Keyword()})
        })
    })
