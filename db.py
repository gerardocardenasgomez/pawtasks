import os
from peewee import *
import datetime
from flask_security import Security, PeeweeUserDatastore, UserMixin, RoleMixin, login_required

db_env = os.environ['PAWTASKS_DB_ENV']
db_user = os.environ['PAWTASKS_DB_USER']
db_password = os.environ['PAWTASKS_DB_PASSWORD']
db_hostname = os.environ['PAWTASKS_DB_HOSTNAME']
db_port = os.environ['PAWTASKS_DB_PORT']

db = PostgresqlDatabase(db_env, user=db_user, password=db_password,
                           host=db_hostname, port=db_port)

class Paw(Model):
    pet_type = CharField()
    gender = CharField()
    location = CharField()
    color = CharField()

    class Meta:
        database = db

class Person(Model, UserMixin):
    username = CharField(null=False, index=True, unique=True)
    name = CharField(null=True)
    email = CharField(null=False)
    age = IntegerField(null=True)
    pet_type = CharField(null=True)
    user_type = CharField(null=True)
    password = CharField(null=False)
    birthdate = DateField(null=True)
    authenticated = BooleanField(default=False)

    class Meta:
        database = db

class Task(Model):
    title = CharField()
    due_date = DateField()
    created_date = DateField(default=datetime.datetime.now)
    created_by = CharField()
    picture = CharField(null=True)
    points = IntegerField()
    difficulty = CharField()
    notes = TextField(null=True)
    username = ForeignKeyField(Person, backref="tasks")

    class Meta:
        database = db

class Reward(Model):
    id = UUIDField(unique=True)
    name = CharField()
    points = IntegerField()
    earned_count = IntegerField(default=0)
    username = ForeignKeyField(Person, backref="rewards")

    class Meta:
        database = db

class Role(Model, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

    class Meta:
        database = db

class UserRoles(Model):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(Person, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)

    class Meta:
        database = db

if __name__ == "__main__":
    db.connect()
    db.drop_tables([Paw, Person, Task, Reward, Role, UserRoles])
    db.create_tables([Paw, Person, Task, Reward, Role, UserRoles])
