from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from db import *
from peewee import *
from flask_security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required, auth_token_required, current_user
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ['PAWTASKS_SECRET_KEY']
api = Api(application)

db.connect()

user_datastore = PeeweeUserDatastore(db, Person, Role, UserRoles)
security = Security(application, user_datastore)

parser = reqparse.RequestParser(bundle_errors=True)

class User(Resource):
    @auth_token_required
    def get(self):
        return jsonify({"message": {"username": current_user.username}})
    def post(self):
        parser.add_argument('username', type=str, location='json', required=True)
        parser.add_argument('password', type=str, location='json', required=True)
        parser.add_argument('email', type=str, location='json', required=True)
        args = parser.parse_args()
        print args
        username = args['username']
        password = args['password']
        email = args['email']

        if password == '':
            response = jsonify({"message": {"password":"Password can't be empty."}})
            response.status_code = 400
            return response

        try:
            if username and password and email:
                user_datastore.create_user(email=email, password=password, username=username)
                return {'created': username}
        except IntegrityError:
            response = jsonify({"message": {"error":"Username already exists."}})
            response.status_code = 400
            return response

class Login(Resource):
    def post(self):
        parser.add_argument('username', type=str, location='json', required=True)
        parser.add_argument('password', type=str, location='json', required=True)
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        if username and password:
            user = Person.select().where(Person.username == username).where(Person.password == password).get()
            if user:
                return jsonify({'token': user.get_auth_token()})
            else:
                response = jsonify({"message": {"error":"Incorrect username or password."}})
                response.status_code = 401
                return response
        else:
            response = jsonify({"message": {"error":"Must provide a username and password"}})
            response.status_code = 422
            return response

api.add_resource(User, '/user')
api.add_resource(Login, '/api/login')
