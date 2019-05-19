from flask_restful import Resource


class TwitchOAuthToken(Resource):
    def get(self):
        return "Valid"
