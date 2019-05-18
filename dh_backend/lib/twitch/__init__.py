from dh_backend.lib.twitch.twitch import Twitch
from dh_backend.lib.twitch.auth import TwitchOAuth

twitch = Twitch(requires_auth=True)

__all__ = ['twitch', 'Twitch', 'TwitchOAuth']
