import json

from faker import Faker
from flask.testing import FlaskClient

from dh_backend.models import User


def register_user(db_session,
                  client: FlaskClient,
                  username="TestUser",
                  password="Test",
                  email="test@nomail.de"):
    client.post('/api/user/register',
                data=json.dumps({
                    'username': username,
                    'password': password,
                    'email': email
                }),
                content_type='application/json')

    return db_session.query(User).filter_by(user_name=username).first()


def start_twitch_session(client: FlaskClient, user: User):
    client.post('/api/auth/twitch_session',
                data=json.dumps({
                    'username': user.user_name,
                    'token': user.api_key
                }),
                content_type='application/json')

    return user.twitch_session


def test_user():
    user = User(user_name="TestUser", password="Test", email="test@nomail.de")
    return user


def test_users(n: int = 50):
    fake = Faker(locale="de-DE")
    Faker.seed(1234)

    users = []
    for i in range(n):
        profile = fake.profile()
        u = User(user_name=profile["username"], email=profile["mail"], password=fake.password())
        users.append(u)

    return users
