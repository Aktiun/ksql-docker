# KSQL Docker

This docker-compose will start the confluent platform (4.1.0), ksql server (4.1.0) and nginx as a reverse proxy for ksql through port 9098.

It will automatically start the data generators for users and pageviews.


## Running

1. Run `docker-compose up -d` to start the CP, ksql, ngnix and data generators. 
2. Create the tables and stream by running `python3 streams.py`. Usually the script have to be executed only once. It will notify if the streams and tables are allready created nevertheless.


## Troubleshoot:

#### Some of the servers (kafka, ksql-server...) are failing or attempting to reboot

1. Stop the docker-compose execution (Ctrl+C)
2. Make no server is running with `docker-compose ps`
3. If the status of any of them is `up` then execute `docker-compose stop`
4. Try running again


#### Python3 cannot find module 'requests' when running streams.py

If this happens it means that you need to install the module by using `pip3 install requests` or any other python3 package manager you are using.

#### Errors when executing streams.py

Make sure all servers are running and data is being generated correctly. You can use a REST client (like Postman) to test the connection to the KSQL api to check if is working.

1. Test through nginx port first: http://localhost:9098
2. Test directly kafka server port: http://localhost:8088
