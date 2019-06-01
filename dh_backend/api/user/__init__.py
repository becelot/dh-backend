from flask_restful import Api

from dh_backend.api.user.ExtensionConfigured import ExtensionConfigured
from dh_backend.api.user.Recent import Recent
from dh_backend.api.user.RegisterUser import RegisterUser


def load_user_api(api: Api, prefix):
    api.add_resource(RegisterUser, f"{prefix}/register")
    api.add_resource(ExtensionConfigured, f"{prefix}/<string:channel_id>/configured")
    api.add_resource(Recent, f"{prefix}/<string:channel_id>/recent")
