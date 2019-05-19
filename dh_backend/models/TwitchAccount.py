from dh_backend.lib.twitch import twitch
from dh_backend.lib.twitch.models import TwitchUser
from dh_backend.models import db, User


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

    @staticmethod
    def from_user(user: User) -> 'TwitchAccount':
        twitch_user: TwitchUser = twitch.user(user)
        account: TwitchAccount = TwitchAccount(user=user)

        account.channel_id = twitch_user.id
        account.login = twitch_user.login
        account.display_name = twitch_user.display_name
        account.type = twitch_user.type
        account.broadcaster_type = twitch_user.broadcaster_type
        account.description = twitch_user.description
        account.view_count = twitch_user.view_count
        account.email = twitch_user.email

        return account
