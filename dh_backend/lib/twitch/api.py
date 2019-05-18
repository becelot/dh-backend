from typing import Optional

from flask import Flask


class TwitchAPI(object):
    def __init__(self, client_id: str = None, requires_auth: bool = False):
        self.initialized: bool = False
        self.client_id: str = client_id
        self.client_secret: Optional[str] = None
        self.requires_auth: bool = requires_auth
        self.redirect_url: Optional[str] = None

    def init_app(self, app: Flask):

        # if client_id is not set, try to get from flask config
        if not self.client_id:
            self.client_id = app.config.get('TWITCH_CLIENT_ID')

        # get client_secret and redirection URL
        self.client_secret = app.config.get('TWITCH_CLIENT_SECRET')
        self.redirect_url = app.config.get('TWITCH_REDIRECT_URL')

        # if client secret was not provided, but the application requires authorization, fail
        if not self.client_secret and self.requires_auth:
            raise Exception("TWITCH_CLIENT_SECRET was not set in configuration")

        if not self.redirect_url and self.requires_auth:
            raise Exception("TWITCH_REDIRECT_URL was not set in configuration")

        # if authentication requirements is fulfilled, implicitly set the parameter
        if self.client_secret and self.redirect_url:
            self.requires_auth = True
