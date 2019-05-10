from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful import reqparse

from dh_backend.lib.hearthstone.deck import HearthstoneDeck, HSDeckParserException
from dh_backend.models import User, Deck, DeckVersion


class UploadDeck(Resource):
    """Upload a new deck to the database that the user is currently playing. Requires the user to be logged in!"""

    parser = reqparse.RequestParser()\
        .add_argument('deckname', type=str, location='json', required=True, help="Deckname is required") \
        .add_argument('deckstring', type=str, location='json', required=True, help="Deck code is required")
    """
    Expected input format for this resource is:
        - deckname: string -> name of the deck that the user plays
        - deckstring: string -> the hearthstone deck code identifying the deck
    """

    @jwt_required
    def post(self):
        """Upload a new deck to the tracker"""
        args = UploadDeck.parser.parse_args()

        # Get the identity of the uploader
        username = get_jwt_identity()
        user: User = User.query.filter_by(user_name=username).first()
        if user is None:
            return {'status': 401, 'message': 'The username could not be verified'}, 401

        # Validate new deckcode
        deckcode: str = args.get("deckstring")
        try:
            new_deck: HearthstoneDeck = HearthstoneDeck.parse_deck(deckcode)
        except HSDeckParserException:
            return {'status': 400, 'message': 'Invalid deck string'}

        # Try to compare to current deck
        deck: Deck = user.recent_decks.current_deck
        if deck:

            # Get most recent version
            current_version: DeckVersion = deck.current_version
            if current_version:

                # If they are the same, then cancel
                if current_version.deck_code == deckcode:
                    return {'status': 422, 'message': 'Deck was already uploaded'}

                # compare the two deck lists
                current_deck: HearthstoneDeck = HearthstoneDeck.parse_deck(current_version.deck_code)
                self.significant_change(new_deck, current_deck)

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
            return False

        # if the decks differ in at most threshold cards
        return deck_1.compare(deck_2, threshold+1) > threshold
