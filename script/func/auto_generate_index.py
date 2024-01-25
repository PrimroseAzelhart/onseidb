# -*- coding: utf-8 -*-

from db_config import db_client


idx = ['circle', 'cv', 'series', 'author', 'scripter', 'illustrator']

client = db_client()
db = client['onseidb']

def update(index, count):
    existCount = db['update'].find_one({'doc': index})['count']
    if count != existCount:
        db['update'].update_one({'doc': index}, {'$set': {'update': True, 'count': count}})


def main():
    circle = {}
    cv = {}
    series = {}
    author = {}
    scripter = {}
    illustrator = {}

    circleDB = []
    cvDB = []
    seriesDB = []
    authorDB = []
    scripterDB = []
    illustratorDB = []

    for work in db['meta'].find():
        i = work['circle_id']
        if i in circle.keys():
            circle[i][1].append(work['id'])
        else:
            circle[i] = [work['circle'], [work['id']]]

        if 'cv' in work.keys():
            for i in work['cv']:
                if i in cv.keys():
                    cv[i].append(work['id'])
                else:
                    cv[i] = [work['id']]

        if 'series_id' in work.keys():
            i = work['series_id']
            if i in series.keys():
                series[i][1].append(work['id'])
            else:
                series[i] = [work['series'], [work['id']]]

        if 'author' in work.keys():
            for i in work['author']:
                if i in author.keys():
                    author[i].append(work['id'])
                else:
                    author[i] = [work['id']]

        if 'scripter' in work.keys():
            for i in work['scripter']:
                if i in scripter.keys():
                    scripter[i].append(work['id'])
                else:
                    scripter[i] = [work['id']]

        if 'illustrator' in work.keys():
            for i in work['illustrator']:
                if i in illustrator.keys():
                    illustrator[i].append(work['id'])
                else:
                    illustrator[i] = [work['id']]

    for key, value in circle.items():
        circleDB.append({'id': key, 'name': value[0], 'work': value[1], 'count': len(value[1])})

    for key, value in cv.items():
        cvDB.append({'name': key, 'work': value, 'count': len(value)})

    for key, value in series.items():
        seriesDB.append({'id': key, 'name': value[0], 'work': value[1], 'count': len(value[1])})

    for key, value in author.items():
        authorDB.append({'name': key, 'work': value, 'count': len(value)})

    for key, value in scripter.items():
        scripterDB.append({'name': key, 'work': value, 'count': len(value)})

    for key, value in illustrator.items():
        illustratorDB.append({'name': key, 'work': value, 'count': len(value)})

    for i in idx:
        db[i].drop()

    db['circle'].insert_many(circleDB)
    db['cv'].insert_many(cvDB)
    db['series'].insert_many(seriesDB)
    db['author'].insert_many(authorDB)
    db['scripter'].insert_many(scripterDB)
    db['illustrator'].insert_many(illustratorDB)

    update('circle', len(circleDB))
    update('cv', len(cvDB))
    update('series', len(seriesDB))
    update('author', len(authorDB))
    update('scripter', len(scripterDB))
    update('illustrator', len(illustratorDB))

if __name__ == '__main__':
    main()
