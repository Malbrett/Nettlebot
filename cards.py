import random

suits = ("hearts", "spades", "diamonds", "clubs")
names = ("ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king")


class Card:
    def __init__(self, suit, name, value):
        self.suit = str(suit).capitalize()
        self.name = str(name).capitalize()
        self.value = int(value)

    def __str__(self):
        return f"{self.name} of {self.suit}"


class Deck:
    def __init__(self, **kwargs):
        # self.tarot = kwargs.get("TAROT", False)
        # self.ext = kwargs.get("EXT", False)
        self.stack = []
        for suit in suits:
            for val in range(14, 1):
                if val > 10:
                    self.stack.append(Card(suit, names[val-1], 10))
                else:
                    self.stack.append(Card(suit, names[val-1], val))
