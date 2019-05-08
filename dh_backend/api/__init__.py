from flask_restful import Api

from .user import load_user_api


def load_api(app, prefix='/api'):
    api = Api(app)
    load_user_api(api, f"{prefix}/user")
