from typing import Optional

from flask import Flask


class Twitch(object):
    def __init__(self, client_id: str = None, requires_auth: bool = False):
        self.initialized: bool = False
        self.client_id: str = client_id
        self.client_secret: Optional[str] = None
        self.requires_auth: bool = requires_auth

    def init_app(self, app: Flask):

        # if client_id is not set, try to get from flask config
        if not self.client_id:
            self.client_id = app.config.get('TWITCH_CLIENT_ID')

        # get client_secret
        self.client_secret = app.config.get('TWITCH_CLIENT_SECRET')

        # if client secret was not provided, but the application requires authorization, fail
        if not self.client_secret and self.requires_auth:
            raise Exception("Client secret was not set in configuration")
