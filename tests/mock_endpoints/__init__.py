from flask_restful import Api

from tests.mock_endpoints.TwitchOAuthToken import TwitchOAuthToken


def load_mock_endpoints(api: Api):
    api.add_resource(TwitchOAuthToken, '/api/mock/twitch/token')
