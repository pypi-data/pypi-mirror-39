import random


class Card(int):
    '''An individual playing card. Subclass of int for simplicity.'''

    def __new__(cls, rank, value):
        self = super().__new__(cls, value)
        self.rank = rank
        return self

    def __str__(self):
        return (str(self.rank))


CARDSET = [
    Card('A', 1),
    Card('2', 2),
    Card('3', 3),
    Card('4', 4),
    Card('5', 5),
    Card('6', 6),
    Card('7', 7),
    Card('8', 8),
    Card('9', 9),
    Card('10', 10),
    Card('J', 10),
    Card('Q', 10),
    Card('K', 10),
]

DECK = CARDSET * 4


class Shoe:
    def __init__(self, decks=6):
        self.numdecks = decks
        self.new()

    def deal(self):
        return self.cards.pop()

    def time_to_shuffle(self):
        return len(self.cards) <= self.cut

    def new(self):
        self.cards = DECK * self.numdecks
        random.shuffle(self.cards)
        if self.numdecks == 1:
            self.cut = len(self.cards) / 2
        else:
            self.cut = len(self.cards) / 4


class Hand:
    def __init__(self, shoe):
        self.cards = []
        self.shoe = shoe

    def hard_total(self):
        return sum(self.cards)

    def soft_total(self):
        total = self.hard_total()
        if total > 11 or 1 not in self.cards:
            return None
        return total + 10

    def total(self):
        return self.soft_total() or self.hard_total()

    def print_hand(self, downcard=False):
        cards = self.cards[:]
        if downcard:
            cards[0] = '[]'
        cardtext = ' '.join(str(card) for card in cards)
        if downcard:
            return cardtext
        else:
            return '{} ({})'.format(cardtext, self.total())

    def check_blackjack(self):
        return len(self.cards) == 2 and self.total() == 21

    def check_bust(self):
        return self.hard_total() > 21

    def hit(self):
        self.cards.append(self.shoe.deal())

    def reset(self):
        self.cards = []


class Dealer(Hand):
    def __init__(self, shoe, hit_soft_17=True):
        super().__init__(shoe)
        self.hard_stand = 17
        if hit_soft_17:
            self.soft_stand = 18
        else:
            self.soft_stand = 17

    def check_insurance(self):
        return self.cards[1] == 1

    def play_hand(self):
        while True:
            if ((self.soft_total() and self.soft_total() >= self.soft_stand)
                    or self.hard_total() >= self.hard_stand):
                break
            self.hit()


class Player(Hand):
    _id = 0

    def __init__(self, shoe, name=None, chips=1000):
        super().__init__(shoe)
        self.__class__._id += 1
        self.id = self.__class__._id
        if name is None:
            self.name = 'Player {}'.format(self.id)
        else:
            self.name = name
        self.chips = chips
        self.bet = 0
        self.split_hand = None
        self.insurance = False

    def check_bet(self):
        return self.chips >= self.bet

    def check_split(self):
        return (len(self.cards) == 2
                and self.cards[0].rank == self.cards[1].rank)

    def split(self):
        self.chips -= self.bet
        self.split_hand = Hand(self.shoe)
        self.split_hand.cards.append(self.cards.pop())
        self.hit()

    def check_double(self):
        return len(self.cards) == 2 and 9 <= self.total() <= 11

    def double_down(self):
        self.chips -= self.bet
        self.bet *= 2
        self.hit()

    def surrender(self):
        self.chips += self.bet // 2

    def buy_insurance(self):
        price = self.bet // 2
        self.chips -= price
        self.insurance = price

    def reset(self):
        super().reset()
        if self.split_hand:
            self.split_hand = None
