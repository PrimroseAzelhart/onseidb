# -*- coding: utf-8 -*-

# Main backend application

import json
import bcrypt
import datetime
import secrets
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from func.db_config import db_client

application = Flask(__name__)
CORS(application)

client = db_client()
responseField = {'_id': False, 'circle_id': False, 'series': False, 'series_id': False, 'genre_id': False,
                'rank': False, 'author': False, 'scripter': False, 'music': False, 'size': False, 'wish': False,
                'format': False, 'illustrator': False}

detailField = {'_id': False}

postDataField = ['id', 'title', 'circle[id]', 'cv[]', 'age[]', 'rel_date[]',
                'genre[]', 'series[id]', 'scripter[name]', 'illustrator[name]']

listFiled = ['cv[]', 'genre[]', 'age[]', 'rel_date[]']

def postDataParser(data):
    postData = {}
    for i in postDataField:
        if i in listFiled:
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
                token = secrets.token_hex(32)
                expiration = datetime.datetime.now() + datetime.timedelta(days=1)
                result['token'].append({token: expiration})
                client['onseidb']['user'].replace_one({'username': user}, result)

    if code != 0:
        response = {'code': code}
    else:
        response = {'code': code, 'user': user, 'token': token}

    return jsonify(response)

@application.route('/query', methods=['POST'])
def query():
    data = postDataParser(request.values)
    if len(data) == 0:
        abort(400)
    if 'id' in data.keys():
        results = list(client['onseidb']['meta'].find({'id': data['id']}, responseField))
        return jsonify(results)
    querySentence = {}
    if 'title' in data.keys():
        querySentence['title'] = {'$regex': f'{data["title"]}'}
    if 'circle[id]' in data.keys():
        querySentence['circle_id'] = data['circle[id]']
    if 'cv[]' in data.keys():
        querySentence['cv'] = {'$all': []}
        for i in data['cv[]']:
            querySentence['cv']['$all'].append(i)
    if 'age[]' in data.keys():
        querySentence['age'] = {'$in': []}
        for i in data['age[]']:
            querySentence['age']['$in'].append(int(i))
    if 'rel_date[]' in data.keys():
        if len(data['rel_date[]']) == 1:
            date = datetime.datetime.strptime(data['rel_date[]'][0][0:10], '%Y-%m-%d')
            querySentence['release_date'] = date
        else:
            startDate = datetime.datetime.strptime(data['rel_date[]'][0][0:10], '%Y-%m-%d')
            endDate = datetime.datetime.strptime(data['rel_date[]'][1][0:10], '%Y-%m-%d')
            querySentence['release_date'] = {}
            querySentence['release_date']['$gte'] = startDate
            querySentence['release_date']['$lte'] = endDate
    if 'genre[]' in data.keys():
        querySentence['genre_id'] = {'$all': []}
        for i in data['genre[]']:
            querySentence['genre_id']['$all'].append(i)
    if 'series[id]' in data.keys():
        querySentence['series_id'] = data['series[id]']
    if 'scripter[name]' in data.keys():
        querySentence['scripter'] = {'$in': [data['scripter[name]']]}
    if 'illustrator[name]' in data.keys():
        querySentence['illustrator'] = {'$in': [data['illustrator[name]']]}
    results = list(client['onseidb']['meta'].find(querySentence, responseField))
    return jsonify(results)

@application.route('/list/<key>')
def get_list(key):
    try:
        with open(f'/opt/app/json/{key}.json', 'r') as fp:
            return jsonify(json.load(fp))
    except:
        abort(404)

@application.route('/detail/<id>')
def get_detail(id):
    result = client['onseidb']['meta'].find_one({'id': id}, detailField)
    if not result:
        abort(404)
    return jsonify(result)

@application.route('/database')
def get_database():
    results = list(client['onseidb']['field'].find({}, {'_id': False}))
    update = {}
    for i in results:
        update[i['index']] = i['last_update']
    return jsonify(update)

if __name__ == '__main__':
    application.run()
