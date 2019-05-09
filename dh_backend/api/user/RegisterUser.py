import re

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
        username: str = data["username"]

        pattern = re.compile("^[a-zA-Z0-9]{4,24}$")
        if not pattern.match(username):
            return {"status": 400, "message": "The username has an invalid format."}

        user = User.query.filter_by(user_name=username).first()
        if user:
            return {"message": "The username already exists.", "status": 422}

        new_user = User(user_name=username, password=data["password"], email=data["email"])
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User was successfully registered", "status": 201}
