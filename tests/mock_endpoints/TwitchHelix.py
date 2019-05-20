import json

from requests import PreparedRequest

from dh_backend.lib.twitch import twitch


def mock_twitch_helix_users(responses, twitch_db):
    """Mocks the https://api.twitch.tv/helix/users endpoint"""

    def twitch_helix_users(request: PreparedRequest):
        client_id: str = request.headers['Client-ID']
        authorization: str = request.headers['Authorization'][7:]

        if client_id != twitch.api.client_id:
            print("Client ID mismatch")
            return 200, {'Content-Type': 'application/json'}, json.dumps({})

        user_session = next(filter(lambda x: x['access_token'] == authorization, twitch_db['sessions']), None)
        if not user_session:
            print(f"Username for {authorization} not found")
            return 200, {'Content-Type': 'application/json'}, json.dumps({})

        user = twitch_db['users'][user_session['user']]
        if not user:
            print(f"User for {user_session['user']} not found")
            return 200, {'Content-Type': 'application/json'}, json.dumps({})

        return 200, {'Content-Type': 'application/json'}, json.dumps({
            'data': [
                user.data
            ]
        })

    responses.add_callback(
        responses.GET,
        'https://api.twitch.tv/helix/users',
        callback=twitch_helix_users,
        content_type='application/json'
    )
