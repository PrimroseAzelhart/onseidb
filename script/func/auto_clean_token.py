# -*- coding: utf-8 -*-

from db_config import db_client
from datetime import datetime

client = db_client()
users = client['onseidb']['user']

def main():
    current = datetime.now()
    for user in users.find({}, {'_id': False}):
        expiredTokens = []
        tokens = user['token']
        for token,expiration in tokens.items():
            if current > expiration:
                expiredTokens.append(token)
        for token in expiredTokens:
            tokens.pop(token)
        users.update_one({'username': user['username']}, {'$set': {'token': tokens}})

if __name__ == '__main__':
    main()
