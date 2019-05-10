from flask_restful import Api

from dh_backend.api.auth.LoginUser import LoginUser


def load_auth_api(api: Api, prefix):
    api.add_resource(LoginUser, f"{prefix}/login")
