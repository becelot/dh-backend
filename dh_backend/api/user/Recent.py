from typing import List

from flask_restful import Resource

from dh_backend.models import TwitchAccount, RecentDeck, Deck


class Recent(Resource):

    @staticmethod
    def __add_to_response(deck: Deck, response: List):
        if deck and deck.current_version:
            response.append({
                'name': deck.current_version.deck_name,
                'code': deck.current_version.deck_code
            })

    def get(self, channel_id: str):
        if not channel_id:
            return {'status': 402, 'message': 'No channel id was provided'}

        account: TwitchAccount = TwitchAccount.query.filter_by(channel_id=channel_id).first()

        if not account:
            return {'status': 402, 'message': 'Channel is not currently linked'}

        recentDecks: RecentDeck = account.user.recent_decks

        if not recentDecks:
            return {'status': 402, 'message': 'No recent decks were found'}

        decks = []
        Recent.__add_to_response(recentDecks.current_deck, decks)
        Recent.__add_to_response(recentDecks.previous_deck, decks)
        Recent.__add_to_response(recentDecks.deck_3, decks)
        Recent.__add_to_response(recentDecks.deck_4, decks)
        Recent.__add_to_response(recentDecks.deck_5, decks)

        return {'status': 200, 'message': 'Recent decks retrieved', 'decks': decks}
