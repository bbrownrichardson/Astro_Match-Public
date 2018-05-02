import pytest
import os
from db_module import DBHandler
import requests


# When using pytest, any function that starts with the string test will
# automatically be run.
def test_db_mod():
    # Create an instance of the class
    DB = DBHandler()

    # Initiate the database
    DB.init_db()

    # Add some users
    DB.post('male', 'Taurus', 'Test User', 21, 'female', 'Test1')
    DB.post('female', 'Aries', 'Test User2', 19, 'male', 'Test2')

    users = DB.get_all_users()
    assert users == [{'sign': 'Taurus', 'id': 1, 'gender': 'male',
                      'preference': 'female', 'bio': 'Test1', 'age': 21,
                      'name': 'Test User'}, {'sign': 'Aries', 'id': 2,
                                             'gender': 'female',
                                             'preference': 'male', 'bio':
                                                 'Test2', 'age': 19,
                                             'name': 'Test User2'}]

    # Get one user
    one_user = DB.get_by_id(1)

    assert one_user == {'sign': 'Taurus', 'id': 1, 'gender': 'male',
                        'preference': 'female', 'bio': 'Test1', 'age': 21,
                        'name': 'Test User'}


def test_api_one_user():
    # Get One User
    r = requests.get('http://127.0.0.1:5000/api/users/1')
    print(r.text)
    expected = {
        "age": 21,
        "bio": "Test1",
        "gender": "male",
        "id": 1,
        "name": "Test User",
        "preference": "female",
        "sign": "Taurus"
    }

    assert r.json() == expected


def test_api_all_users():
    # Get All Users
    r = requests.get('http://127.0.0.1:5000/api/users/')
    expected = [{"age": 21, "bio": "Test1", "gender":
                 "male", "id": 1, "name": "Test User", "preference": "female",
                 "sign": "Taurus"}, {"age": 19, "bio": "Test2",
                                     "gender": "female", "id": 2,
                                     "name": "Test User2",
                                     "preference": "male", "sign": "Aries"}]

    assert r.json() == expected


def test_post():
    # Test post
    r = requests.post('http://127.0.0.1:5000/api/register/', data={
        "age": 18,
        "bio": "Test3",
        "gender": "male",
        "name": "Test User",
        "preference": "female",
        "sign": "Taurus"
    })

    r2 = requests.get('http://127.0.0.1:5000/api/users/3')
    expected = {
        "age": 18,
        "bio": "Test3",
        "gender": "male",
        "id": 3,
        "name": "Test User",
        "preference": "female",
        "sign": "Taurus"
    }

    assert r2.json() == expected


def test_request_error():
    # Tests for if not all the information is provided
    r = requests.post('http://127.0.0.1:5000/api/register/', data={
        "age": 18,
        "bio": "Test3",
        "name": "Test User",
        "preference": "female",
        "sign": "Taurus"
    })

    assert r.json() == {"error": "gender required"}
    
