import binascii
from typing import Optional, List, Tuple, Iterator

from hearthstone.deckstrings import Deck
from hearthstone.enums import CardClass, CardType

from dh_backend.lib.hearthstone import get_card
from dh_backend.lib.hearthstone.card import HearthstoneCard


class HSDeckParserException(Exception):
    pass


class HSDeckNoHeroException(Exception):
    pass


class HearthstoneDeck(Deck):
    def __init__(self, deck: Optional['HearthstoneDeck'] = None):
        super(HearthstoneDeck, self).__init__()
        self.deckcode = ""
        if deck:
            self.heroes: List[int] = list(deck.heroes)
            self.cards = list(deck.cards)
            self.format = deck.format
            self.deckcode = deck.deckcode

    @classmethod
    def parse_deck(cls, deckcode: str):
        """
        Parse a deckcode and return the corresponding deck instance
        :param deckcode: The deckcode to be parsed
        :return: Instance of the parsed deck
        :rtype Deck
        :raises HSDeckParserException: if the deckcode was invalid
        """
        try:
            result = cls.from_deckstring(deckcode)
            result.deckcode = deckcode
            return result
        except ValueError or binascii.Error:
            raise HSDeckParserException("Error while parsing deckcode")

    def get_hero_class(self) -> CardClass:
        """Get the class associated with the deck"""
        hero_id = self.heroes[0]
        hero: HearthstoneCard = get_card(hero_id)

        if hero.get_type() != CardType.HERO:
            return CardClass.INVALID

        return hero.card_class

    def get_real_cards(self) -> Iterator[Tuple[HearthstoneCard, int]]:
        """
        Transform the cardid list into a list containing real cards
        :return: A list containing references to actual hearthstone cards
        """
        return map(lambda x: (get_card(x[0]), x[1]), self.get_dbf_id_list())

    def get_cards_in_deck_order(self) -> Iterator[Tuple[HearthstoneCard, int]]:
        """
        Get the cards in deck order. Sort it first on name, then on cost.
        :return: A deck in display deck order
        """
        return sorted(
            sorted(self.get_real_cards(), key=lambda x: x[0].name),
            key=lambda x: x[0].cost
        )

    def compare(self, other, threshold=60):
        """
        Compare this deck to another one
        :param other: The deck that this deck is compared to
        :type other: Deck
        :param threshold: After the difference threshold is reached, the algorithm will break. Defaults to 60, the
                          maximum difference between decks (adventure decks may contain more cards)
        :type threshold: int
        :return: The number of cards the decks differ in
        :rtype int
        """
        # Convert both decks to a list of contained cards, sorted by ID
        sorted1 = self.get_dbf_id_list()
        sorted2 = other.get_dbf_id_list()

        # Compare the two decks iteratively
        diff = 0
        j = 0  # pointer to current position in deck2
        for i in range(len(sorted1)):
            # if j is out of bounds, the cards differ
            if j >= len(sorted2):
                diff += sorted1[i][1]
                continue

            # if the ID of the current position in deck1 matches that of deck2
            if sorted1[i][0] == sorted2[j][0]:
                # if the count differs, add difference and point to the next position in deck2
                diff += abs(sorted1[i][1] - sorted2[j][1])
                j += 1
            else:
                # the ID on the current position differs, and the first ID is smaller than the second, count and inc i
                if sorted1[i][0] < sorted2[j][0]:
                    diff += sorted1[i][1]
                else:
                    # otherwise catch up j, but don't count the diff, as we count number of cards changed
                    while j < len(sorted2) and sorted1[i][0] > sorted2[j][0]:
                        j += 1

                    # if j is still in bounds, and the current IDs match, j has to be advanced
                    if j < len(sorted2) and sorted1[i][0] == sorted2[j][0]:
                        # if the count differs, add difference and point to the next position in deck2
                        diff += abs(sorted1[i][1] - sorted2[j][1])
                        j += 1
                    else:
                        # otherwise, the cards differ trivially
                        diff += sorted1[i][1]

            # if difference is bigger than threshold, cancel prematurely
            if diff >= threshold:
                return threshold

        return diff if diff <= threshold else threshold
