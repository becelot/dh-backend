from hearthstone import cardxml
from hearthstone.deckstrings import Deck

from dh_backend import create_app

deck = Deck.from_deckstring("AAECAf0ECsUE7QWQB+wHvwj7DKCAA6aHA8CYA4qeAwpNigG7AskDqwTLBJYF4Qe+7AKDlgMA")
deckId = deck.get_dbf_id_list()
dbf_db, _ = cardxml.load_dbf()

print(deck.heroes[0])
print(dbf_db[deck.heroes[0]].card_class)
print(dbf_db[deckId[0][0]].card_id)

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
