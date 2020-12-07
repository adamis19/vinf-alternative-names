from elasticsearch import Elasticsearch
import csv
from elasticsearch import helpers


def search(name):
    es = Elasticsearch(HOST="http/localhost", PORT=9200)
    es = Elasticsearch()

    body = {
        "query": {
            "multi_match": {
                "query": name,
                "type": "phrase",
                "fields": ["body.name", "body.alt_names"]
            }
        }}

    res = es.search(index="alt_names_index", body=body)

    if len(res["hits"]["hits"]) > 0:
        for i in range(0, len(res["hits"]["hits"])):
            print(res["hits"]["hits"][i]["_source"]["body"]["name"] + ": " + res["hits"]["hits"][i]["_source"]["body"]["alt_names"] + "\n")
    else:
        print("no results")


def create_index():
    es = Elasticsearch(HOST="http/localhost", PORT=9200)
    es = Elasticsearch()
    es.indices.delete(index="alt_names_index", ignore=[400, 404])

    alt_names_file = csv.reader(open("../alternative_names.csv", "r", encoding="utf-8"), delimiter='\t')
    i = -1
    actions = []
    for row in alt_names_file:
        i += 1
        action = {
            "_index": "alt_names_index",
            "doc_type": 'post',
            "id": i,
            "body": {
                "name": row[0],
                "alt_names": row[1]
            }}
        actions.append(action)
        if i % 10000 == 0 and i != 0:
            helpers.bulk(es, actions, request_timeout=70)
            actions = []

    print(es.get(index='alt_names_index', id=1))
