from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
from db import *
from user import *
from peewee import *
from flask_security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required, auth_token_required, current_user
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ['PAWTASKS_SECRET_KEY']
api = Api(application)

db.connect()

user_datastore = PeeweeUserDatastore(db, Person, Role, UserRoles)
security = Security(application, user_datastore)

class Login(Resource):
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('username', type=str, location='json', required=False)
        parser.add_argument('password', type=str, location='json', required=False)
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

api.add_resource(User, '/api/user')
api.add_resource(Login, '/api/login')
