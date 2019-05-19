from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from dh_backend.lib.twitch import twitch
from dh_backend.models import TwitchAccount, db, TwitchSession


class TwitchRedirect(Resource):
    """
    URL that is called after the user authorized
    """

    parser = RequestParser()\
        .add_argument('code', type=str, location='args')\
        .add_argument('scope', type=str, location='args')\
        .add_argument('state', type=str, location='args')

    def get(self):
        args = TwitchRedirect.parser.parse_args()

        session = args['state']
        if not session:
            return "Authorization failed. Please try again later."

        twitch_session: TwitchSession = TwitchSession.query.filter_by(twitch_session_token=session).first()
        if not twitch_session:
            return "Authorization failed. Invalid session."

        if not twitch.auth_flow().validate_redirect_authorization():
            return "Authorization failed. Invalid session."

        account: TwitchAccount = TwitchAccount.from_user(twitch_session.user)
        db.session.add(account)
        db.session.commit()

        return account.login
