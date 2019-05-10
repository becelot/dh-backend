from hearthstone.cardxml import CardXML
from hearthstone.enums import CardType


class HearthstoneCard(CardXML):

    def get_type(self) -> CardType:
        return self.type
