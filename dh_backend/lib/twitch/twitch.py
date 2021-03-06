from flask import Flask

from dh_backend.lib.twitch.api import TwitchAPI
from dh_backend.lib.twitch.auth import TwitchOAuth
from dh_backend.lib.twitch.models.user import TwitchUser
from dh_backend.lib.twitch.users import TwitchUsers
from dh_backend.models import User


class Twitch(object):
    def __init__(self, client_id: str = None, requires_auth: bool = False):
        self.api: TwitchAPI = TwitchAPI(client_id, requires_auth)

    def init_app(self, app: Flask):
        self.api.init_app(app)

    def auth_flow(self) -> TwitchOAuth:
        if not self.api.requires_auth:  # pragma: no cover
            raise Exception("Application is not configured for authentication")

        return TwitchOAuth(self.api)

    def user(self, user: User) -> TwitchUser:
        return TwitchUsers(self.api, user)[0]
