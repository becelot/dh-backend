from dh_backend.models.Deck import Deck
from tests.data.decks import new_deck, new_deck_version


def test_deck_add(db_session):
    deck = new_deck()

    db_session.add(deck)
    db_session.commit()

    assert db_session.query(Deck).get(deck.id) is not None


def test_deck_current_version(db_session):
    deck = new_deck()

    version = new_deck_version(deck)
    db_session.add(version)
    db_session.commit()

    deck.current_version = version
    db_session.commit()

    assert deck.current_version_id == version.id
    assert deck.current_version.id == version.id

    version = new_deck_version(deck)
    db_session.add(version)
    db_session.commit()

    deck.current_version = version
    db_session.commit()

    assert deck.current_version_id == version.id
    assert deck.current_version.id == version.id


def test_deck_versions(db_session):
    deck = new_deck()

    version = new_deck_version(deck)
    version2 = new_deck_version(deck)
    db_session.add(version)
    db_session.add(version2)
    db_session.commit()

    assert len(deck.versions.all()) == 2
    assert deck.versions.filter_by(id=version.id).first() is not None
    assert deck.versions.filter_by(id=version2.id).first() is not None
