from dh_backend.models import db


class Deck(db.Model):

    __tablename__ = 'Deck'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
