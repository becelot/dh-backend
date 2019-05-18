import re
import secrets

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from dh_backend.models import User, db


class TwitchSession(Resource):
    """
    Generate a temporary session that is used to link the account to a Twitch account.
    """

    parser = RequestParser() \
        .add_argument('username', type=str, location='json', required=True, help="Username is required")\
        .add_argument('token', type=str, location='json', required=True, help="Token is required")
    """
    Expected input format:
        - username: str -> The username of the user that wants to link to Twitch
        - token: str -> The login token of the user
    """

    def post(self):
        args = TwitchSession.parser.parse_args()

        # username sanity checks
        username: str = args['username']

        pattern = re.compile("^[a-zA-Z0-9]{4,24}$")
        if not pattern.match(username):
            return {"status": 400, "message": "The username has an invalid format."}

        # check if authorization succeeds in constant time
        authenticated: bool = False
        user = User.query.filter_by(user_name=username).first()
        if user:
            token = args['token']

            if secrets.compare_digest(token, user.api_key):
                authenticated = True

        # return error if not successfully authenticated
        if not authenticated:
            return {'status': 422, 'message': 'Authentication failed.'}

        # create a temporary session token and
        session_token: str = secrets.token_urlsafe(30)
        user.twitch_auth_session = session_token
        db.session.commit()

        return {
            'status': 200,
            'message': 'Authentication session created',
            'auth_url': "https://id.twitch.tv/oauth2/authorize"
                        "?client_id=3jqh17gag0ubkiz9h24z7gp5x3fd8e"
                        "&redirect_uri=http://localhost:5000/api/auth/twitch_redirect"
                        "&response_type=code"
                        "&scope=user:read:email"
                        "&force_verify=true"
                        f"&state={session_token}"
        }
