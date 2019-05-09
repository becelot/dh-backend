from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from flask_restful import reqparse

from dh_backend.models import User, Deck


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

        # Get current deck of the user and check, if they are the same
        deck: Deck = user.recent_decks.current_deck
        if deck.current_version.deck_code == args.get("deckstring"):
            return {'status': 422, 'message': 'Deck was already uploaded'}
