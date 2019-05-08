

def test_deck_add(db_session):
    from dh_backend.models.Deck import Deck
    deck = Deck()

    db_session.add(deck)
    db_session.commit()

    assert db_session.query(Deck).get(deck.id) is not None
