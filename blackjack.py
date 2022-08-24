import cards


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = cards.Deck(True)
        self.score = 0
        self.stand = False
        self.bust = False

    def show_hand(self):
        print(f"{self.name}'s hand: {self.hand.list()}")
        print(f"Total: {self.hand.list(val=True)}")


def main():
    players = []
    player_count = 0
    passed = 0
    deck = cards.Deck()
    deck.shuffle()

    while True:
        user = input(f"Player {player_count+1} name: ")
        if user:
            players.append(Player(user))
            player_count += 1
            continue
        if player_count == 0:
            print(f"You need at least one player to start")
            continue
        if player_count == 1:
            players.append(Player("Jerry"))
            player_count += 1
        break
    print('---')
    for player in players:
        player.hand.insert(deck.draw(hidden=True))
        player.hand.insert(deck.draw())
        player.show_hand()

    while True:
        passed = 0
        for player in players:
            if player.stand or player.bust:
                passed += 1
            print(f"{player.name}'s turn:")
            while True:
                move = input("> ")
                if move == "hit":
                    player.hand.insert(deck.draw())
                    player.show_hand()
                    if player.hand.list(val=True) > 21:
                        player.bust = True
                        player.score = 0
                        print(f"{player.name} has bust!")
                        passed += 1
                        continue
                if move == "stand":
                    player.stand = True
                    player.score = player.hand.list(val=True)
                    print(f"{player.name} stood")
                    passed += 1
                    continue
                print(f"Invalid move")
        if passed == player_count:
            break

    winner = players[0]
    for player in players:
        if player.score > winner.score:
            winner = player
    print(f"{winner.name} wins!!")
    exit()


if __name__ == '__main__':
    main()
