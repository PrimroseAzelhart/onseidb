# -*- coding: utf-8 -*-

import json
import aiohttp
import asyncio
from datetime import datetime

from db_config import db_client

sema = asyncio.Semaphore(20)
client = db_client()
db = client['onseidb']

failed = []

async def fetch(session, idList, log):
    async with sema:
        url = f'https://www.dlsite.com/maniax/product/info/ajax?product_id='
        for id in idList:
            url += id + ','
        async with session.get(url) as resp:
            if resp.status == 200:
                html = await resp.text()
                info = json.loads(html)
                for id in idList:
                    updateJson = {
                        'price_current': info[id]['price'],
                        'dl': info[id]['dl_count'],
                        'wish': info[id]['wishlist_count']
                    }
                    if info[id]['rate_average_2dp']:
                        updateJson['rate'] = info[id]['rate_average_2dp']
                    if len(info[id]['rank']) != 0:
                        updateJson['rank'] = info[id]['rank']
                        rankFirst = {'voice':[], 'all':[]}
                        for i in info[id]['rank']:
                            if i['rank'] == 1:
                                rankFirst[i['category']].append(i['term'])
                        if len(rankFirst['voice']) != 0 or len(rankFirst['all']) != 0:
                            updateJson['rank_first'] = rankFirst
                    
                    db['meta'].update_one({'id': id}, {'$set': updateJson})
                    log.write(f'[{datetime.now()}][success] {id}\n')
                await asyncio.sleep(1)
            else:
                failed.append({'id': id, 'status': 'failed'})
                log.write(f'[{datetime.now()}][fail:{resp.status}] {id}\n')

async def main(idGroup):
    with open('/opt/app/log/work.txt', 'a') as log:
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(fetch(session, idList, log)) for idList in idGroup]
            await asyncio.gather(*tasks)
            await session.close()
            db['id'].drop()
            if len(failed) != 0:
                db['id'].insert_many(failed)

def get_id_group():
    idList = []
    idGroup = []
    meta = db['meta'].find({}, {'_id': False})
    for work in meta:
        idList.append(work['id']) 
    for i in range(0, len(idList), 100):
        idGroup.append(idList[i:i+100])
    return idGroup

if __name__ == '__main__':
    idGroup = get_id_group()
    # print(idGroup)
    
    if len(idGroup) != 0:
        asyncio.run(main(idGroup))