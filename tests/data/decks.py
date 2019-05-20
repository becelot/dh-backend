from dh_backend.models import DeckVersion, Deck

TokenDruid = "AAECAZICAtfvAtaZAw5A/QL3A+YFxAaY+wLf+wL2/QKJgAOMgAO0kQPDlAPOlAPKnAMA"
TokenDruidMalfurion = "AAECAbSKAwLX7wLWmQMOQP0C9wPmBcQGmPsC3/sC9v0CiYADjIADtJEDw5QDzpQDypwDAA=="
TokenDruid2 = "AAECAZICAtfvAtaZAw5A/QL3A+YFxAaY+wLf+wKJgAOMgAO0kQPDlAPOlAPKnAPTnAMA"
SilencePriest = "AAECAa0GBPIF64gDgpQDyJ0DDe0B+ALdBOUEpQnRCtIK8gzy8QKDlAOHlQOumwOCnQMA"
MurlocShaman = "AAECAaoIArWYA5ybAw6/AcUD2wP+A+MF0AenCJMJ8PMC3oID4okDjJQDxpkD9JkDAA=="
EvenWarlock = "AAEBAf0GBooB+wegzgLCzgKX0wLN9AIM8gX7BooHtgfhB40I58sC8dAC/dACiNIC2OUC6uYCAA=="
SummonMage = "AAECAf0ECMUE+wyggAOvhwPnlQODlgOWmgOKngMLTYoBuwLJA6sEywSWBewHw/gCn5sDoJsDAA=="
SummonMage2 = "AAECAf0EBsUE+wyggAPnlQOWmgOKngMMTYoBuwKrBMsElgXhB+wHw/gCg5YDn5sDoJsDAA=="
SecretMage = "AAEBAf0EBsABqwS/CKO2AsbBAqLTAgxxuwKVA+YElgXsBde2Auu6Aoe9AsHBApjEAo/TAgA="
SecretPaladin = "AAECAZ8FAq8ElJoDDkaMAZ4ByAT1Bc8GrwexCK3yAtj+AvWJA76YA46aA5CaAwA="
PirateRogue = "AAECAaIHBrICyAPdCM6MA9aMA9uMAwy0AZsFqAXUBYgH5weGCabvAt/vAqr/As+JA5CXAwA="


def new_deck():
    return Deck()


def new_deck_version(deck):
    return DeckVersion(deck_name="TestDeck", deck_code="==saf", deck=deck)
