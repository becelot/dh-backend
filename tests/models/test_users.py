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
