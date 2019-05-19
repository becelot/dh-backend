from typing import Optional, Dict, Any

import requests
from flask import Flask


class TwitchAPI(object):
    def __init__(self, client_id: str = None, requires_auth: bool = False):
        self.initialized: bool = False
        self.client_id: str = client_id
        self.client_secret: Optional[str] = None
        self.requires_auth: bool = requires_auth
        self.redirect_url: Optional[str] = None
        self.base_url: str = 'https://api.twitch.tv/helix/'
        self.twitch_authorization_endpoint = 'https://id.twitch.tv/oauth2/'

    def _headers(self, custom: Dict[str, str] = None) -> Dict[str, str]:
        default: Dict[str, str] = {
            'Client-ID': self.client_id
        }
        return {**default, **custom} if custom else default.copy()

    def _url(self, path: str = '') -> str:
        return self.base_url.rstrip('/') + '/' + path.lstrip('/')

    def init_app(self, app: Flask):

        # if client_id is not set, try to get from flask config
        if not self.client_id:
            self.client_id = app.config.get('TWITCH_CLIENT_ID')

        # reconfigure the Helix endpoint URL
        if app.config.get('TWITCH_HELIX_ENDPOINT'):
            self.base_url = app.config.get('TWITCH_HELIX_ENDPOINT')

        # get client_secret and redirection URL
        self.client_secret = app.config.get('TWITCH_CLIENT_SECRET')
        self.redirect_url = app.config.get('TWITCH_REDIRECT_URL')

        # if the authorization configuration option is set, use it instead
        if app.config.get('TWITCH_AUTHORIZATION_ENDPOINT'):
            self.twitch_authorization_endpoint = app.config.get('TWITCH_AUTHORIZATION_ENDPOINT')

        # if client secret was not provided, but the application requires authorization, fail
        if not self.client_secret and self.requires_auth:
            raise Exception("TWITCH_CLIENT_SECRET was not set in configuration")

        if not self.redirect_url and self.requires_auth:
            raise Exception("TWITCH_REDIRECT_URL was not set in configuration")

        # if authentication requirements is fulfilled, implicitly set the parameter
        if self.client_secret and self.redirect_url:
            self.requires_auth = True

    def request(self, method, path: str = '', **kwargs) -> dict:
        url: str = self._url(path=path)
        request = requests.Request(method, url, **kwargs).prepare()

        response: requests.Response = requests.Session().send(request)

        # Raise exception if status code is not 200
        response.raise_for_status()

        return response.json()

    def get(self, path: str, params: Dict[str, Any] = None, headers: Dict[str, Any] = None, **kwargs) -> dict:
        return self.request('GET', path, params=params, headers=self._headers(headers), **kwargs)
