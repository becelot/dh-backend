from flask import render_template_string, Response
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
        .add_argument('state', type=str, location='args')\
        .add_argument('error', type=str, location="args")\
        .add_argument('error_description', type=str, location="args")

    def get(self):
        args = TwitchRedirect.parser.parse_args()

        authorized, message = twitch.auth_flow().validate_redirect_authorization()
        if not authorized:
            return Response(render_template_string('Authroization failed. Reason: {{ reason }}', reason=message),
                            mimetype='text/html')

        session = args['state']
        twitch_session: TwitchSession = TwitchSession.query.filter_by(twitch_session_token=session).first()

        account: TwitchAccount = TwitchAccount.from_user(twitch_session.user)
        db.session.add(account)
        db.session.commit()

        return Response(render_template_string(
                'Authroization success. Linked account to {{ username }}',
                username=account.display_name
            ),
            mimetype='text/html'
        )
