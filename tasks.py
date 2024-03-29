from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource, request
from flask_security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required, auth_token_required, current_user
import app
import datetime
from db import *

user_datastore = PeeweeUserDatastore(db, Person, Role, UserRoles)

class Tasks(Resource):
    @auth_token_required
    def get(self):
        task_titles = []
        for task in current_user.tasks:
            task_titles.append(task.title)
        return jsonify({'message': {'tasks': task_titles}})

    @auth_token_required
    def post(self):
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument('title', type=str, location='json', required=True)
        parser.add_argument('due_date', type=str, location='json', required=True)
        parser.add_argument('points', type=str, location='json', required=True)
        parser.add_argument('difficulty', type=str, location='json', required=True)
        args = parser.parse_args()

        title = args['title']
        due_date = args['due_date']
        points = args['points']
        difficulty = args['difficulty']

        created_date = datetime.datetime.now().strftime("%Y-%m-%d")

        # check if the date is valid
        try:
            year, month, day = map(int, due_date.split("-"))
            datetime.date(year, month, day)
            if due_date < created_date:
                raise ValueError('The due date cannot be before the current date!')
        except ValueError as e:
            response = jsonify({'message': {'due_date': e}})
            response.status_code = 400
            return response
        except Exception:
            response = jsonify({'message': {'due_date':'The date format needs to be YYYY-MM-DD'}})
            response.status_code = 400
            return response

        user_task = Task.create(title=title,
                                due_date=due_date,
                                created_date=created_date,
                                created_by=current_user.username,
                                points=points,
                                difficulty=difficulty,
                                username=current_user.id)

        user_task.save()

        return jsonify({"message": {"created": title}})
