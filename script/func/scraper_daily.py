# -*- coding: utf-8 -*-

import aiohttp
import asyncio
from datetime import datetime
from bs4 import BeautifulSoup
# from db_config import db_client

def html_parser(html):
    soup = BeautifulSoup(html, 'lxml')

async def main():
    date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://www.dlsite.com/maniax/new/=/date/{date}/work_type_category/voice/show_layout/1'
    with open('/opt/app/log/daily', 'a') as log:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp != 200:
                    print('failed')
                    return
                html = await resp.text()
                html_parser(html)

if __name__ == '__main__':
    asyncio.run(main())
