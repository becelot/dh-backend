from typing import Dict, Optional
from xml.etree import ElementTree

from flask import Flask

from dh_backend.lib.hearthstone.card import HearthstoneCard


class HSNoSuchCardException(Exception):
    def __init__(self, *args, **kwargs):
        super(HSNoSuchCardException, self).__init__("Card was not found in the database.", *args, **kwargs)


class HearthstoneDatabaseMeta(type):
    __database__: Dict[int, HearthstoneCard] = None
    initialized: bool = False
    app: Optional[Flask] = None

    def __getitem__(cls, val):
        """
        Retrieve a card instance by its ID
        :param val: The ID of the card
        :return: The card associated with the ID
        :rtype HearthstoneCard
        :raises HSNoSuchCardException: if the card_id was not found in the database
        """
        # Try to return the entry
        try:
            return cls.__database__[val]
        except TypeError:
            # if database was not loaded, initialize it, and try again
            cls.load_database()
            try:
                cls.__database__[val]
            except KeyError:
                # if ID does not exist, raise
                raise HSNoSuchCardException()
        except KeyError:
            # if ID does not exist, raise
            raise HSNoSuchCardException()

    def load_database(cls, **kwargs):
        if 'app' in kwargs:
            kwargs['app'].hs_database = cls
            cls.app = kwargs['app']

        if cls.app is not None:
            cls.app.logger.info("HearthstoneDatabase: Loading database...")

        if cls.initialized:
            return

        from hearthstone_data import get_carddefs_path
        path = get_carddefs_path()

        cls.__database__ = {}
        locale = kwargs['locale'] if 'locale' in kwargs else 'enUS'

        with open(path, "rb") as f:
            xml = ElementTree.parse(f)
            for carddata in xml.findall("Entity"):
                card = HearthstoneCard.from_xml(carddata)
                card.locale = locale
                cls.__database__[getattr(card, 'dbf_id')] = card

        cls.initialized = True


class HearthstoneDatabase(object, metaclass=HearthstoneDatabaseMeta):
    pass
