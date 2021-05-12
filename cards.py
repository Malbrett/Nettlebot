import random

suits = ("hearts", "spades", "diamonds", "clubs")
names = ("ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king")


class Card:
    def __init__(self, suit, name, value):
        self.suit = str(suit).capitalize()
        self.name = str(name).capitalize()
        self.value = int(value)


class Deck:
    def __init__(self, **kwargs):
        self.tarot = kwargs.get("TAROT", False)
        self.ext = kwargs.get("EXT", False)
        self.stack = []
        total_cards = 0
        for suit in suits:
            for val in range(14, 1):
                self.stack[total_cards] = Card(suit, names[val],
                                               lambda x: [1, 11] if val == 1 else (10 if val >= 10 else val))
                total_cards += 1
