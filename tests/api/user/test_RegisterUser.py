import json

from flask.testing import FlaskClient

from dh_backend.models import RecentDeck


def test_register_user(client: FlaskClient, db_session):
    register = client.post('/api/user/register',
                           data=json.dumps({
                               'username': 'test',
                               'password': 'test',
                               'email': 'test'
                           }),
                           content_type='application/json')

    assert register.json["status"] == 201

    assert len(db_session.query(RecentDeck).all()) == 1


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
