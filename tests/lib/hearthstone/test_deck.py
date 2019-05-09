from typing import List, Tuple

from hearthstone.enums import FormatType

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
