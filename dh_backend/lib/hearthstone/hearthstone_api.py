from dh_backend.lib.hearthstone.card import HearthstoneCard
from dh_backend.lib.hearthstone.database import HearthstoneDatabase


class HSInitException(Exception):
    def __init__(self, *args, **kwargs):
        super(HSInitException, self).__init__("HearthstoneAPI is not properly initialized", *args, **kwargs)


def get_card(card_id: int) -> HearthstoneCard:
    """
    Retrieve a card instance by its ID
    :param card_id: The ID of the card
    :return: The card associated with the ID
    :rtype HearthstoneCard
    :raises HSNoSuchCardException: if the card_id was not found in the database
    """
    return HearthstoneDatabase[card_id]


def init_app(**kwargs):
    """
    Load all resources for the HearthstoneAPI into memory.
    :param app: The app that initializes the API
    """
    HearthstoneDatabase.load_database(**kwargs)
