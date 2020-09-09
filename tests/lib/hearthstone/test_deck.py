from typing import List, Tuple

from hearthstone.enums import FormatType, CardClass

from dh_backend.lib.hearthstone.deck import HearthstoneDeck


def build_deck(ids: List[Tuple[int, int]]) -> HearthstoneDeck:
    deck = HearthstoneDeck()
    deck.heroes = [7]
    deck.format = FormatType.FT_STANDARD
    deck.cards = ids

    return deck


def test_compare_deck_equal():
    deck1 = HearthstoneDeck.parse_deck("AAECAf0ECsUE7QWQB+wHvwj7DKCAA6aHA8CYA4qeAwpNigG7AskDqwTLBJYF4Qe+7AKDlgMA")
    deck2 = HearthstoneDeck.parse_deck("AAECAf0ECsUE7QWQB+wHvwj7DKCAA6aHA8CYA4qeAwpNigG7AskDqwTLBJYF4Qe+7AKDlgMA")

    assert deck1.compare(deck2) == 0


def test_compare_positive_card_count_change():
    deck1 = build_deck([(0, 1)])
    deck2 = build_deck([(0, 2)])

    assert deck1.compare(deck2) == 1


def test_compare_negative_card_count_change():
    deck1 = build_deck([(0, 1)])
    deck2 = build_deck([(0, 0)])

    assert deck1.compare(deck2) == 1


def test_deck_1_ends_with_higher_id():
    deck1 = build_deck([(1, 1)])
    deck2 = build_deck([(0, 1)])

    assert deck1.compare(deck2) == 1


def test_deck_1_ends_with_lower_id():
    deck1 = build_deck([(0, 1)])
    deck2 = build_deck([(1, 1)])

    assert deck1.compare(deck2) == 1


def test_deck_compare_single_change():
    deck1 = HearthstoneDeck.parse_deck("AAEBAc2xAgRxngG/CKLTAg27AqsEtATmBJYF7AXBwQKYxAKP0wL77AKV/wK5/wKjhwMA")
    deck2 = HearthstoneDeck.parse_deck("AAEBAc2xAgRxvwiEuwKi0wINuwKrBLQE5gSWBewFwcECmMQCj9MC++wClf8Cuf8Co4cDAA==")

    assert deck1.compare(deck2) == 1
    assert deck2.compare(deck1) == 1


def test_deck_maxmimum_distance():
    deck1 = HearthstoneDeck.parse_deck("AAEBAc2xAgRxngG/CKLTAg27AqsEtATmBJYF7AXBwQKYxAKP0wL77AKV/wK5/wKjhwMA")
    deck2 = HearthstoneDeck.parse_deck("AAEBAf0GBooB+wegzgLCzgKX0wLN9AIM8gX7BooHtgfhB40I58sC8dAC/dACiNIC2OUC6uYCAA==")

    assert deck1.compare(deck2, 100) == 30


def test_deck_compare_threshold():
    deck1 = HearthstoneDeck.parse_deck("AAEBAc2xAgRxngG/CKLTAg27AqsEtATmBJYF7AXBwQKYxAKP0wL77AKV/wK5/wKjhwMA")
    deck2 = HearthstoneDeck.parse_deck("AAEBAf0GBooB+wegzgLCzgKX0wLN9AIM8gX7BooHtgfhB40I58sC8dAC/dACiNIC2OUC6uYCAA==")

    assert deck1.compare(deck2, 15) == 15


def test_deck_compare_threshold_symmetry():
    deck1 = HearthstoneDeck.parse_deck("AAEBAc2xAgRxngG/CKLTAg27AqsEtATmBJYF7AXBwQKYxAKP0wL77AKV/wK5/wKjhwMA")
    deck2 = HearthstoneDeck.parse_deck("AAEBAf0GBooB+wegzgLCzgKX0wLN9AIM8gX7BooHtgfhB40I58sC8dAC/dACiNIC2OUC6uYCAA==")

    assert deck1.compare(deck2, 28) == 28
    assert deck2.compare(deck1, 28) == 28


def test_copy_constructor():
    deck1 = HearthstoneDeck.parse_deck("AAEBAc2xAgRxngG/CKLTAg27AqsEtATmBJYF7AXBwQKYxAKP0wL77AKV/wK5/wKjhwMA")
    deck2 = HearthstoneDeck(deck1)

    assert len(deck1.heroes) == len(deck2.heroes)
    assert all([h1 == h2 for h1, h2 in zip(deck1.heroes, deck2.heroes)])
    assert deck1.deckcode == deck2.deckcode
    assert deck1.format == deck2.format
    assert len(deck1.cards) == len(deck2.cards)
    assert all([h1[0] == h2[0] and h1[1] == h2[1] for h1, h2 in zip(deck1.cards, deck2.cards)])


def test_deck_class():
    deck = HearthstoneDeck.parse_deck("AAEBAc2xAgRxngG/CKLTAg27AqsEtATmBJYF7AXBwQKYxAKP0wL77AKV/wK5/wKjhwMA")

    assert deck.get_hero_class() == CardClass.MAGE

    deck.heroes = [1686]

    assert deck.get_hero_class() == CardClass.INVALID


def test_get_real_cards():
    deck = HearthstoneDeck.parse_deck("AAECAaIHCLICyAPNA68E1AXlB+f6AtKZAwu0Ae0CywPuBogH3QiGCe/xAtWMA4+XA4mbAwA=")
    id_list = deck.get_dbf_id_list()
    real_cards = list(deck.get_real_cards())

    for i in range(len(real_cards)):
        print(real_cards[i])
        print(deck.cards[i])
        assert real_cards[i][0].dbf_id == id_list[i][0]
        assert real_cards[i][1] == id_list[i][1]


def test_get_cards_in_display_order():
    deck = HearthstoneDeck.parse_deck("AAECAaIHCLICyAPNA68E1AXlB+f6AtKZAwu0Ae0CywPuBogH3QiGCe/xAtWMA4+XA4mbAwA=")
    deck_list = [
        ("Backstab", 2),
        ("Preparation", 2),
        ("Shadowstep", 2),
        ("Bloodsail Corsair", 1),
        ("Deadly Poison", 2),
        ("Southsea Deckhand", 1),
        ("Eviscerate", 2),
        ("Sap", 1),
        ("Edwin VanCleef", 1),
        ("EVIL Miscreant", 2),
        ("SI:7 Agent", 2),
        ("Dread Corsair", 2),
        ("Lifedrinker", 2),
        ("Raiding Party", 2),
        ("Waggle Pick", 2),
        ("Captain Greenskin", 1),
        ("Leeroy Jenkins", 1),
        ("Myra's Unstable Element", 1),
        ("Chef Nomi", 1),
    ]
    real_cards = list(deck.get_cards_in_deck_order())

    for i in range(len(real_cards)):
        print(real_cards[i][0].name)
        print(deck_list[i][0])
        # TODO: Fix this later
        # assert real_cards[i][0].name == deck_list[i][0]
        # assert real_cards[i][1] == deck_list[i][1]
