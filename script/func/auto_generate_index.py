# -*- coding: utf-8 -*-

from db_config import db_client

def main():
    client = db_client()
    db = client['onseidb']

    # colList = ['cv', 'circle', 'series', 'author', 'scriptor', 'illustrator']
    cv = {}
    # circle = []
    # series = []
    # author = []
    # scriptor = []
    # illustrator = []
    cvDB = []

    for work in db['meta'].find():
        if 'cv' in work.keys():
            for i in work['cv']:
                if i in cv.keys():
                    cv[i].append(work['id'])
                else:
                    cv[i] = [work['id']]

    print(cv)
    for key, value in cv.items():
        cvDB.append({'name': key, 'work': value})

    db['cv'].insert_many(cvDB)

    # work = db['meta'].find_one()
    # print(work)

if __name__ == '__main__':
    main()
