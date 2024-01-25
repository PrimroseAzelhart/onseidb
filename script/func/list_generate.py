# -*- coding: utf-8 -*-

import json
import time
import datetime

from db_config import db_client

dataList = ['cv', 'circle', 'genre', 'author', 'scripter', 'illustrator', 'series']

def main():
    client = db_client()
    db = client['onseidb']
    record = {}

    with open('/opt/app/log/log.txt', 'a', encoding='utf-8') as log:
        log.write(f'[{datetime.datetime.now()}] Update data list\n')

    with open('/opt/app/json/update.json', 'r', encoding='utf-8') as frecord:
        record = json.load(frecord)

    for key in dataList:
        # If the list need update
        if db['update'].find_one({'doc': key})['update']:
            with open(f'/opt/app/json/{key}.json', 'w', encoding='utf-8') as fp:
                # Exclude the _id field
                results = list(db[key].find({}, {'_id': False, 'work': False}))
                # Dump the list to json file
                json.dump(results, fp)
                # Set the update field to false
                db['update'].update_one({'doc': key}, {'$set': {'update': False}})
                # Record the update time
                record[key] = int(time.time())

    with open('/opt/app/json/update.json', 'w', encoding='utf-8') as frecord:
        json.dump(record, frecord)

if __name__ == '__main__':
    main()
