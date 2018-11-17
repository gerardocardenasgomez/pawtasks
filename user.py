from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource, request
from flask_security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required, auth_token_required, current_user
import app
from db import *

parser = reqparse.RequestParser(bundle_errors=True)
user_datastore = PeeweeUserDatastore(db, Person, Role, UserRoles)

class User(Resource):
    @auth_token_required
    def get(self):
        return jsonify({"message": {"username": current_user.username}})
    def post(self):
        #print request.url_rule
        parser.add_argument('username', type=str, location='json', required=True)
        parser.add_argument('password', type=str, location='json', required=True)
        parser.add_argument('email', type=str, location='json', required=True)
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        email = args['email']

        if password == '' or password == None:
            response = jsonify({"message": {"password":"Password can't be empty."}})
            response.status_code = 400
            return response

        if username == '' or username == None:
            response = jsonify({"message": {"username":"Username can't be empty."}})
            response.status_code = 400
            return response

        try:
            if username and password and email:
                user_datastore.create_user(email=email, password=password, username=username)
                return {'created': username}
        except Exception as e:
            db.rollback()
            response = jsonify({"message": {"error":"Username already exists."}})
            response.status_code = 400
            return response
