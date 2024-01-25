# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import json
from db_config import db_client

client = db_client()
db = client['onseidb']

async def main():
    genres = []
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.dlsite.com/maniax/fs/=/api_access/1') as resp:
            if resp.status == 200:
                text = await resp.text()
                options = json.loads(text)
                for category in options['genre_all']:
                    for genre in category['values']:
                        genres.append(genre)

    db['genre'].drop()
    db['genre'].insert_many(genres)
    db['update'].update_one({'doc': 'genre'}, {'$set': {'update': True, 'count': len(genres)}})

if __name__ == '__main__':
    asyncio.run(main())
