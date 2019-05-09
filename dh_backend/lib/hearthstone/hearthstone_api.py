from typing import Dict

from flask import Flask
from hearthstone import cardxml
from hearthstone.cardxml import CardXML


class HearthstoneAPI(object):
    """Utility class that provides the hearthstone API"""
    def __init__(self):
        dbf_db, _ = cardxml.load_dbf()
        self.dbf: Dict[int, CardXML] = dbf_db

    @staticmethod
    def init_app(app: Flask):
        """Add resources to global application
        :param app: The current Flask application
        :type app: Flask
        """
        api = HearthstoneAPI()

        app.hearthstone_api = api
