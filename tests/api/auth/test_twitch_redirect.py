import secrets

from flask.testing import FlaskClient

from dh_backend.models import User, TwitchSession
from tests.data.users import register_user, start_twitch_session


def simulate_user_authorization(db_session, client: FlaskClient, session: TwitchSession, cancel: bool = False):
    data: dict = {
        'state': session.twitch_session_token
    }

    if cancel:
        data['error'] = 'access_denied'
        data['error_description'] = 'User canceled authorization.'
        data['state'] = session.twitch_session_token
    else:
        code = secrets.token_urlsafe(30)
        data['scope'] = session.scope
        data['code'] = code
        session.code = code
        db_session.commit()

    client.get('/api/auth/twitch_redirect', query_string=data)


def test_twitch_redirect(db_session, client: FlaskClient):
    user: User = register_user(db_session, client)
    session: TwitchSession = start_twitch_session(client, user)
    simulate_user_authorization(db_session, client, session)
