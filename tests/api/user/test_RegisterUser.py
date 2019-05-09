import json

from flask.testing import FlaskClient


def test_register_user(client: FlaskClient):
    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 201


def test_register_already_registered(client: FlaskClient):
    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 201

    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 422


def test_username_invalid(client: FlaskClient):
    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test_321',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 400
