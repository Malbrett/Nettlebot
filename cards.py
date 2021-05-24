import random

suits = ("Hearts", "Spades", "Diamonds", "Clubs")
tarotSuits = ("Swords", "Cups", "Wands", "Coins")
names = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King")
tarotNames = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten",
              "Page", "Knight", "Queen", "King")
arcana = ('The Fool', 'The Magician', 'The High Priestess', 'The Empress', 'The Emperor',
          'The Hierophant', 'The Lovers', 'The Chariot', 'Strength', 'The Hermit', 'Wheel of Fortune',
          'Justice', 'The Hanged Man', 'Death', 'Temperance', 'The Devil', 'The Tower', 'The Star',
          'The Moon', 'The Sun', 'Judgement', 'The World')


class Card:
    def get_value(self):
        if self.tarot:
            if self.suit == "Major":
                return arcana.index(self.name)
            else:
                index_val = tarotNames.index(self.name) + 1
        else:
            index_val = names.index(self.name) + 1

        if index_val == 1:
            return [1, 11]
        elif index_val > 10:
            return 10
        else:
            return index_val

    def __init__(self, suit, name, **kwargs):
        self.suit = str(suit)
        self.name = str(name)
        self.tarot = kwargs.get("TAROT", False)
        self.value = self.get_value()

    def __str__(self):
        if self.suit == "Major":
            return self.name
        else:
            return f"{self.name} of {self.suit}"


class Deck:
    def __init__(self, **kwargs):
        self.tarot = kwargs.get("TAROT", False)
        # self.ext = kwargs.get("EXT", False)
        self.stack = []
        if self.tarot:
            for suit in tarotSuits:
                for name in tarotNames:
                    self.stack.append(Card(suit, name, TAROT=True))
            for name in arcana:
                self.stack.append(Card("Major", name, TAROT=True))
        else:
            for suit in suits:
                for name in names:
                    self.stack.append(Card(suit, name))
