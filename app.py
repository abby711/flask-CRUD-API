from flask import Flask,jsonify,request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)
app.secret_key="secretkey"
app.config['MONGO_URI'] = 'mongodb+srv://abby:<!!!!!!!>@freecluster.lvlvs.mongodb.net/crudapi?retryWrites=true&w=majority'
mongo = PyMongo(app)



@app.route('/create',methods=['POST'])
def add():
    _json=request.json
    _name=_json['name']
    _email=_json['email']
    _password=_json['password']

    if _name and _email and _password and request.method == 'POST':
        _hashpassword=generate_password_hash(_password)
        id=mongo.db.crud.insert({'name':_name,'email':_email,'password':_hashpassword})
        resp=jsonify("user added successfully")
        resp.status_code=200
        return resp
    else:
        return notfound()

@app.route('/read')
def display():
    users=mongo.db.crud.find()
    resp=dumps(users)
    return resp

@app.route('/read/<id>')
def display2(id):
    users=mongo.db.crud.find_one({'_id':ObjectId(id)})
    resp=dumps(users)
    return resp

@app.route('/delete/<id>',methods=['DELETE'])
def deleteyser(id):
    users=mongo.db.crud.delete_one({'_id':ObjectId(id)})
    resp=jsonify("user deleted successfully")
    resp.status_code=200
    return resp

@app.route('/update/<id>',methods=['PUT'])
def update(id):
    _id=id
    _json=request.json
    _name=_json['name']
    _email=_json['email']
    _password=_json['password']
    if _name and _email and _password and _id and request.method == 'PUT':
        _hashpassword=generate_password_hash(_password)
        filter={'_id':ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}
        newvalues = { "$set": { 'name': _name, 'email': _email, 'password': _hashpassword } }
        mongo.db.crud.update_one(filter,newvalues)
        resp=jsonify("user updated successfully")
        resp.status_code=200
        return resp
    else:
        return notfound()



@app.errorhandler(404)
def notfound(error=None):
    message={
    'status':404,
    'message':'not found'
    }
    resp=jsonify(message)
    resp.status_code=404
    return resp










