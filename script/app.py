# -*- coding: utf-8 -*-

# Main backend application

import json
import bcrypt
import datetime
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from func.db_config import db_client

application = Flask(__name__)
CORS(application)

client = db_client()
responseField = {'_id': False, 'circle_id': False, 'series_id': False, 'genre_id': False}

postDataField = ['id', 'title', 'circle[id]', 'cv[]', 'age', 'rel_date', 'rel_after', 'rel_before', 'genre[]', 'series[id]', 'scripter[name]', 'illustrator[name]']

def postDataParser(data):
    postData = {}
    for i in postDataField:
        if i == 'cv[]' or i == 'genre[]':
            d = data.getlist(i)
            if len(d) != 0:
                postData[i] = d
        else:
            d = data.get(i)
            if d:
                postData[i] = d
    return postData

@application.route("/")
def index():
    return '<p>Hello world!</p>'

@application.route('/login', methods=['POST'])
def login():
    user = request.values.get('username')
    pwd = request.values.get('password').encode(encoding='utf-8')
    id = ''
    if ((user == None) or (pwd == None)):
        code = 1
    else:
        result = client['onseidb']['user'].find_one({"username": user})
        if result == None:
            code = 2
        else:
            hashed = result['password'].encode(encoding='utf-8')
            if not bcrypt.checkpw(pwd, hashed):
                code = 3
            else:
                code = 0
                id = str(result['_id'])

    response = {'code': code, 'id': id}
    return jsonify(response)

@application.route('/query', methods=['POST'])
def query():
    data = postDataParser(request.values)
    if 'id' in data.keys():
        results = list(client['onseidb']['meta'].find({'id': data['id']}, responseField))
        return jsonify(results)
    querySentence = {}
    if 'title' in data.keys():
        querySentence['title'] = {'$regex': f'{data["title"]}'}
    if 'circle[id]' in data.keys():
        querySentence['circle_id'] = data['circle[id]']
    if 'cv[]' in data.keys():
        querySentence['cv'] = {'$in': []}
        for i in data['cv[]']:
            querySentence['cv']['$in'].append(i)
    if 'age' in data.keys():
        querySentence['age'] = {'$in': []}
        for i in data['age']:
            querySentence['age']['$in'].append(i)
    if 'rel_date' in data.keys():
        date = datetime.datetime.strptime(data['rel_date'][0:10], '%Y-%m-%d')
        querySentence['release_date'] = date
    if 'rel_after' in data.keys():
        date = datetime.datetime.strptime(data['rel_after'][0:10], '%Y-%m-%d')
        querySentence['release_date'] = {}
        querySentence['release_date']['$gte'] = date
    if 'rel_before' in data.keys():
        date = datetime.datetime.strptime(data['rel_before'][0:10], '%Y-%m-%d')
        if 'release_date' not in querySentence.keys():
            querySentence['release_date'] = {}
        querySentence['release_date']['$lte'] = date
    if 'genre[]' in data.keys():
        querySentence['genre_id'] = {'$in': []}
        for i in data['genre[]']:
            querySentence['genre_id']['$in'].append(i)
    if 'series[id]' in data.keys():
        querySentence['series_id'] = data['series[id]']
    if 'scripter[name]' in data.keys():
        querySentence['scripter'] = {'$in': [data['scripter[name]']]}
    if 'illustrator[name]' in data.keys():
        querySentence['illustrator'] = {'$in': [data['illustrator[name]']]}
    results = list(client['onseidb']['meta'].find(querySentence, responseField))
    return jsonify(results)


@application.route('/search', methods=['POST'])
def search():
    results = list(client['onseidb']['meta'].find({}, responseField))
    return jsonify(results)

@application.route('/list/<key>')
def get_list(key):
    try:
        with open(f'/opt/app/json/{key}.json', 'r') as fp:
            return jsonify(json.load(fp))
    except:
        abort(404)

if __name__ == '__main__':
    application.run()
