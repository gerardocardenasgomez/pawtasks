from db import *
import random
import uuid
from passlib.hash import pbkdf2_sha256

users = ["gerardo", "muffin", "jon", "jane"]
words = ["assessment", "departure", "half", "discourage", "security", "sock", "government", "case", "sink", "objective", "violation", "monkey", "thaw", "exaggerate", "insist", "weak", "fairy", "kit", "continuation", "baseball", "chaos", "index", "constraint", "throne", "groan", "evening", "preference", "pressure", "forge", "note", "depressed", "waste", "shed", "peasant", "isolation", "cassette", "computer", "virus", "invisible", "brink", "bathtub"]
actions = ["roll", "relax", "dictate", "sense", "nod", "sign", "owe", "formulate", "fit", "impress"]

db.connect()
db.drop_tables([Paw, Person, Task, Reward, Role, UserRoles])
db.create_tables([Paw, Person, Task, Reward, Role, UserRoles])


for user in users:
    password_string = random.choice(words)
    password = pbkdf2_sha256.hash(password_string)

    my_user = Person(name=user, username=user, password=password, email=user, age="30", pet_type="cat", user_type="daddy", birthdate="06-17-1988")
    my_user.save()

    title = random.choice(actions) + " " + random.choice(words)
    Task.create(title=title, due_date="11-20-2018", created_by=user, points=1, difficulty=1, username=my_user)

results = Person.select().where(Person.username == "gerardo").get()
print results.username + " " + results.user_type
task_results = Task.select().join(Person).where(Person.username == "gerardo")
for task in task_results:
    print task.title
