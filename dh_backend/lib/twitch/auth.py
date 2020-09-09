import secrets
from datetime import datetime, timedelta

import requests
from flask import request

from dh_backend.lib.twitch.api import TwitchAPI
from dh_backend.models import User, db, TwitchSession


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
        while TwitchSession.query.filter_by(twitch_session_token=session_token).first() is not None:
            session_token = secrets.token_urlsafe(30)  # pragma: no cover

        twitch_session: TwitchSession = TwitchSession(user=user, twitch_session_token=session_token)
        db.session.add(twitch_session)
        db.session.commit()

        return f"{self.api.twitch_authorization_endpoint}authorize" \
               f"?client_id={self.api.client_id}" \
               f"&redirect_uri={self.api.redirect_url}" \
               "&response_type=code" \
               "&scope=user:read:email" \
               "&force_verify=true" \
               f"&state={session_token}"

    def validate_redirect_authorization(self) -> (bool, str):
        """
        Validates the authorization redirection
        :return: True iff the authorization succeeded
        """
        # first, check the state
        session = request.args.get('state')
        if not session:
            return False, "CSRF token was not provided."

        twitch_session: TwitchSession = TwitchSession.query.filter_by(twitch_session_token=session).first()
        if not twitch_session:
            return False, "Invalid session."

        # check if the error flag is set
        error = request.args.get('error')
        if error:
            message = request.args.get('error_description') if request.args.get('error_description')\
                else 'Unspecified error.'
            return False, f"{message} - Access denied"

        code = request.args.get('code')
        if not code:
            return False, "TwitchAPI did not respond. Please try again later"

        # Get access token using the OAuth code retrieved
        try:
            req: requests.PreparedRequest = \
                requests.Request('POST',
                                 f"{self.api.twitch_authorization_endpoint}token"
                                 f"?client_id={self.api.client_id}"
                                 f"&client_secret={self.api.client_secret}"
                                 f"&code={code}"
                                 "&grant_type=authorization_code"
                                 f"&redirect_uri={self.api.redirect_url}")\
                .prepare()

            response: requests.Response = requests.Session().send(req)

            if response.status_code != 200:  # pragma: no cover
                raise Exception("Could not acquire access token from Twitch")
        except Exception as e:  # pragma: no cover
            return False, str(e)

        # update the twitch session with the retrieved data
        twitch_session.access_token = response.json()['access_token']
        twitch_session.refresh_token = response.json()['refresh_token']
        twitch_session.expires_at = datetime.now() + timedelta(seconds=response.json()['expires_in'])
        twitch_session.scope = " ".join(response.json()['scope'])
        twitch_session.token_type = response.json()['token_type']
        db.session.commit()

        return True, "Authorization validated"
