# -*- coding: utf-8 -*-

import re
import json
import aiohttp
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
from db_config import db_client

sema = asyncio.Semaphore(20)
client = db_client()
db = client['onseidb']
fileFormat = []
failed = []

with open("/opt/app/json/option.json", 'r', encoding='utf-8') as fp:
    option = json.load(fp)
    for f in option['options_all']['file_format']:
        fileFormat.append(f['text'])

def html_parser(html):
    soup = BeautifulSoup(html, 'lxml')

    doc = {}
    doc['last_scrape'] = datetime.now()
    doc['id'] = soup.find(id='work_buy_box_wrapper')['data-product-id']
    doc['title'] = soup.find(id='work_name').text.strip()
    doc['circle'] = soup.find(class_='add_follow')['data-follow-name']
    doc['circle_id'] = soup.find(class_='add_follow')['data-follow-key']
    doc['price'] = int(soup.find(id='work_buy_box_wrapper').div['data-official_price'])

    table = soup.find(id='work_outline')

    for row in table.find_all('tr'):
        if row.th.text == '販売日':
            dateStr =  re.search(r'[2].+日', row.td.text.strip()).group()
            doc['release_date'] = datetime.strptime(dateStr, '%Y年%m月%d日')
            continue
        if row.th.text == '更新情報':
            doc['last_update'] = datetime.strptime(row.td.contents[0].strip(), '%Y年%m月%d日')
            continue
        if row.th.text == 'シリーズ名':
            doc['series'] = row.td.text.strip()
            try:
                doc['series_id'] = re.search(r'SRI[0-9]+', row.a['href']).group()
            except:
                pass
            continue
        if row.th.text == '作者':
            doc['author'] = []
            for tag in row.td.find_all('a'):
                doc['author'].append(tag.text.strip())
            continue
        if row.th.text == 'シナリオ':
            doc['scripter'] = []
            for tag in row.td.find_all('a'):
                doc['scripter'].append(tag.text.strip())
            continue
        if row.th.text == 'イラスト':
            doc['illustrator'] = []
            for tag in row.td.find_all('a'):
                doc['illustrator'].append(tag.text.strip())
            continue
        if row.th.text == '声優':
            doc['cv'] = []
            for tag in row.td.find_all('a'):
                doc['cv'].append(tag.text.strip())
            continue
        if row.th.text == '音楽':
            doc['music'] = []
            for tag in row.td.find_all('a'):
                doc['music'].append(tag.text.strip())
            continue
        if row.th.text == '年齢指定':
            age = row.span['class'][0]
            if age == 'icon_GEN':
                doc['age'] = 0
            elif age == 'icon_R15':
                doc['age'] = 1
            else:
                doc['age'] = 2
            continue
        if row.th.text == 'ファイル形式':
            doc['format'] = []
            format = row.td.text.strip()
            for f in fileFormat:
                if re.search(f, format, re.IGNORECASE):
                    doc['format'].append(f)
            continue
        if row.th.text == 'イベント':
            doc['event'] = row.td.text.strip()
            continue
        if row.th.text == 'ジャンル':
            doc['genre'] = []
            doc['genre_id'] = []
            for tag in row.td.find_all('a'):
                try:
                    gid = re.search(r'[0-9]+', tag['href']).group()
                    doc['genre_id'].append(gid)
                    genre = tag.text.strip()
                    doc['genre'].append(genre)
                except:
                    print(doc['id'])
            continue
        if row.th.text == 'ファイル容量':
            doc['size'] = re.search(r'([0-9].+B)', row.td.text.strip()).group()
            continue
    return doc

async def fetch(session, id, log):
    async with sema:
        url = f'https://www.dlsite.com/maniax/work/=/product_id/{id}.html'
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    html = await resp.text()
                    try:
                        doc = html_parser(html)
                        log.write(f'[{datetime.now()}][success] {id}')
                        db['meta'].update_one({'id': doc['id']}, {'$set': doc}, True)
                    except:
                        log.write(f'[{datetime.now()}][fail: parser] {id}')
                    await asyncio.sleep(1)
                else:
                    failed.append({'id': id, 'status': 'failed'})
                    log.write(f'[{datetime.now()}][fail:{resp.status}] {id}\n')
        except:
            log.write(f'[{datetime.now()}][fail] {id}\n')

def get_id_list():
    idList = []
    idDB = db['id'].find({}, {'_id': False})
    for id in idDB:
        idList.append(id['code'])
    return idList

async def main(idList):
    with open('/opt/app/log/scraper_work_log.txt', 'a') as log:
        log.write(f'\n[{datetime.now()}] Scraper start\n')
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.ensure_future(fetch(session, id, log)) for id in idList]
            await asyncio.gather(*tasks)
            await session.close()
            db['id'].drop()
            if len(failed) != 0:
                db['id'].insert_many(failed)
            log.write(f'[{datetime.now()}] Scraper finish\n')

if __name__ == '__main__':
    idList = get_id_list()
    if len(idList) != 0:
        asyncio.run(main(idList))
