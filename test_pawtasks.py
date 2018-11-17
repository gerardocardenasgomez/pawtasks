import pytest
import os
import random
import string
import json
from app import *
from db import *

db_username = "UNIT_TEST_USER"
db_user_pass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))

try:
    query = Person.delete().where(Person.username == db_username)
    query.execute()
except Exception as e:
    print e
    pass

@pytest.fixture
def client():
    client = application.test_client()
    yield client

def test_user_no_auth(client):
    """Start with an unauthenticated request for /api/user"""

    req = client.get("/api/user")
    assert b"Unauthorized" in req.data

def test_user_creation(client):
    """Create a user first"""

    data = {"username":db_username, "password":db_user_pass, "email":"testing@localhost"}

    req = client.post("/api/user", data=json.dumps(data), content_type="application/json")
    assert b"created" in req.data

    """I shouldn't be allowed to create a duplicate user"""
    req = client.post("/api/user", data=json.dumps(data), content_type="application/json")
    assert b"Username already exists" in req.data

    """Username and password are required"""
    data = {"username":"", "password":db_user_pass, "email":"testing@localhost"}

    req = client.post("/api/user", data=json.dumps(data), content_type="application/json")
    assert b"Username can\'t be empty" in req.data


    data = {"username":db_username, "password":"", "email":"testing@localhost"}

    req = client.post("/api/user", data=json.dumps(data), content_type="application/json")
    assert b"Password can\'t be empty" in req.data

def test_user_login(client):
    """Get the token first"""

    data = {"username":db_username, "password":db_user_pass}

    request = client.post("/api/login", data=json.dumps(data), content_type="application/json")
    assert b"token" in request.data
    json_data = json.loads(request.data)

    """Try to use the token"""

    headers = {"Authentication-Token":json_data['token']}
    req = client.get("/api/user", headers=headers)
    assert db_username in req.data
