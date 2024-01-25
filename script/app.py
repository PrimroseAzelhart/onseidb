# -*- coding: utf-8 -*-

# Main backend application

import json
import bcrypt
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from func.db_config import db_client

application = Flask(__name__)
CORS(application)

client = db_client()

@application.route("/")
def index():
    return "<p>Hello world!</p>"

@application.route("/login", methods=['POST'])
def login():
    user = request.values.get('username')
    pwd = request.values.get('password').encode(encoding='utf-8')
    id = ""
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

    response = {"code": code, "id": id}
    return jsonify(response)

@application.route("/search", methods=['POST'])
def search():
    results = list(client['onseidb']['meta'].find({}, {'_id': False}))
    return jsonify(results)

@application.route("/list/<key>")
def get_list(key):
    try:
        with open(f'/opt/app/json/{key}.json', 'r') as fp:
            return jsonify(json.load(fp))
    except:
        abort(404)

if __name__ == '__main__':
    application.run()
