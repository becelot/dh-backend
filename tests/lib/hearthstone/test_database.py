import pytest

from dh_backend.lib.hearthstone.database import HearthstoneDatabase, HSNoSuchCardException


@pytest.mark.first
def test_database():
    with pytest.raises(HSNoSuchCardException):
        card = HearthstoneDatabase[1]

    with pytest.raises(HSNoSuchCardException):
        card = HearthstoneDatabase[1]

    card = HearthstoneDatabase[637]

    assert card.name == "Jaina Proudmoore"
