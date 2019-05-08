from dh_backend.models import DeckVersion, Deck


def new_deck():
    return Deck()


def new_deck_version(deck):
    return DeckVersion(deck_name="TestDeck", deck_code="==saf", deck=deck)
