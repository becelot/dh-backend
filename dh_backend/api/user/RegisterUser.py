from flask import request
from flask_restful import Resource

from dh_backend.models import db, User


class RegisterUser(Resource):
    """Register a new user in the application. Expected request format is:
        - username: string -> the username of the new user
        - password: string -> the password as a hashed string
        - email: string -> email address of the user
    """
    def post(self):
        data = request.get_json()
        username = data["username"]

        user = User.query.filter_by(user_name=username).first()
        if user:
            return {"message": "User already exists", "status": 500}

        new_user = User(user_name=username, password=data["password"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User successfully registered", "status": 200}
