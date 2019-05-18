import secrets

from flask import request

from dh_backend.lib.twitch.api import TwitchAPI
from dh_backend.models import User, db


class TwitchOAuth(object):
    def __init__(self, api: TwitchAPI):
        self.api: TwitchAPI = api

    def create_oauth_session(self, user: User) -> str:
        """
        Creates a new OAuth link session for the selected user.
        :param user: User that wants to link to twitch
        :return: URL that contains the session information
        """
        # create new session token
        session_token: str = secrets.token_urlsafe(30)
        while User.query.filter_by(twitch_auth_session=session_token).first() is not None:
            session_token = secrets.token_urlsafe(30)  # pragma: no cover
        user.twitch_auth_session = session_token
        db.session.commit()

        return "https://id.twitch.tv/oauth2/authorize" \
               f"?client_id={self.api.client_id}" \
               f"&redirect_uri={self.api.redirect_url}" \
               "&response_type=code" \
               "&scope=user:read:email" \
               "&force_verify=true" \
               f"&state={session_token}"
