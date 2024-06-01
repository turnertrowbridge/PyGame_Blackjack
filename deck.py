import random


class Deck:
    def __init__(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8',
                 '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        nicknames = ['2', '3', '4', '5', '6', '7', '8',
                     '9', '10', 'J', 'Q', 'K', 'A']
        return [(rank, suit, nickname) for suit, nickname in zip(suits, nicknames) for rank in ranks]

    def deal_card(self):
        return self.deck.pop()
