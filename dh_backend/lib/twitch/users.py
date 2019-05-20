from typing import List

from dh_backend.lib.twitch.api import TwitchAPI
from dh_backend.lib.twitch.models.user import TwitchUser
from dh_backend.models import User


class TwitchUsers(object):
    def __init__(self, api: TwitchAPI, user: User):
        self.api: TwitchAPI = api
        self._data: List[TwitchUser] = []

        if user and user.twitch_session and user.twitch_session.access_token:
            users = self.api.get('users',
                                 headers={'Authorization': f'Bearer {user.twitch_session.access_token}'}
                                 )['data']

            for user in users:
                self._data.append(TwitchUser(user))

    def __getitem__(self, item: int) -> TwitchUser:
        return self._data[item]
