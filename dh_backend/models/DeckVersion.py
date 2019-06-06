from datetime import datetime

from dh_backend.models import db


class DeckVersion(db.Model):

    __tablename__ = 'DeckVersion'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    deck_name = db.Column(db.String(32), nullable=False)
    deck_code = db.Column(db.String, nullable=False)

    loss_count = db.Column(db.Integer, default=0)
    win_count = db.Column(db.Integer, default=0)

    last_played = db.Column(db.DateTime, default=datetime.now)

    deck_id = db.Column(db.Integer, db.ForeignKey("Deck.id"), nullable=False)
    deck = db.relationship("Deck", foreign_keys=[deck_id])

    games = db.relationship('Game', back_populates='deck_version')
