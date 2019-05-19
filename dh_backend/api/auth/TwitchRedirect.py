from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from dh_backend.lib.twitch import twitch
from dh_backend.lib.twitch.models.user import TwitchUser
from dh_backend.models import User, TwitchAccount, db


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

        user: User = User.query.filter_by(twitch_auth_session=session).first()
        if not user:
            return "Authorization failed. Invalid session."

        if not twitch.auth_flow().validate_redirect_authorization():
            return "Authorization failed. Invalid session."

        account: TwitchAccount = TwitchAccount.from_user(user)
        db.session.add(account)
        db.session.commit()

        return account.login
