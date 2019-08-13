import time
from elasticsearch import Elasticsearch


class DeleteObsolete:
    def __init__(self):
        self.connection = Elasticsearch('elasticsearch', port=9200)

    def get_indexes(self):
        list_of_indexes = list(self.connection.indices.get_alias("*"))
        list_of_indexes.sort(reverse=True)
        base_indexes = set(i.split('-')[0] for i in list_of_indexes if len(i.split('-')) > 1)
        return list_of_indexes, base_indexes

    def get_to_delete(self, list_of_indexes, base_indexes):
        to_delete = []
        for base_name in base_indexes:
            to_delete += self.get_to_delete_for_single_base(base_name, list_of_indexes)
        return to_delete

    def get_to_delete_for_single_base(self, base_name, list_of_indexes):
        indexes = []
        for al in list_of_indexes:
            if al.startswith(base_name):
                indexes.append(al)
        return indexes[3:]

    def delete_indexes(self, to_delete):
        for i in to_delete:
            self.connection.indices.delete(index=i, ignore=[400, 404])
        return to_delete

    def run(self):
        try:
            to_delete = self.get_to_delete(*self.get_indexes())
            return self.delete_indexes(to_delete)
        except Exception as e:
            return e


if __name__ == '__main__':
    while True:
        instance = DeleteObsolete()
        result = instance.run()
        print('Deleted following indexes:', result)
        time.sleep(60)
