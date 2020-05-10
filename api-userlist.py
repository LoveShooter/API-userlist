import pymongo
import requests
import json, bson
import random
import datetime
import os
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS


class JSONEncoder(json.JSONEncoder):                           
    ''' extend json-encoder class'''    
    def default(self, o):                               
        if isinstance(o, ObjectId):
            return str(o)                               
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


app = Flask(__name__)
CORS(app)   # This will enable CORS for all routes


app.config['MONGO_DBNAME'] = 'userslist' # Name of database on mongo
app.config["MONGO_URI"] = "mongodb+srv://sysadm:Ff121314@cluster0-gpxwq.mongodb.net/userslist" #URI to Atlas cluster  + Auth Credentials


mongo = PyMongo(app)
app.json_encoder = JSONEncoder # Use the modified encoder class to handle ObjectId & datetime object while jsonifying the response.


@app.route('/', methods=['GET']) # Hello message
def index():
    
    return 'Hello! It works!'



@app.route('/get-data', methods=['GET'])  # Find all data in my collection
def getAllData():
    user = mongo.db.users # Connect to my collection

    output = []

    for el in user.find():   # el - like query. each element in list
        output.append({'_id': el['_id'], 'login': el['login'], 'password': el['password'], 'firstName': el['firstName'], 'secondName': el['secondName'], 'email': el['email']})

    return jsonify({'result': output})



@app.route('/add-data', methods=['POST']) # Add data in db. Need input JSON-like data.
def addData():
    user = mongo.db.users
    
    _login = request.json['login']
    _password = request.json['password']
    _firstName = request.json['firstName']
    _secondName = request.json['secondName']
    _email = request.json['email']


    userId = user.insert({'login': _login, 'password': _password, 'firstName': _firstName, 'secondName': _secondName, 'email': _email})
    newUser = user.find_one({'_id': userId})

    output = {'login': newUser['login'], 'password': newUser['password'], 'firstName': newUser['firstName'], 'secondName': newUser['secondName'], 'email': newUser['email']}

    return jsonify({'result': output})



@app.route('/del-data/<id>', methods=['DELETE'])
def delData(id):
    outputId = []
    for element in mongo.db.users.find():
        outputId.append(str(element['_id']))
    
    if id in outputId:
        mongo.db.users.delete_one({'_id': ObjectId(id)})
        response = {"message": "Record deleted"}
    else:
        response = {"message": "Record Not Found!"}
    
    return jsonify(response), 200


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp



if __name__ == '__main__':
    app.run(debug=True)