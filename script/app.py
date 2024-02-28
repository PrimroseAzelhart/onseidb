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

noAuthPath = ['/login', '/', '/register']

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
        errCode = 1
    else:
        result = client['onseidb']['user'].find_one({"username": user})
        if result == None:
            errCode = 2
        else:
            hashed = result['password'].encode(encoding='utf-8')
            if not bcrypt.checkpw(pwd, hashed):
                errCode = 3
            else:
                errCode = 0
                token = secrets.token_hex(32)
                expiration = datetime.datetime.now() + datetime.timedelta(days=1)
                result['token'][token] = expiration
                client['onseidb']['user'].replace_one({'username': user}, result)

    if errCode != 0:
        response = {'err_code': errCode}
    else:
        response = {'err_code': errCode, 'user': user, 'token': token}

    return jsonify(response)

@application.route('/register', methods=['POST'])
def register():
    user = request.values.get('username')
    pwd = request.values.get('password').encode(encoding='utf-8')
    code = request.values.get('invitation_code')
    if len(code) != 32:
        abort(403)
    result = client['onseidb']['invitation_code'].find_one_and_delete({'code': code})
    if not result:
        errCode = 1
    else:
        userExist = client['onseidb']['user'].find_one({'username': user})
        if userExist:
            errCode = 2
        else:
            salt = bcrypt.gensalt()
            encryptedPwd = bcrypt.hashpw(pwd, salt).decode(encoding='utf-8')
            userInfo = {'username': user, 'password': encryptedPwd, 'token': {}, 'register_time': datetime.datetime.now()}
            client['onseidb']['user'].insert_one(userInfo)
            errCode = 0
    return jsonify({'err_code': errCode})

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

@application.route('/list/<key>', methods=['POST'])
def get_list(key):
    try:
        with open(f'/opt/app/json/{key}.json', 'r') as fp:
            return jsonify(json.load(fp))
    except:
        abort(404)

@application.route('/detail/<id>', methods=['POST'])
def get_detail(id):
    result = client['onseidb']['meta'].find_one({'id': id}, detailField)
    if not result:
        abort(404)
    return jsonify(result)

@application.route('/database', methods=['POST'])
def get_database():
    results = list(client['onseidb']['field'].find({}, {'_id': False}))
    update = {}
    for i in results:
        update[i['index']] = i['last_update']
    return jsonify(update)

@application.before_request
def before():
    url = request.path
    if url in noAuthPath:
        pass
    else:
        token = request.values.get('token')
        if not token:
            abort(403)
        result = client['onseidb']['user'].find_one({f'token.{token}': {'$exists': True}})
        if not result:
            abort(403)
        else:
            pass

if __name__ == '__main__':
    application.run()
