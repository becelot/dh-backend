import pytest
from sqlalchemy.exc import IntegrityError

from dh_backend.models import User
from tests.data.users import test_user


def test_user_create(db_session):
    admin = User(user_name="admin", password="test", email="NoneMail")
    db_session.add(admin)
    db_session.commit()

    assert db_session.query(User).get(admin.id) is not None


def test_user_bulk_create(db_session):
    from tests.data.users import test_users
    users = test_users()

    for u in users:
        db_session.add(u)
    db_session.commit()


def test_user_already_exists_exception(db_session):
    testuser1 = test_user()
    testuser2 = test_user()

    db_session.add(testuser1)
    db_session.commit()

    with pytest.raises(IntegrityError):
        db_session.add(testuser2)
        db_session.commit()


def test_user_delete(db_session):
    test_user_create(db_session)
    user = db_session.query(User).filter_by(user_name="admin").first()

    assert user is not None

    db_session.delete(user)

    assert db_session.query(User).filter_by(user_name="admin").first() is None


def test_user_recent_decks(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    assert user.recent_decks is None

    from dh_backend.models import RecentDeck
    recent = RecentDeck(user=user)
    db_session.add(recent)
    db_session.commit()

    assert user.recent_decks is not None


def test_user_generate_api_key(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    old_key = user.api_key
    assert len(old_key) > 90

    user.generate_new_api_key()
    db_session.commit()

    assert len(user.api_key) > 90
    assert user.api_key != old_key
