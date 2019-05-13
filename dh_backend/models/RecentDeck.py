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

    def set_recent_deck(self, deck: Deck):
        """
        Update the list of decks with a new deck
        :param deck: The deck to insert into the list
        """
        if deck == self.current_deck:
            return

        tmp = self.previous_deck
        self.previous_deck = self.current_deck
        self.current_deck = deck

        if deck == tmp:
            return

        tmp2 = self.deck_3
        self.deck_3 = tmp

        if deck == tmp2:
            return

        tmp = self.deck_4
        self.deck_4 = tmp2

        if deck == tmp:
            return

        self.deck_5 = tmp
