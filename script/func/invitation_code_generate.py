# -*- coding: utf-8 -*-

from db_config import db_client
import secrets

client = db_client()
codesCollection = client['onseidb']['invitation_code']
count = 10

def main():
    codes = []
    for i in range(count):
        code = secrets.token_hex(16)
        codes.append({'code': code})
    codesCollection.insert_many(codes)

if __name__ == '__main__':
    main()
