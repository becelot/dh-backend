import secrets

import pytest
from flask import Response
from flask.testing import FlaskClient

from dh_backend.lib.twitch import twitch
from dh_backend.lib.twitch.models import TwitchUser
from dh_backend.models import User, TwitchSession
from tests.data.users import register_user, start_twitch_session
from tests.mock_endpoints.TwitchHelix import mock_twitch_helix_users
from tests.mock_endpoints.TwitchOAuthToken import mock_twitch_oauth_token


@pytest.fixture
def twitch_db():
    yield {
        'users': {
            'TwitchUser': TwitchUser(data={
                'id': '12405834',
                'login': 'twitchuser',
                'display_name': 'TwitchUser',
                'type': '',
                'broadcaster_type': '',
                'view_count': 234,
                'description': '',
                'email': 'twitch_user@testmail.com'
            })
        },
        'pending_sessions': {},
        'sessions': []
    }


def simulate_user_authorization(client: FlaskClient, session: TwitchSession, twitch_db, cancel: bool = False):
    data: dict = {
        'state': session.twitch_session_token
    }

    if cancel:
        data['error'] = 'access_denied'
        data['error_description'] = 'User canceled authorization'
    else:
        # Generate a code for this session
        code = secrets.token_urlsafe(30)

        twitch_session = {
            'user': 'TwitchUser',
            'expected_client_secret': twitch.api.client_secret,
            'expected_client_id': twitch.api.client_id,
            'allowed_scopes': ['user:email:read'],
            'grant_type': 'authorization_code',
            'redirect_uri': twitch.api.redirect_url
        }

        twitch_db['pending_sessions'][code] = twitch_session

        data['scope'] = session.scope
        data['code'] = code

    return client.get('/api/auth/twitch_redirect', query_string=data)


def test_twitch_redirect(db_session, client: FlaskClient, responses, twitch_db):
    mock_twitch_oauth_token(responses, twitch_db)
    mock_twitch_helix_users(responses, twitch_db)
    user: User = register_user(db_session, client)
    session: TwitchSession = start_twitch_session(client, user)
    response: Response = simulate_user_authorization(client, session, twitch_db)

    assert response.data.startswith(b'Authroization success. Linked account to TwitchUser')


def test_twitch_redirect_no_state(client: FlaskClient):
    response: Response = client.get('/api/auth/twitch_redirect', query_string={})

    assert response.data.startswith(b'Authroization failed. Reason: CSRF token was not provided')


def test_twitch_redirect_invalid_state(client: FlaskClient):
    response: Response = client.get('/api/auth/twitch_redirect', query_string={'state': 'rsgeergaaerh'})

    assert response.data.startswith(b'Authroization failed. Reason: Invalid session')


def test_twitch_redirect_user_cancelled(db_session, client: FlaskClient):
    user: User = register_user(db_session, client)
    session: TwitchSession = start_twitch_session(client, user)
    response: Response = simulate_user_authorization(client, session, twitch_db, True)

    assert response.data.startswith(b'Authroization failed. Reason: User canceled authorization - Access denied')


def test_twitch_redirect_twitch_invalid_response(db_session, client: FlaskClient):
    user: User = register_user(db_session, client)
    session: TwitchSession = start_twitch_session(client, user)
    response = client.get('/api/auth/twitch_redirect', query_string={
        'state': session.twitch_session_token
    })
    assert response.data.startswith(b'Authroization failed. Reason: TwitchAPI did not respond. Please try again later')
