import sys
from elasticsearch import Elasticsearch


class Search:
    _query_phrase = ''
    _index = 'post*'
    _fields = ['name', 'text']
    size = 10
    from_ = 0

    def __init__(self):
        self.connection = Elasticsearch('elasticsearch', port=9200)

    def set_query(self, query_phrase):
        self._query_phrase = query_phrase

    def run(self):
        index = self._get_index()
        query = self._form_query()
        results = self.connection.search(index=index, body=query,
                                         size=self.size, from_=self.from_)
        return self._clean_results(results)

    def _get_index(self) -> str:
        list_of_indices = list(self.connection.indices.get_alias(self._index))
        list_of_indices.sort(reverse=True)
        return list_of_indices[1]

    def _clean_results(self, results: dict):
        clean_results = [hit['_source'] for hit in results['hits']['hits']]
        return clean_results

    def _form_query(self) -> dict:
        return {
            'query': {
                'bool': {
                    'should': [
                        {
                            'query_string': {
                                'fields': self._fields,
                                'query': self._query_phrase,
                                'analyzer': 'english',
                                'default_operator': 'AND',
                            }
                        },
                        {
                            'query_string': {
                                'fields': self._fields,
                                'query': self._query_phrase,
                                'analyzer': 'standard',
                                'default_operator': 'AND',
                            }
                        }
                    ]
                }
            }
        }


if __name__ == '__main__':
    query = sys.argv[1]
    search = Search()
    if len(sys.argv) > 3:
        search.size = sys.argv[3]
    if len(sys.argv) > 2:
        search.from_ = sys.argv[2]
    search.set_query(query)
    result = search.run()
    print(result)
