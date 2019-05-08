from dh_backend.models import db


class DeckVersion(db.Model):

    __tablename__ = 'DeckVersion'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    deck_name = db.Column(db.String(32), nullable=False)
    deck_code = db.Column(db.String, nullable=False)

    deck_id = db.Column(db.Integer, db.ForeignKey("Deck.id"), nullable=False)
    deck = db.relationship("Deck", foreign_keys=[deck_id])
