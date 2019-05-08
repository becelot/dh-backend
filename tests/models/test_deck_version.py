import pytest
from sqlalchemy.exc import IntegrityError

from dh_backend.models import DeckVersion
from tests.data.decks import new_deck, new_deck_version


def test_deck_version_add(db_session):
    deck = new_deck()
    db_session.add(deck)
    db_session.commit()

    version = new_deck_version(deck)
    db_session.add(version)
    db_session.commit()

    db_session.add(version)
    db_session.commit()

    assert db_session.query(DeckVersion).filter_by(id=version.id).first() is not None


def test_version_requires_reference_to_deck(db_session):
    with pytest.raises(IntegrityError):
        version = DeckVersion(deck_name="Control Warrior", deck_code="==asfnjweg")
        db_session.add(version)
        db_session.commit()


def test_version_deck(db_session):
    deck = new_deck()
    db_session.add(deck)
    db_session.commit()

    version = new_deck_version(deck)
    db_session.add(version)
    db_session.commit()

    assert version.deck_id == deck.id
    assert version.deck.id == deck.id
