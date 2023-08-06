from elasticsearch_dsl import analyzer, token_filter


class Analyzer(object):
    """
    A class Aimed at analyzing specific language text.
    ES reference: https://www.elastic.co/guide/en/elasticsearch/reference/6.3/analysis-lang-analyzer.html
    """
    analyzer = None
    token_filters = None


class ArabicAnalyzer(Analyzer):
    token_filters = [
        'lowercase',
        'arabic_normalization',
        token_filter('arabic_stop', type='stop', stopwords='_arabic_'),
        token_filter('arabic_stemmer', type='stemmer', language='arabic')
    ]

    def __init__(self):
        self.analyzer = analyzer('arabic', tokenizer='standard', filter=self.token_filters)


arabic_analyzer = ArabicAnalyzer().analyzer
