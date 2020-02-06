import logging
import json
import psycopg2
from elasticsearch import Elasticsearch

conn = psycopg2.connect(database ="db_name", user="username", password= "password", host="localhost", port="xxxx")

#change the ES host and port accordingly
es=Elasticsearch(['http://localhost9200'])
#Delete indices if already exist 

'''es.indices.delete(index='index1', ignore=[400, 404])
es.indices.delete(index='index2', ignore=[400, 404])
es.indices.delete(index='index3', ignore=[400, 404])
es.indices.delete(index='index4', ignore=[400, 404])'''

if es.ping():
    print('Connected to Elasticsearch')
else:
    print('Could not be connected!')
es.indices.create(index='index_name', body={
   'settings' : {
         'index' : {
              'number_of_shards':2
         }
   }
})
es.indices.put_mapping(
    index="index_name",
    doc_type="_doc",
    include_type_name=True,
    body={
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "@version": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "location_column": {
                    "type": "geo_point"},

                "column1_name": {
                    "type": "date"
                },
                "column2_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "column3_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "column4_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }

        }})

es.indices.create(index='index2_name', body={
   'settings' : {
         'index' : {
              'number_of_shards':2
         }
   }
})
es.indices.put_mapping(
    index="index2_name",
    doc_type="_doc",
    include_type_name=True,
    body={
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "@version": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "location_column": {
                    "type": "geo_point"},

                "column1_name": {
                    "type": "date"
                },
                "column2_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "column3_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "column4_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }

        }})
es.indices.create(index='index3_name', body={
   'settings' : {
         'index' : {
              'number_of_shards':2
         }
   }
})
es.indices.put_mapping(
    index="index_name3",
    doc_type="_doc",
    include_type_name=True,
    body={
            "properties": {
                "@timestamp": {
                    "type": "date"
                },
                "@version": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "location_column": {
                    "type": "geo_point"},

                "column1_name": {
                    "type": "date"
                },
                "column2_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "column3_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                },
                "column4_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                        }
                    }
                }

        }})


