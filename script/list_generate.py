#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from db_config import mongoUri

updated = {'update': False}
doc = {
    'cv': {'doc': 'cv'},
    'circle': {'doc': 'circle'},
    'tag': {'doc': 'tag'}
}

def main():
    client = MongoClient(mongoUri, server_api = ServerApi('1'))
    db = client['onseidb']
    record = {}

    with open('/opt/app/log.txt', 'a', encoding='utf-8') as log:
        log.write(f'[{datetime.datetime.now()}] Update data list\n')

    with open('update_record.json', 'r', encoding='utf-8') as frecord:
        record = json.load(frecord)

    if db['update'].find_one(doc['cv'])['update']:
        with open('/opt/app/cv.json', 'w', encoding='utf-8') as fcv:
            results = list(db['cv'].find({}, {"_id": 0, "name": 1}))
            json.dump(results, fcv)
            db['update'].update_one(doc['cv'], {'$set': updated})
            record['cv'] = int(time.time())

    if db['update'].find_one({'doc': 'circle'})['update']:
        with open('/opt/app/circle.json', 'w', encoding='utf-8') as fcircle:
            results = list(db['circle'].find({}, {"_id": 0, "name": 1}))
            json.dump(results, fcircle)
            db['update'].update_one(doc['circle'], {'$set': updated})
            record['circle'] = int(time.time())

    if db['update'].find_one({'doc': 'tag'})['update']:
        with open('/opt/app/tag.json', 'w', encoding='utf-8') as ftag:
            results = list(db['tag'].find({}, {"_id": 0, "value": 1}))
            json.dump(results, ftag)
            db['update'].update_one(doc['tag'], {'$set': updated})
            record['tag'] = int(time.time())

    with open('update_record.json', 'w', encoding='utf-8') as frecord:
        json.dump(record, frecord)

if __name__ == '__main__':
    main()
