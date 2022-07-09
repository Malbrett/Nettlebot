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
unoColors = ('Red', 'Green', 'Blue', 'Yellow')
unoSpecials = ('Skip', 'Reverse', 'Draw')

# TODO:
#  Give cards emoji representations
#  Implement into bot


class Card:
    def get_value(self):
        if self.tarot:
            if self.suit == "Major":
                return arcana.index(self.name)
            else:
                return min(tarotNames.index(self.name) + 1, 10)
        if self.uno:
            return
        return min(names.index(self.name) + 1, 10)

    def __init__(self, suit, name, hidden=False, tarot=False, uno=False):
        self.suit = str(suit)
        self.name = str(name)
        self.hidden = hidden
        self.tarot = tarot
        self.uno = uno
        self.value = self.get_value()

    def __str__(self):
        if self.suit == "Major":
            return self.name
        if self.uno:
            return f'{self.suit} {self.name}'
        return f'{self.name} of {self.suit}'


class Deck:
    def __init__(self, hand=False, tarot=False, uno=False):
        self.hand = hand
        self.tarot = tarot
        self.uno = uno
        self.stack = []

        if self.hand:
            return
        if self.tarot:
            for suit in tarotSuits:
                for name in tarotNames:
                    self.stack.append(Card(suit, name, tarot=True))
            for name in arcana:
                self.stack.append(Card("Major", name, tarot=True))
            return
        if self.uno:  # Does not work
            for color in unoColors:
                for num in range(1, 10):
                    self.stack.append(Card(color, num, uno=True))
                    self.stack.append(Card(color, num, uno=True))
                for special in unoSpecials:
                    self.stack.append(Card(color, special, uno=True))
                    self.stack.append(Card(color, special, uno=True))
            for num in range(0, 4):
                self.stack.append(Card('Wild', '', uno=True))
                self.stack.append(Card('Wild', 'Draw', uno=True))
            return

        for suit in suits:
            for name in names:
                self.stack.append(Card(suit, name))
        return

    def list(self, hidden=True):
        contents = ""
        for card in self.stack:
            if card.hidden and hidden:
                contents += f"*Hidden card,* "
            contents += f"{card}, "
        return contents

    def shuffle(self):
        random.shuffle(self.stack)

    def draw(self, pos=0, hidden=False):
        dealt = self.stack.pop(pos)
        if hidden:
            dealt.hidden = True
        return dealt

    def insert(self, card, pos=0, bottom=False):
        if bottom:
            self.stack.append(card)
        else:
            self.stack.insert(pos, card)
