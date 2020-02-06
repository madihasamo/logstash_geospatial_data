# logstash_geospatial_data
Logstash configuration for ingesting geospatial data to Elasticsearch 

## Logstash Installation (Ubuntu 18.04)
1- Download and install the Public Signing Key:

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

2- You may need to install the apt-transport-https package on Debian before proceeding:

sudo apt-get install apt-transport-https

3- Save the repository definition to /etc/apt/sources.list.d/elastic-7.x.list: (replace the elastic version accordingly)

echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

4- Run sudo apt-get update and the repository is ready for use. You can install it with:

sudo apt-get update && sudo apt-get install logstash

## Logstash Deployment (Ubuntu 18.04)

 Once installed, it is configured by default (unless specified) in the directory /usr/share/logstash
To run the service change the current path to the this directory and run following command : 

bin/logstash -f /path_to_config_file/config.conf

## Configuration for transferring csv files containing spatial information 

Elasticsearch supports two spatial data types : geo_point and geo_shape.
For indexing data containing lat, long info in a csv file, mutate filter plugin is used  for converting and merging the lat, long information and adding a new location field with geo_point data type in the output index. (Refer to csv_configuration.conf file for the code)  

## Configuration for directly indexing PostgreSQL data 
 
 1- Download the PostgreSQL JDBC Driver from PostgreSQL
 
 2- Make sure to install jbdc plugin to allow logstash to communicate with the PostgreSQL database
 
 3- Alter the jbdc string and driver path in the postgres_to_elastic.conf configuration
 
 3- Alter HOST IP and table/index name according to requirements in postgres_to_elastic.conf configuration
 
 4- Run the command in Logstash deployment section with the modified configuration file as an input
