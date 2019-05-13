from dh_backend.models import RecentDeck, Deck
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


def test_recent_decks_update(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    recent = RecentDeck(user=user)
    db_session.add(recent)
    db_session.commit()

    decks = [
        Deck(user=user),
        Deck(user=user),
        Deck(user=user),
        Deck(user=user),
        Deck(user=user),
        Deck(user=user),
        Deck(user=user)
    ]
    for deck in decks:
        db_session.add(deck)
    db_session.commit()

    validity_set = [
        (0, (0, None, None, None, None)),
        (1, (1, 0, None, None, None)),
        (2, (2, 1, 0, None, None)),
        (3, (3, 2, 1, 0, None)),
        (4, (4, 3, 2, 1, 0)),
        (5, (5, 4, 3, 2, 1)),
        (2, (2, 5, 4, 3, 1)),
        (1, (1, 2, 5, 4, 3)),
        (6, (6, 1, 2, 5, 4)),
        (6, (6, 1, 2, 5, 4)),
        (1, (1, 6, 2, 5, 4)),
        (2, (2, 1, 6, 5, 4)),
    ]

    for test in validity_set:
        recent.set_recent_deck(decks[test[0]])

        assert recent.current_deck == (None if test[1][0] is None else decks[test[1][0]])
        assert recent.previous_deck == (None if test[1][1] is None else decks[test[1][1]])
        assert recent.deck_3 == (None if test[1][2] is None else decks[test[1][2]])
        assert recent.deck_4 == (None if test[1][3] is None else decks[test[1][3]])
        assert recent.deck_5 == (None if test[1][4] is None else decks[test[1][4]])
