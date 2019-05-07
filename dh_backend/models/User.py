from dh_backend.models import db


class User(db.Model):
    """Streamer table."""
    __tablename__ = 'User'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    twitch_name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)