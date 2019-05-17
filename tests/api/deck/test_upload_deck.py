import json
from typing import List, Tuple

from flask.testing import FlaskClient

from dh_backend.models import RecentDeck, User
from tests.data.decks import TokenDruid, SilencePriest, MurlocShaman, EvenWarlock, SummonMage, SecretPaladin, \
    PirateRogue, TokenDruid2, SummonMage2, SecretMage
from tests.data.users import test_user


def test_client_key_required(client: FlaskClient):

    response = client.post('/api/deck/upload',
                           data=json.dumps({
                               'deckname': 'Test deck',
                               'deckstring': 'Nope'
                           }),
                           content_type='application/json')

    assert response.status_code == 400


def test_client_key_invalid(client: FlaskClient):
    response = client.post('/api/deck/upload',
                           data=json.dumps({
                               'deckname': 'Test deck',
                               'deckstring': 'Nope',
                               'client_key': 'some random key'
                           }),
                           content_type='application/json')

    assert response.json['status'] == 401


def test_deck_code_invalid(client: FlaskClient, db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    response = client.post('/api/deck/upload',
                           data=json.dumps({
                               'deckname': 'Test deck',
                               'deckstring': 'Nope',
                               'client_key': user.api_key
                           }),
                           content_type='application/json')

    assert response.json['status'] == 400


def setup_user(db_session):
    user = test_user()
    db_session.add(user)
    db_session.commit()

    user2 = User(user_name="InvalidUser", password="NoPassword", email="Yep, thats me")
    db_session.add(user2)
    db_session.commit()

    recent_deck = RecentDeck(user=user)
    db_session.add(recent_deck)
    db_session.commit()

    return user


TestSpec = List[Tuple[int, Tuple[int, int, int, int, int]]]


def run_cases(client: FlaskClient, user: User, decks: List[str], tests: TestSpec):
    for test in tests:
        response = client.post('/api/deck/upload',
                               data=json.dumps({
                                   'deckname': 'Test deck',
                                   'deckstring': decks[test[0]],
                                   'client_key': user.api_key
                               }),
                               content_type='application/json')

        assert response.status_code == 200
        assert (None if test[1][0] is None else user.recent_decks.current_deck.current_version.deck_code) == \
               (None if test[1][0] is None else decks[test[1][0]])
        assert (None if test[1][1] is None else user.recent_decks.previous_deck.current_version.deck_code) == \
               (None if test[1][1] is None else decks[test[1][1]])
        assert (None if test[1][2] is None else user.recent_decks.deck_3.current_version.deck_code) == \
               (None if test[1][2] is None else decks[test[1][2]])
        assert (None if test[1][3] is None else user.recent_decks.deck_4.current_version.deck_code) == \
               (None if test[1][3] is None else decks[test[1][3]])
        assert (None if test[1][4] is None else user.recent_decks.deck_5.current_version.deck_code) == \
               (None if test[1][4] is None else decks[test[1][4]])


def test_upload_deck_no_match(client: FlaskClient, db_session):
    user = setup_user(db_session)

    decks = [
        TokenDruid,
        SilencePriest,
        MurlocShaman,
        EvenWarlock,
        SummonMage,
        SecretPaladin,
        PirateRogue
    ]

    tests = [
        (0, (0, None, None, None, None)),
        (1, (1, 0, None, None, None)),
        (2, (2, 1, 0, None, None)),
        (3, (3, 2, 1, 0, None)),
        (4, (4, 3, 2, 1, 0)),
        (5, (5, 4, 3, 2, 1)),
        (6, (6, 5, 4, 3, 2))
    ]

    run_cases(client, user, decks, tests)
    assert len(user.decks.all()) == 7


def test_upload_deck_exact_match(client: FlaskClient, db_session):
    user = setup_user(db_session)

    decks = [
        TokenDruid,
        SilencePriest,
        MurlocShaman,
        EvenWarlock,
        SummonMage,
        SecretPaladin,
        PirateRogue,
        SecretMage
    ]

    tests = [
        (0, (0, None, None, None, None)),
        (1, (1, 0, None, None, None)),
        (2, (2, 1, 0, None, None)),
        (3, (3, 2, 1, 0, None)),
        (4, (4, 3, 2, 1, 0)),
        (5, (5, 4, 3, 2, 1)),
        (6, (6, 5, 4, 3, 2)),
        (3, (3, 6, 5, 4, 2)),
        (1, (1, 3, 6, 5, 4)),
        (7, (7, 1, 3, 6, 5))
    ]

    run_cases(client, user, decks, tests)
    assert len(user.decks.all()) == 8


def test_upload_deck_inexact_match(client: FlaskClient, db_session):
    # todo: verify decklist strings in endpoint
    user = setup_user(db_session)

    decks = [
        TokenDruid,
        SilencePriest,
        MurlocShaman,
        EvenWarlock,
        SummonMage,
        SecretPaladin,
        PirateRogue,
        SecretMage,
        TokenDruid2,
        SummonMage2,
    ]

    tests = [
        (0, (0, None, None, None, None)),
        (1, (1, 0, None, None, None)),
        (2, (2, 1, 0, None, None)),
        (3, (3, 2, 1, 0, None)),
        (4, (4, 3, 2, 1, 0)),
        (5, (5, 4, 3, 2, 1)),
        (6, (6, 5, 4, 3, 2)),
        (3, (3, 6, 5, 4, 2)),
        (9, (9, 3, 6, 5, 2)),
        (8, (8, 9, 3, 6, 5)),
        (7, (7, 8, 9, 3, 6))
    ]

    run_cases(client, user, decks, tests)
    assert len(user.decks.all()) == 8
