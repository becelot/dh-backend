from dh_backend.models import DeckVersion


def test_deck_version_add(db_session):
    deck = DeckVersion(deck_name="Control Warrior", deck_code="something")

    db_session.add(deck)
    db_session.commit()

    assert db_session.query(DeckVersion).get(deck.id) is not None
