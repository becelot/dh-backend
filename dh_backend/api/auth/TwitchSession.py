import re
import secrets

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from dh_backend.lib.twitch import twitch
from dh_backend.models import User


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

        return {
            'status': 200,
            'message': 'Authentication session created',
            'auth_url': twitch.auth_flow().create_oauth_session(user)
        }
