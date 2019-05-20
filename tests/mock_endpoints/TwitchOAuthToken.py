import json
import secrets
from urllib.parse import urlparse, parse_qs

from flask_restful import Resource
from requests import PreparedRequest


def mock_twitch_oauth_token(responses, twitch_db):
    """Mock implementation for https://id.twitch.tv/oauth/token"""

    def twitch_oauth_token(request: PreparedRequest):
        params: dict = dict(parse_qs(urlparse(request.url).query))
        client_id: str = params.get('client_id')[0]
        client_secret: str = params.get('client_secret')[0]
        code: str = params.get('code')[0]
        grant_type: str = params.get('grant_type')[0]
        redirect_uri: str = params.get('redirect_uri')[0]

        pending_session = twitch_db['pending_sessions'][code]

        if not pending_session:
            return 200, {'Content-Type': 'application/json'}, json.dumps({'error': 'No session'})

        if client_id != pending_session['expected_client_id'] or \
                client_secret != pending_session['expected_client_secret']:
            return 200, {'Content-Type': 'application/json'}, json.dumps({'error': 'Invalid client credentials'})

        if grant_type != pending_session['grant_type']:
            return 200, {'Content-Type': 'application/json'}, json.dumps({'error': 'grant type not set'})

        if redirect_uri != pending_session['redirect_uri']:
            return 200, {'Content-Type': 'application/json'}, json.dumps({'error': 'Redirect URI does not match'})

        access_token = secrets.token_urlsafe(30)
        refresh_token = secrets.token_urlsafe(30)
        expires_in = 3600
        scope = pending_session['allowed_scopes']
        token_type = 'bearer'

        session = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'scope': scope,
            'token_type': token_type,
            'user': pending_session['user']
        }

        twitch_db['sessions'].append(session)

        return 200, {'Content-Type': 'application/json'}, json.dumps({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'expires_in': expires_in,
            'scope': scope,
            'token_type': token_type
        })

    responses.add_callback(
        responses.POST,
        'https://id.twitch.tv/oauth2/token',
        callback=twitch_oauth_token,
        content_type='application/json'
    )


class TwitchOAuthToken(Resource):
    def get(self):
        return "Valid"
