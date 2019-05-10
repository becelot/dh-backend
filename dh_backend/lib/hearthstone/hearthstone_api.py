from typing import Dict, Optional
from xml.etree import ElementTree

from flask import Flask

from dh_backend.lib.hearthstone.card import HearthstoneCard


class HSInitException(Exception):
    def __init__(self, *args, **kwargs):
        super(HSInitException, self).__init__("HearthstoneAPI is not properly initialized", *args, **kwargs)


class HSNoSuchCardException(Exception):
    def __init__(self, *args, **kwargs):
        super(HSNoSuchCardException, self).__init__("Card was not found in the database.", *args, **kwargs)


class HearthstoneAPI(object):
    """Utility class that provides the hearthstone API"""

    __instance__ = None

    @staticmethod
    def instance() -> 'HearthstoneAPI':
        """
        Returns the singleton instance of the hearthstone api class.
        :return: The instance of the API object
        :rtype HearthstonAPI
        :raises HSInitException: if the instance has not been initialized
        """
        if HearthstoneAPI.__instance__ is None:
            raise HSInitException()

        return HearthstoneAPI.__instance__

    def __init__(self):
        self.dbf_db: Dict[int, HearthstoneCard] = self._load(None, "enUS", "dbf_id")

    @staticmethod
    def _load(path, locale, attr) -> Dict[int, HearthstoneCard]:
        from hearthstone_data import get_carddefs_path

        if path is None:
            path = get_carddefs_path()

        db = {}

        with open(path, "rb") as f:
            xml = ElementTree.parse(f)
            for carddata in xml.findall("Entity"):
                card = HearthstoneCard.from_xml(carddata)
                card.locale = locale
                db[getattr(card, attr)] = card

        return db

    @staticmethod
    def init_app(app: Flask):
        """Add resources to global application
        :param app: The current Flask application
        :type app: Flask
        """
        api = HearthstoneAPI()
        HearthstoneAPI.__instance__ = api
        app.hearthstone_api = api

    def get_card(self, card_id: int) -> HearthstoneCard:
        """
        Retrieve a card instance by its ID
        :param card_id: The ID of the card
        :return: The card associated with the ID
        :rtype HearthstoneCard
        :raises HSNoSuchCardException: if the card_id was not found in the database
        """
        card = self.dbf_db[card_id]
        if card is None:
            raise HSNoSuchCardException()

        return card


HSDatabase = Dict[int, HearthstoneCard]
__db_cache__: Optional[HSDatabase] = None


def init_app(**kwargs):
    """
    Load all resources for the HearthstoneAPI into memory.
    :param app: The app that initializes the API
    """
    if __db_cache__ is not None:
        return

    from hearthstone_data import get_carddefs_path
    path = get_carddefs_path()

    global __db_cache__
    __db_cache__ = {}
    locale = kwargs['locale'] if kwargs['locale'] else 'enUS'

    with open(path, "rb") as f:
        xml = ElementTree.parse(f)
        for carddata in xml.findall("Entity"):
            card = HearthstoneCard.from_xml(carddata)
            card.locale = locale
            __db_cache__[getattr(card, 'dbf_id')] = card


def inject_db(fn):
    def wrapper(*args, **kwargs):
        global __db_cache__
        try:
            fn(*args, card_db=__db_cache__, **kwargs)
        except:
            init_app()
            fn(*args, card_db=__db_cache__, **kwargs)
    return wrapper


@inject_db
def get_card(card_id: int, card_db: HSDatabase) -> HearthstoneCard:
    """
    Retrieve a card instance by its ID
    :param card_id: The ID of the card
    :param card_db: The database to use. Parameter is automatically injected by inject db
    :return: The card associated with the ID
    :rtype HearthstoneCard
    :raises HSNoSuchCardException: if the card_id was not found in the database
    """
    card = card_db[card_id]

    if card is None:
        raise HSNoSuchCardException()

    return card
