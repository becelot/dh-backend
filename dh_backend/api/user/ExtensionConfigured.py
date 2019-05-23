from flask_restful import Resource

from dh_backend.models import TwitchAccount


class ExtensionConfigured(Resource):

    def get(self, channel_id: str):
        if not channel_id:
            return {'status': 402, 'message': 'No channel id was provided'}

        account: TwitchAccount = TwitchAccount.query.filter_by(channel_id=channel_id).first()

        if not account:
            return {'status': 402, 'message': 'Channel is not currently linked'}

        return {'status': 200, 'message': 'Channel has been linked to the extension'}
