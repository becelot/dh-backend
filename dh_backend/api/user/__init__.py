from flask_restful import Api

from dh_backend.api.user.RegisterUser import RegisterUser


def load_user_api(api: Api, prefix):
    api.add_resource(RegisterUser, f"{prefix}/register")
