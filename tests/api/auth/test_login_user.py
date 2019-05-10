import json

from flask.testing import FlaskClient

from dh_backend.models import User


def test_login(db_session, client: FlaskClient):
    user = User(user_name='tester', password='1234', email='NoMAid')
    db_session.add(user)
    db_session.commit()

    response = client.post('/api/auth/login',
                           data=json.dumps({'username': 'tester', 'password': '1234'}),
                           content_type='application/json')

    assert response.json['status'] == 200