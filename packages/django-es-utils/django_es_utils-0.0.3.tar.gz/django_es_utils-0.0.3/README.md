# Elasticsearch Utilities
Elasticsearch utilities for Django projects to analyze queries, create documents, sync data and connect to ES.

# Required configurations
Add the following configurations to Django project settings:
- `ES_SYNC_FEATURE` (**Required:** Boolean)
- `ELASTICSEARCH_HOST` (**Required:** String)
- `ELASTICSEARCH_USERNAME` (**Optional:** String)
- `ELASTICSEARCH_PASSWORD` (**Optional:** String)

# Syncing data with Elasticsearch

#### Steps to index a Django model into Elasticsearch:

1- create a new file inside any Django app called `es_indices.py` and insert this code into it with your modifications:

```python3
from es_utils.analyzers import arabic_analyzer
from es_utils.document import ESDocument
from elasticsearch_dsl import (
    connections,
    Document,
    Text,
    Completion
)


class ProgramIndex(ESDocument):
    """
    This class is used to map the programs with Elasticsearch index.
    """

    class Index:
        name = 'programs'
    
    # the fields you want to index with their types
    
    id = Text()
    
    # support autocomplete for this field
    name_en = Text(fields={'completion': Completion()})
    
    # add arabic analyzer to this field
    about_ar = Text(analyzer=arabic_analyzer)
    about_en = Text()
   
    # nested object
    category = Object(properties={
        'name_en': Text(),
        'name_ar': Text()
    })
    
    # ...
    # ...

```

2- Add the `indexing` function to your model in `models.py` file:

```python3
from cms.djangoapps.program.es_indices import ProgramIndex
from es_utils.helpers import es_indexing


class Program(models.Model):
    name_en = models.CharField(max_length=255)
    about_en = models.CharField(max_length=255)
    ..
    ..
    
    # It's optional to add 'async' arg.
    @es_indexing
    def indexing(self, async=True):
        attrs = dict(
            meta={'id': self.id},
            metadata={
                'filters': {'type': self.program_type, 'status': self.status},
                'sorting': {'name': self.name_en, 'type': self.program_type, 'start_date': self.start}
            },
            id=self.id,
            slug=self.slug,
            name_en=self.name_en,
            type=self.program_type,
            about_en=self.about_en,
            
            # nested dict
            category=dict(
                name_en=self.category.name_en,
                name_ar=self.category.name_ar
            ),
        )
        return ProgramIndex, attrs
```

3- Add a `post_save` and `post_delete` signals and connect them with the model:
```python3
from cms.djangoapps.program.models import Program
from cms.djangoapps.program import es_indices
from django.db.models.signals import post_save, post_delete
from elasticsearch_dsl import Search
from es_utils.connection import connection
from es_utils.helpers import delete_es_document


def index_program(sender, instance, created, **kwargs):
    if instance.can_index():
        instance.indexing(new=created, async=True)
    elif not created:
        index_name = es_indices.ProgramIndex._index._name
        delete_es_document(document.id, index_name, async=True)


def delete_program(sender, instance, **kwargs):
    index_name = es_indices.ProgramIndex._index._name
    delete_es_document(instance.id, index_name, async=True)


for cls_name in settings.ES_SYNC_MODELS:
    Cls = getattr(models, cls_name)
    signals.post_save.connect(index_program, sender=Cls)
    signals.post_delete.connect(delete_program, sender=Cls)

```


# Compatibility
- Django >= 1.8.
- Python3.
