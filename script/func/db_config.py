#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

username = ''
password = ''
host = 'localhost'
port = 0
auth = 'admin'
authMech = 'SCRAM-SHA-1'

mongoUri = f"mongodb://{username}:{password}@{host}:{port}/?authSource={auth}&authMechanism={authMech}"

# Connect and return a db client instance
def db_client():
    return MongoClient(mongoUri, server_api = ServerApi('1'))
