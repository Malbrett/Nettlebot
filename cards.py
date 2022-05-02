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
unoCards = ('Red', 'Green', 'Blue', 'Yellow')
unoSpecialCards = ('Reverse', 'Draw Two', 'Skip Turn', 'Wild', 'Draw Four')

# TODO:
#  Give cards emoji representations
#  Implement into bot


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

    def __init__(self, suit, name, tarot=False, uno=False):
        self.suit = str(suit)
        self.name = str(name)
        self.tarot = tarot
        self.uno = uno
        self.value = self.get_value()

    def __str__(self):
        if self.suit == "Major":
            return self.name
        else:
            return f"{self.name} of {self.suit}"


class Deck:
    def __init__(self, tarot=False, hand=False, uno=False):
        self.tarot = tarot
        self.hand = hand
        self.uno = uno
        self.stack = []
        if self.hand:
            return
        elif self.tarot:
            for suit in tarotSuits:
                for name in tarotNames:
                    self.stack.append(Card(suit, name, tarot=True))
            for name in arcana:
                self.stack.append(Card("Major", name, tarot=True))
        elif self.uno:                                                  # Does not work
            for color in unoCards:
                for num in range(0, 10):
                    self.stack.append(Card(color, num, uno=True))
                for special in unoSpecialCards:
                    self.stack.append(Card(color, special, uno=True))
        else:
            for suit in suits:
                for name in names:
                    self.stack.append(Card(suit, name))

    def shuffle(self):
        random.shuffle(self.stack)

    def draw(self, pos=0, card=None):
        if card:
            self.stack.pop(self.stack.index(card))  # doesn't work yet
        else:
            return self.stack.pop(pos)

    def insert(self, card, pos=0, bottom=False):
        if bottom:
            self.stack.append(card)
        else:
            self.stack.insert(pos, card)
