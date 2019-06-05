from enum import IntEnum

from dh_backend.models import db


class GameResult(IntEnum):
    RESULT_UNKNOWN = 0
    RESULT_WIN = 1
    RESULT_LOSS = 2
    RESULT_DRAW = 3


class Game(db.Model):
    __tablename__ = 'game'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    opponent_name = db.Column(db.String)
    opponent_deck = db.Column(db.String)
    time = db.Column(db.DateTime)
    result = db.Column(db.Enum(GameResult))

    deck_version_id = db.Column(db.Integer, db.ForeignKey('DeckVersion.id', ondelete="SET NULL"))
    deck_version = db.relationship('DeckVersion', back_populates='games')
