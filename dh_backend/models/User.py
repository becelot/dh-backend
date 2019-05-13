import secrets

from dh_backend.models import db, RecentDeck


def generate_new_key():
    new_key: str = secrets.token_urlsafe(98)
    while User.query.filter_by(api_key=new_key).first() is not None:
        new_key = secrets.token_urlsafe(98)  # pragma: no cover

    return new_key


class User(db.Model):
    """Streamer table."""
    __tablename__ = 'User'

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String, nullable=False, unique=True)
    twitch_name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    recent_decks: RecentDeck = db.relationship("RecentDeck", uselist=False, back_populates="user", cascade="all,delete")
    decks = db.relationship("Deck", back_populates="user")
    api_key: str = db.Column(db.String, nullable=False, default=generate_new_key)

    def generate_new_api_key(self):
        self.api_key = generate_new_key()
