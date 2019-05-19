from dh_backend.models import db


class TwitchSession(db.Model):

    __tablename__ = "TwitchSession"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete="SET NULL"))
    user = db.relationship("User", back_populates="twitch_session")
    twitch_session_token: str = db.Column(db.String, nullable=True, default=None)
    code = db.Column(db.String)
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)
    expires_at = db.Column(db.Date)
    scope = db.Column(db.String)
    token_type = db.Column(db.String)
