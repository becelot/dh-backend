from flask_restful import Api

from dh_backend.api.auth.TwitchRedirect import TwitchRedirect
from dh_backend.api.auth.TwitchSession import TwitchSession
from dh_backend.api.auth.LoginUser import LoginUser


def load_auth_api(api: Api, prefix):
    api.add_resource(LoginUser, f"{prefix}/login")
    api.add_resource(TwitchSession, f"{prefix}/twitch_session")
    api.add_resource(TwitchRedirect, f"{prefix}/twitch_redirect")
