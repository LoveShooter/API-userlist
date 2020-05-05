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



@app.route('/get_data', methods=['GET'])  # Find all data in my collection
def get_all_data():
    user = mongo.db.users # Connect to my collection

    output = []

    for q in user.find():   # q - like query
        output.append({'login': q['login'], 'password': q['password'], 'firstName': q['firstName'], 'secondName': q['secondName'], 'email': q['email']})

    return jsonify({'result': output})



@app.route('/add_data', methods=['POST']) # Add data in db. Need input JSON-like data.
def add_data():
    user = mongo.db.users
    
    _login = request.json['login']
    _password = request.json['password']
    _firstName = request.json['firstName']
    _secondName = request.json['secondName']
    _email = request.json['email']


    user_id = user.insert({'login': _login, 'password': _password, 'firstName': _firstName, 'secondName': _secondName, 'email': _email})
    new_user = user.find_one({'_id': user_id})

    output = {'login': new_user['login'], 'password': new_user['password'], 'firstName': new_user['firstName'], 'secondName': new_user['secondName'], 'email': new_user['email']}

    return jsonify({'result': output})



@app.route('/del_data/<id>', methods=['DELETE'])
def del_one_data(id):
    db_response = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if db_response.deleted_count == 1:
        response = {'message': 'Record deleted'}
    else:
        response = {'message': 'No record found!'}
    return jsonify(response), 200



#@app.route('/del_data/<id>', methods=['GET'])  # Delete data by user ID
#def del_one_data(id):
#    usercoll = mongo.db.users
#    delete_user = usercoll.delete_one({'_id': ObjectId(id)}) 
#    
#    resp = jsonify('Task deleted successfully!')
#    resp.status_code = 200
#	
#    return resp


#@app.route('/add_data_placeholder', methods=['GET'])  # Send a request to the API and add data in mongodb from jsonplaceholder
#def add_data_placeholder():
#    mycoll = mongo.db.users
#    
#    url1 = 'https://jsonplaceholder.typicode.com/users/6'
#    url2 = 'https://jsonplaceholder.typicode.com/users/5'
#    url3 = 'https://jsonplaceholder.typicode.com/users/8'
#    url4 = 'https://jsonplaceholder.typicode.com/users/10'
#    url5 = 'https://jsonplaceholder.typicode.com/users/4'
#    
#    urls = [url1, url2, url3, url4, url5]
#
#    url = requests.get(random.choice(urls))
#    userlist = json.loads(url.text)
#    mycoll.insert_one(userlist)
#    
#    return userlist


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