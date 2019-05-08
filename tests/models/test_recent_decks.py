from dh_backend.models import RecentDeck
from tests.data.decks import new_deck
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


def test_recent_user_one_to_one(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    recent = RecentDeck(user=user)
    db_session.add(recent)
    db_session.commit()

    deck = new_deck()
    recent.current_deck = deck
    db_session.commit()

    recent2 = RecentDeck(user=user)
    db_session.add(recent2)
    db_session.commit()

    assert len(db_session.query(RecentDeck).filter_by(user_id=user.id).all()) == 1
