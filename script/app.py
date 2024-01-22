# -*- coding: utf-8 -*-

# Main backend application

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

from db_config import mongoUri

application = Flask(__name__)
CORS(application)

client = MongoClient(mongoUri, server_api = ServerApi('1'))

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
    results = list(client['onseidb']['main'].aggregate([
        {"$project": {"_id": 0, "title": 1, "release_date": 1, "price": 1, "circle": 1, "cv": 1, "tag": 1}}
    ]))
    return jsonify(results)

@application.route("/list/cv")
def listCV():
    with open('/opt/app/cv.json', 'r') as fcv:
        results = json.load(fcv)
        return jsonify(results)

@application.route("/list/circle")
def listCircle():
    with open('/opt/app/circle.json', 'r') as fcv:
        results = json.load(fcv)
        return jsonify(results)

@application.route("/list/tag")
def listTag():
    with open('/opt/app/tag.json', 'r') as fcv:
        results = json.load(fcv)
        return jsonify(results)

@application.route("/update")
def update():
    with open('/opt/app/update_record.json', 'r') as frecord:
        results = json.load(frecord)
        return jsonify(results)

if __name__ == '__main__':
    application.run()
