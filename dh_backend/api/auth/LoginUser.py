import re

from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from dh_backend.models import User


class LoginUser(Resource):
    """
    Endpoint handling user login.
    """

    parser = RequestParser()\
        .add_argument('username', type=str, location='json', required=True, help="Username is required")\
        .add_argument('password', type=str, location='json', required=True, help="Password is required")
    """
    Expected input format for this resource is:
        - username: string -> name of the user that requires a login
        - password: string -> password of the user to authenticate him
    """
    def post(self):
        """Login is done using POST method"""
        args = LoginUser.parser.parse_args()

        # username sanity checks
        username: str = args['username']

        pattern = re.compile("^[a-zA-Z0-9]{4,24}$")
        if not pattern.match(username):
            return {"status": 400, "message": "The username has an invalid format."}

        # check if user is registered
        user = User.query.filter_by(user_name=username).first()
        if not user:
            return {"message": "The username or password is not correct.", "status": 422}

        # check password of user
        password: str = args['password']
        if user.password != password:
            return {"message": "The username or password is not correct.", "status": 422}

        # login success, create corresponding tokens for user
        return {
            'status': 200,
            'message': f'Logged in as {username}',
            'api_key': user.api_key
        }
