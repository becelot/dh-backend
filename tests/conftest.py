import pytest

from dh_backend import create_test_app, models
from tests import setup_db, teardown_db, clean_db


@pytest.fixture(scope="session")
def app():
    yield create_test_app()


@pytest.fixture(scope="session")
def db(app):
    """Creates clean database schema and drops it on teardown
    Note, that this is a session scoped fixture, it will be executed only once
    and shared among all tests. Use `db_session` fixture to get clean database
    before each test.
    """

    setup_db(app)
    yield models.db
    teardown_db()


@pytest.fixture(scope="function")
def db_session(db, app):
    """Provides clean database before each test. After each test,
    session.rollback() is issued.
    Return sqlalchemy session.
    """

    with app.app_context():
        clean_db()
        yield db.session
        db.session.rollback()