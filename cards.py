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

# TODO: Give cards emoji representations
#       Implement into bot


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
            return [11, 1]
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
        self.hand = kwargs.get("HAND", False)
        self.stack = []
        if self.hand:
            return
        elif self.tarot:
            for suit in tarotSuits:
                for name in tarotNames:
                    self.stack.append(Card(suit, name, TAROT=True))
            for name in arcana:
                self.stack.append(Card("Major", name, TAROT=True))
        else:
            for suit in suits:
                for name in names:
                    self.stack.append(Card(suit, name))

    def shuffle(self):
        random.shuffle(self.stack)

    def draw(self, pos=0, **kwargs):
        card_name = kwargs.get("CARD", None)
        if card_name:
            self.stack.pop(self.stack.index(card_name))  # doesn't work yet
        else:
            return self.stack.pop(pos)

    def insert(self, card, **kwargs):
        if kwargs.get("BOTTOM", False):
            self.stack.append(card)
        else:
            pos = kwargs.get("POS", 0)
            self.stack.insert(pos, card)
