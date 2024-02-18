# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import copy
from datetime import datetime
from bs4 import BeautifulSoup, NavigableString, Tag

from db_config import db_client
from ng import omit

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
    'options[]':['JPN'],
    'work_type_category[]':'audio',
    'order':'release_d',
    'show_type':1,
    'per_page':100,
}

url = 'https://www.dlsite.com/maniax/fs'

sema = asyncio.Semaphore(10)
client = db_client()
col = client['onseidb']['id']

def html_parser(html, fp):
    soup = BeautifulSoup(html, 'lxml')
    workList = soup.table.children
    doc = []
    for work in workList:
        if isinstance(work, NavigableString):
            continue
        circle = work.div['data-maker_id']
        if circle in omit['circle']:
            continue
        id = work.div['data-product_id']
        doc.append({'code': id})
    col.insert_many(doc)

async def fetch(session: aiohttp.ClientSession, fp, page):
    async with sema:
        payloadTmp = copy.deepcopy(payload)
        payloadTmp['page'] = page

        async with session.post(url, data=payloadTmp) as resp:
            if resp.status == 200:
                html = await resp.text()
                html_parser(html, fp)
                fp.write(f'{datetime.now()} Scrape page {page} done: {resp.status}\n')
                await asyncio.sleep(1)
            else:
                fp.write(f'{datetime.now()} Scrape page{page} failed\n')

async def main():
    async with aiohttp.ClientSession() as session:
        with open('/opt/app/log/scraper_id_log.txt', 'w') as res:
            tasks = [asyncio.ensure_future(fetch(session, res, page)) for page in range(1,500)]
            await asyncio.gather(*tasks)
            await session.close()

if __name__ == '__main__':
    asyncio.run(main())
