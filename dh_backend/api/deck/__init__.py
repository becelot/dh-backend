from flask_restful import Api

from .UploadDeck import UploadDeck


def load_deck_api(api: Api, prefix):
    api.add_resource(UploadDeck, f"{prefix}/upload")
