# Ingesting geospatial data using Logstash
Logstash configuration for ingesting geospatial data to Elasticsearch 

## Logstash Installation (Ubuntu 18.04)
1- Download and install the Public Signing Key:
```
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
```
2- You may need to install the apt-transport-https package on Debian before proceeding:
```
sudo apt-get install apt-transport-https
```
3- Save the repository definition to /etc/apt/sources.list.d/elastic-7.x.list: (replace the elastic version accordingly)
```
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list
```
4- Run sudo apt-get update and the repository is ready for use. You can install it with:
```
sudo apt-get update && sudo apt-get install logstash
```
## Logstash Deployment (Ubuntu 18.04)

 Once installed, it is configured by default (unless specified) in the directory /usr/share/logstash.
To run the service change the current path to this directory and run following command : 
```
bin/logstash -f /path_to_config_file/config.conf
```
## Mapping Elastic indexes to appropiate data types 

It is often convinient to already map indexes to the appropiate data type (specially while indexing spatial data) so that while ingesting data using logstash, it doesn't dynamically map the location field and assume it to be of type - text. 

The file create_index_mapping.py creates indexes and maps the field data type as specified.

Number of columns and data types can  be changed according to the requirements   
```
from elasticsearch import Elasticsearch

es=Elasticsearch(['http://localhost9200'])

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
```


## Configuration for transferring csv files containing spatial information 

Elasticsearch supports two spatial data types : geo_point and geo_shape.
For indexing data containing lat, long info in a csv file, mutate filter plugin is used  for converting and merging the lat, long information and adding a new location field with geo_point data type in the output index. (Refer to csv_configuration.conf file for the code)  

```
input {
  file {
    path => "/path/logs.csv"
    start_position => "beginning"
    sincedb_path => "/dev/null"
  }
}

filter {
 csv {
     separator => ","
    columns => ["doc_id","lat","long","timestamp"]
  }
mutate {
         add_field => { "[location][lat]" => "%{lat}" }
         add_field => { "[location][lon]" => "%{long}" }
         remove_field => [ "lat", "long" ]
  
       }

}

output {

elasticsearch {
        hosts => "localhost:9200"
        index => "api_logs_1"
        document_id => "%{doc_id}"
#        document_type => "my_type"
        user => "username"
        password => "password"
        }


}
```

## Configuration for directly indexing PostgreSQL data 
 
 1- Download the PostgreSQL JDBC Driver from PostgreSQL
 
 2- Make sure to install jbdc plugin to allow logstash to communicate with the PostgreSQL database
 
 3- Alter the jbdc string and driver path in the postgres_to_elastic.conf configuration
 
 3- Alter HOST IP and table/index name according to requirements in postgres_to_elastic.conf configuration
 
 4- Run the command in Logstash deployment section with the modified configuration file as an input
 
 ```
 jdbc {
tags => "table_name1"
jdbc_driver_class => "org.postgresql.Driver"
jdbc_connection_string => "jdbc:postgresql://POSTGRES_IP:5432/TPLMaps"
jdbc_user => "username"
jdbc_password => "postgreSQL_password"
jdbc_default_timezone => "Asia/Karachi"
statement => "SELECT * from table_name where id in
(select feature_id from postgres_logs where operation_time>:sql_last_value )  "
tracking_column_type => "timestamp"
#To run the config at specific time, set the schedule
#schedule => "00 05 * * *"
}

jdbc {
tags => "table_name2"
jdbc_driver_class => "org.postgresql.Driver"
jdbc_connection_string => "jdbc:postgresql://POSTGRES_IP:5432/TPLMaps"
jdbc_user => "username"
jdbc_password => "postgreSQL_password"
jdbc_default_timezone => "Asia/Karachi"
statement => "SELECT * from table_name where id in
(select feature_id from postgres_logs where operation_time>:sql_last_value )  "
tracking_column_type => "timestamp"
#schedule => "00 05 * * *"
}

jdbc {
tags => "table_name3"
jdbc_driver_class => "org.postgresql.Driver"
jdbc_connection_string => "jdbc:postgresql://POSTGRES_IP:5432/TPLMaps"
jdbc_user => "username"
jdbc_password => "postgreSQL_password"
jdbc_default_timezone => "Asia/Karachi"
statement => "SELECT * from table_name where id in
(select feature_id from postgres_logs where operation_time>:sql_last_value )  "
tracking_column_type => "timestamp"
#schedule => "00 05 * * *"
}


filter {

if "table_name1" in [tags] or "table_name2" in [tags] or "table_name3" in [tags] 
 {
mutate {
         add_field => { "[location][lat]" => "%{lat}" }
         add_field => { "[location][lon]" => "%{long}" }
       }
}


}

output {

if "table_name1" in [tags] {

elasticsearch {
        hosts => "ELASTIC_IP_ADDRESS:9200"
        index => "house"
#       document_type => "my_type"
        document_id => "%{id}"
        user => "input_elastic_user"
        password => "input_elastic_pass"
        }
}

else if "table_name2" in [tags] {
elasticsearch {
        hosts => "ELASTIC_IP_ADDRESS:9200"
        index => "house"
#       document_type => "my_type"
        document_id => "%{id}"
        user => "input_elastic_user"
        password => "input_elastic_pass"
        }
}

else if "table_name3" in [tags] {
elasticsearch {
        hosts => "ELASTIC_IP_ADDRESS:9200"
        index => "house"
#       document_type => "my_type"
        document_id => "%{id}"
        user => "input_elastic_user"
        password => "input_elastic_pass"
        }
}



}

 ```
