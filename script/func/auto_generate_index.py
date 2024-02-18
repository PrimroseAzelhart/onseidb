# -*- coding: utf-8 -*-

import json
from db_config import db_client
from datetime import datetime

circleDB = []
cvDB = []
seriesDB = []
authorDB = []
scripterDB = []
illustratorDB = []
genreDB = []

idx = {'circle': circleDB, 'cv': cvDB, 'series': seriesDB, 'author': authorDB, 'scripter': scripterDB, 'illustrator': illustratorDB, 'genre': genreDB}

client = db_client()
db = client['onseidb']

def main():
    circle = {}
    cv = {}
    series = {}
    author = {}
    scripter = {}
    illustrator = {}
    genre = {}

    for work in db['meta'].find({}, {'_id': False}):
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

        if 'genre' in work.keys():
            for i in range(len(work['genre'])):
                if work['genre_id'][i] in genre.keys():
                    genre[work['genre_id'][i]][1].append(work['id'])
                else:
                    genre[work['genre_id'][i]] = [work['genre'][i], [work['id']]]

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

    for key, value in genre.items():
        genreDB.append({'id': key, 'value': value[0], 'work': value[1], 'count': len(value[1])})

    for i,v in idx.items():
        db[i].drop()
        db[i].insert_many(v)
        db['field'].update_one({'index': i}, {'$set': {'last_update': datetime.now().timestamp()}}, True)
        with open(f'/opt/app/json/{i}.json', 'w', encoding='utf-8') as fp:
            results = db[i].find({}, {'_id': False, 'work': False})
            results = sorted(results, key=lambda e:e.__getitem__('count'), reverse=True)
            json.dump(results, fp)

if __name__ == '__main__':
    main()
