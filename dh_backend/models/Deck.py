from dh_backend.models import db


class Deck(db.Model):

    __tablename__ = 'Deck'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    current_version_id = db.Column(db.Integer, db.ForeignKey("DeckVersion.id", ondelete="SET NULL"), nullable=True)
    current_version = db.relationship("DeckVersion", uselist=False, foreign_keys=[current_version_id], post_update=True)

    versions = db.relationship("DeckVersion", primaryjoin="Deck.id==DeckVersion.deck_id", post_update=True,
                               cascade="all,delete", lazy="dynamic")
