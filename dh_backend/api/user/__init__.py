from flask_restful import Api

from dh_backend.api.user.ExtensionConfigured import ExtensionConfigured
from dh_backend.api.user.RegisterUser import RegisterUser


def load_user_api(api: Api, prefix):
    api.add_resource(RegisterUser, f"{prefix}/register")
    api.add_resource(ExtensionConfigured, f"{prefix}/configured/<string:channel_id>")
