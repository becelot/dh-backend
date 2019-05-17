from enum import IntEnum
from itertools import chain
from typing import List, Optional, Iterable

from flask_restful import Resource
from flask_restful import reqparse
from sqlalchemy import and_

from dh_backend.lib.hearthstone.deck import HearthstoneDeck, HSDeckParserException
from dh_backend.models import User, Deck, DeckVersion, db


class DeckMatch(IntEnum):
    NO_MATCH = 0
    INEXACT_MATCH = 1
    EXACT_MATCH = 2


class UploadDeck(Resource):
    """Upload a new deck to the database that the user is currently playing. Requires the user to be logged in!"""

    parser = reqparse.RequestParser()\
        .add_argument('deckname', type=str, location='json', required=True, help="Deckname is required") \
        .add_argument('deckstring', type=str, location='json', required=True, help="Deck code is required")\
        .add_argument('client_key', type=str, location='json', required=True, help="The client key identifying the user"
                                                                                   "was not provided")
    """
    Expected input format for this resource is:
        - deckname: string -> name of the deck that the user plays
        - deckstring: string -> the hearthstone deck code identifying the deck
        - user_key: string -> the api key identifying the user
    """
    def post(self):
        """Upload a new deck to the tracker"""
        args = UploadDeck.parser.parse_args()

        # Get the identity of the uploader
        client_key = args['client_key']
        user: User = User.query.filter_by(api_key=client_key).first()
        if user is None:
            return {'status': 401, 'message': 'The username could not be verified'}

        # Validate new deckcode
        deckcode: str = args.get("deckstring")
        try:
            new_deck: HearthstoneDeck = HearthstoneDeck.parse_deck(deckcode)
        except HSDeckParserException:
            return {'status': 400, 'message': 'Invalid deck string'}

        # Try to compare to most recent decks
        recent_decks: List[Deck] = [
            user.recent_decks.current_deck,
            user.recent_decks.previous_deck,
            user.recent_decks.deck_3,
            user.recent_decks.deck_4,
            user.recent_decks.deck_5,
        ]

        # build a custom iterator that first emits all recent decks, and the the others
        decks_iterator: Iterable[Deck] = chain(
            recent_decks,
            Deck.query.filter(
                and_(Deck.user == user,
                     ~Deck.id.in_(filter(lambda x: x is not None,
                                         map(lambda x: x.id if x is not None else None,
                                             recent_decks
                                             )
                                         )
                                  )
                     )
            ).yield_per(100)
        )

        # try to find deck in existing ones
        deck_match, deck_result = UploadDeck.find_similar_deck(new_deck, decks_iterator)

        # an exact match was found
        if deck_match == DeckMatch.EXACT_MATCH:
            user.recent_decks.set_recent_deck(deck_result)
            db.session.commit()

            return {'status': 200, 'message': 'Deck uploaded successfully'}
        elif deck_match == DeckMatch.NO_MATCH:
            # it is a completely new archetype that the user has not played before, create new deck
            deck_result = Deck(user=user)
            db.session.add(deck_result)
            db.session.commit()

        # create a new version for the deck
        version = DeckVersion(deck_name=args['deckname'], deck_code=deckcode, deck=deck_result)
        db.session.add(version)
        db.session.commit()

        deck_result.current_version = version
        user.recent_decks.set_recent_deck(deck_result)
        db.session.commit()

        # and return success message
        return {'status': 200, 'message': 'Deck uploaded successfully'}

    @staticmethod
    def find_similar_deck(new_deck: HearthstoneDeck, decks: Iterable[Deck]) -> (DeckMatch, Optional[Deck]):
        for deck in decks:
            if deck:

                # Get most recent version of the deck
                current_version: DeckVersion = deck.current_version
                if current_version:

                    # If they are the same, then cancel
                    if current_version.deck_code == new_deck.deckcode:
                        return DeckMatch.EXACT_MATCH, deck

                    # compare the two deck lists for similarity
                    current_deck: HearthstoneDeck = HearthstoneDeck.parse_deck(current_version.deck_code)
                    if not UploadDeck.significant_change(new_deck, current_deck):
                        # if the decks are not the same, but similar enough, create a new version for the deck
                        return DeckMatch.INEXACT_MATCH, deck

        return DeckMatch.NO_MATCH, None

    @staticmethod
    def significant_change(deck_1: HearthstoneDeck, deck_2: HearthstoneDeck, threshold: int = 5) -> bool:
        """
        Detect if the two provided decks differ by a significant amount
        :param deck_1: The first deck to compare
        :param deck_2: The deck that the first one is compared to
        :param threshold: The threshold used to determine if decks differ significantly. Defaults to 5.
        :return true iff the decks differs in threshold cards
        """

        # First, check if the classes match
        if deck_1.get_hero_class() != deck_2.get_hero_class():
            return True

        # if the decks differ in at most threshold cards
        return deck_1.compare(deck_2, threshold+1) > threshold
