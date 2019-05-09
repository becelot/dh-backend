from dh_backend.models import db, Deck


class RecentDeck(db.Model):

    __tablename__ = 'RecentDeck'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete="CASCADE"))
    user = db.relationship("User", back_populates="recent_decks")

    current_deck_id = db.Column(db.Integer, db.ForeignKey("Deck.id"), nullable=True)
    current_deck: Deck = db.relationship("Deck", foreign_keys=[current_deck_id])

    previous_deck_id = db.Column(db.Integer, db.ForeignKey("Deck.id"), nullable=True)
    previous_deck = db.relationship("Deck", foreign_keys=[previous_deck_id])

    deck_3_id = db.Column(db.Integer, db.ForeignKey("Deck.id"), nullable=True)
    deck_3 = db.relationship("Deck", foreign_keys=[deck_3_id])

    deck_4_id = db.Column(db.Integer, db.ForeignKey("Deck.id"), nullable=True)
    deck_4 = db.relationship("Deck", foreign_keys=[deck_4_id])

    deck_5_id = db.Column(db.Integer, db.ForeignKey("Deck.id"), nullable=True)
    deck_5 = db.relationship("Deck", foreign_keys=[deck_5_id])
