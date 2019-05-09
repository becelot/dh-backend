from flask_restful import Api

from dh_backend.api.deck import load_deck_api
from .user import load_user_api


def load_api(app, prefix='/api'):
    api = Api(app)
    load_user_api(api, f"{prefix}/user")
    load_deck_api(api, f"{prefix}/deck")