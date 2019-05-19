import json

from flask.testing import FlaskClient

from dh_backend.models import User
from dh_backend.lib.twitch import twitch
from tests.data.users import register_user


def test_twitch_session_success(db_session, client: FlaskClient):
    user: User = register_user(db_session, client)

    session = client.post('/api/auth/twitch_session',
                          data=json.dumps({
                              'username': user.user_name,
                              'token': user.api_key
                          }),
                          content_type='application/json')

    assert session.json['status'] == 200
    assert user.twitch_session
    assert user.twitch_session.twitch_session_token

    expected_url = f"{twitch.api.twitch_authorization_endpoint}authorize" \
        f"?client_id={twitch.api.client_id}" \
        f"&redirect_uri={twitch.api.redirect_url}" \
        "&response_type=code" \
        "&scope=user:read:email" \
        "&force_verify=true" \
        f"&state={user.twitch_session.twitch_session_token}"

    assert session.json['auth_url'] == expected_url


def test_twitch_session_invalid_username(db_session, client: FlaskClient):
    user: User = register_user(db_session, client)

    session = client.post('/api/auth/twitch_session',
                          data=json.dumps({
                              'username': 'SELECT * FROM User',
                              'token': user.api_key
                          }),
                          content_type='application/json')

    assert session.json['status'] == 400
    assert not user.twitch_session


def test_twitch_session_token_mismatch(db_session, client: FlaskClient):
    user: User = register_user(db_session, client)

    session = client.post('/api/auth/twitch_session',
                          data=json.dumps({
                              'username': user.user_name,
                              'token': 'HeReIsSomeRanDoMInC0RrEctTOkEn'
                          }),
                          content_type='application/json')

    assert session.json['status'] == 422
    assert not user.twitch_session
