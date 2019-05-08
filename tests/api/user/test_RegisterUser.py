import json

from flask.testing import FlaskClient


def test_register_user(client: FlaskClient, db_session):
    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 200


def test_register_already_registered(client: FlaskClient, db_session):
    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 200

    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 500
