from dh_backend.models import RecentDeck
from tests.data.users import test_user


def test_recent_decks_add(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    recent = RecentDeck(user=user)
    db_session.add(recent)
    db_session.commit()

    assert db_session.query(RecentDeck).filter_by(id=recent.id).first() is not None


def test_recent_decks_user(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    recent = RecentDeck(user=user)
    db_session.add(recent)
    db_session.commit()

    assert recent.user_id == user.id
    assert recent.user.id == user.id


def test_delete_user_deletes_recent(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    recent = RecentDeck(user=user)
    db_session.add(recent)
    db_session.commit()

    db_session.delete(user)
    db_session.commit()

    assert db_session.query(RecentDeck).filter_by(id=recent.id).first() is None
