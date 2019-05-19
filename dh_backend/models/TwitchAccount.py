from dh_backend.models import db


class TwitchAccount(db.Model):

    __tablename__ = "TwitchAccount"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id", ondelete="SET NULL"))
    user = db.relationship("User", back_populates="twitch_account")
    channel_id = db.Column(db.String)
    login = db.Column(db.String)
    display_name = db.Column(db.String)
    type = db.Column(db.String)
    broadcaster_type = db.Column(db.String)
    description = db.Column(db.String)
    view_count = db.Column(db.Integer)
    email = db.Column(db.Integer)
