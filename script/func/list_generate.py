#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import datetime

from db_config import db_client

updated = {'$set': {'update': False}}
dataList = ['cv', 'circle', 'tag']
config = {
    'cv': {
        'update': {'doc': 'cv'},
        'res': '/opt/app/json/cv.json',
        'item': {"_id": 0, "name": 1},
    },
    'circle': {
        'update': {'doc': 'circle'},
        'res': '/opt/app/json/circle.json',
        'item': {"_id": 0, "name": 1},
    },
    'tag': {
        'update': {'doc': 'tag'},
        'res': '/opt/app/json/tag.json',
        'item': {"_id": 0, "value": 1},
    }
}

def main():
    client = db_client()
    db = client['onseidb']
    record = {}

    with open('/opt/app/log/log.txt', 'a', encoding='utf-8') as log:
        log.write(f'[{datetime.datetime.now()}] Update data list\n')

    with open('/opt/app/json/update.json', 'r', encoding='utf-8') as frecord:
        record = json.load(frecord)

    for key in dataList:
        if db['update'].find_one(config[key]['update'])['update']:
            with open(config[key]['res'], 'w', encoding='utf-8') as fp:
                results = list(db[key].find({}, config[key]['item']))
                json.dump(results, fp)
                db['update'].update_one(config[key]['update'], updated)
                record[key] = int(time.time())

    with open('/opt/app/json/update.json', 'w', encoding='utf-8') as frecord:
        json.dump(record, frecord)

if __name__ == '__main__':
    main()
