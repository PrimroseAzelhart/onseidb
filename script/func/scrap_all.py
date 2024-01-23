# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import copy
import datetime
from bs4 import BeautifulSoup, NavigableString, Tag

from db_config import db_client

payload = {
    '_qf__fulltext_search':'',
    '_layout':'fs',
    '_site':'maniax',
    '_form_id':'FulltextSearchProductForm',
    '_view':'input',
    'from':'fs.detail',
    'keyword':'',
    'options_not[]':['AIG', 'AIP'],
    'discount_rates':'',
    'release_term':'',
    'price_category':'',
    'sales_conditions':'',
    'is_reserve':'',
    'options[]':['JPN', 'NM'],
    'work_type_category[]':'audio',
    'order':'release_d',
    'show_type':1,
    'per_page':100,
}

url = 'https://www.dlsite.com/maniax/fs'

sema = asyncio.Semaphore(2)
client = db_client()
col = client['onseidb']['id']

def get_date(tag: Tag):
    dateStr = tag.find(class_ = 'sales_date').get_text()
    return datetime.datetime.strptime(dateStr, '販売日: %Y年%m月%d日')

def get_age(tag: Tag):
    if tag.find(class_ = 'icon_GEN'):
        return 0
    if tag.find(class_ = 'icon_R15'):
        return 1
    return 2

def html_parser(html, fp):
    soup = BeautifulSoup(html, 'lxml')
    workList = soup.table.children
    doc = []
    for work in workList:
        if isinstance(work, NavigableString):
            continue
        id = work.div['data-product_id']
        title = work.div['data-work_name']
        circle = work.div['data-maker_id']
        price = work.div['data-official_price']
        date = get_date(work)
        age = get_age(work)
        fp.write(f'{id} {title} {circle} {price} {date}\n')
        doc.append({'code': id, 'titile': title, 'circle': circle, 'price': price, 'release_date': date, 'age': age})
    col.insert_many(doc)

async def scrap(session: aiohttp.ClientSession, fp, page):
    async with sema:
        payloadTmp = copy.deepcopy(payload)
        payloadTmp['page'] = page
        try:
            async with session.post(url, data=payloadTmp) as resp:
                print("Status:", resp.status)
                html = await resp.text()
                html_parser(html, fp)
        except:
            fp.write(f'Scrap page{page} failed')

async def main():
    async with aiohttp.ClientSession() as session:
        with open('/opt/app/log/results.txt', 'w') as res:
            tasks = [asyncio.ensure_future(scrap(session, res, page)) for page in range(1,2)]
            await asyncio.gather(*tasks)
            await session.close()

asyncio.run(main())
