#!/usr/env python3
import json
import requests

URL = 'http://localhost:9098/ksql'
HEADERS = {'Content-Type': 'application/json'}
DATA = {'streamsProperties': {}}
QUERIES = [
    # --- Main
    "CREATE STREAM pageviews_original (viewtime bigint, userid varchar, pageid varchar) WITH (kafka_topic='pageviews', value_format='DELIMITED');",
    "CREATE TABLE users_original (registertime bigint, gender varchar, regionid varchar, userid varchar) WITH (kafka_topic='users', value_format='JSON', key = 'userid');",

    # --- Page views by users
    "CREATE TABLE POBYUSER1S AS SELECT USERID, COUNT(*) AS PO_COUNT FROM PAGEVIEWS_ORIGINAL WINDOW TUMBLING (SIZE 1 SECOND) GROUP BY USERID;",
    "CREATE TABLE POBYUSER1M AS SELECT USERID, COUNT(*) AS PO_COUNT FROM PAGEVIEWS_ORIGINAL WINDOW TUMBLING (SIZE 1 MINUTE) GROUP BY USERID;"

    # --- Page views trend
    "CREATE STREAM PAGEVIEWS_ORIGINAL2 AS SELECT 1 AS FOO,* FROM PAGEVIEWS_ORIGINAL;",
    "CREATE TABLE PO1S AS SELECT FOO, COUNT(*) AS PO_COUNT FROM PAGEVIEWS_ORIGINAL2 WINDOW TUMBLING (SIZE 1 SECOND) GROUP BY FOO;",
    "CREATE TABLE PO1M AS SELECT FOO, COUNT(*) AS PO_COUNT FROM PAGEVIEWS_ORIGINAL2 WINDOW TUMBLING (SIZE 1 MINUTE) GROUP BY FOO;"
]


for query in QUERIES:
    DATA['ksql'] = query
    splits = query.split(" ")
    req = requests.post(url=URL, headers=HEADERS, data=json.dumps(DATA))

    print('Creating {}: {}'.format(splits[1], splits[2]))

    if req.status_code == 200:
        if 'errorMessage' in req.text:
            print(json.loads(req.text)[0]['error']['errorMessage']['message'])
        else:
            print("Done")
    print('-------------')
