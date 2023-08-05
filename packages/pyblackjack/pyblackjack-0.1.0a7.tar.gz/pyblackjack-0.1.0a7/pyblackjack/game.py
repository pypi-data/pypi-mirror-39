import sys

from . import console
from .objects import Shoe, Dealer, Player


ACTION_HIT = '[H]it'
ACTION_STAND = '[S]tand'
ACTION_SPLIT = 'S[p]lit'
ACTION_DOUBLE = '[D]ouble down'
ACTION_SURRENDER = 'S[u]rrender'


class Game:
    def __init__(self, players=[None], chips=1000, decks=6, hit_soft_17=True):
        self.shoe = Shoe(decks)
        self.dealer = Dealer(self.shoe, hit_soft_17=hit_soft_17)
        self.players = []
        for name in players:
            self.players.append(Player(self.shoe, name=name, chips=chips))
        self.all_hands = self.players + [self.dealer]
        self.active_players = []

    def mainloop(self):
        while self.play_hand():
            print('=' * 10)
            if self.shoe.time_to_shuffle():
                self.shoe.new()
                print('New shoe in play!')
                print('=' * 10)

    def play_hand(self):
        self.active_players = []
        self.collect_bets()
        if not self.players:
            return False
        self.deal_cards()
        print('Dealer: {}'.format(self.dealer.print_hand(downcard=True)))
        for player in self.active_players:
            print('{}: {}'.format(player.name, player.print_hand()))
        print('-' * 10)
        if self.check_dealer_blackjack():
            return True
        self.check_player_blackjacks()
        for player in self.active_players.copy():
            self.play_player_hand(player)
        if self.active_players:
            print('-' * 10)
            self.dealer.play_hand()
            print('Dealer: {}'.format(self.dealer.print_hand()))
            self.pay_winners()
        return True

    def collect_bets(self):
        for player in self.players.copy():
            self.get_bet(player)

    def get_bet(self, player: Player):
        if player.chips == 0:
            print('{} is out of chips and is eliminated.'.format(player.name))
            self.players.remove(player)
            return
        print('{} has {} chips.'.format(player.name, player.chips))
        bet = console.get_int('Enter a bet, or [q]uit: ', 0, player.chips, 'q')
        if bet == 'q':
            self.players.remove(player)
            return
        player.bet = bet
        player.chips -= bet
        self.active_players.append(player)

    def deal_cards(self):
        for hand in self.all_hands:
            hand.reset()
        for _ in range(2):
            for hand in self.all_hands:
                hand.hit()

    def check_dealer_blackjack(self):
        if self.dealer.check_insurance():
            for player in self.active_players:
                insure = console.get_yes_no(
                    '{}: Buy insurance?'.format(player.name)
                )
                if insure:
                    player.buy_insurance()
        if self.dealer.check_blackjack():
            self.resolve_dealer_blackjack()
            return True
        for player in self.active_players:
            if player.insurance:
                player.insurance = False
        return False

    def resolve_dealer_blackjack(self):
        print('Dealer has blackjack!')
        for player in self.active_players:
            if player.insurance:
                player.chips += player.insurance * 3
                player.insurance = False
            if player.check_blackjack():
                print('{} has blackjack!'.format(player.name))
                player.chips += player.bet
        self.active_players.clear()

    def check_player_blackjacks(self):
        for player in self.active_players.copy():
            if player.check_blackjack():
                print('{} has blackjack!'.format(player.name))
                player.chips += int(player.bet * 2.5)
                self.active_players.remove(player)

    def play_player_hand(self, player: Player):
        self.play_single_hand(player)
        if player.split_hand:
            self.play_single_hand(player, split=True)

    def play_single_hand(self, player: Player, split=False):
        if split:
            hand = player.split_hand
            hand.hit()
        else:
            hand = player
        while not hand.check_bust():
            name = self.get_name(player, split)
            print('{}: {}'.format(name, hand.print_hand()))
            if player.split_hand and player.cards[0] == 1:
                break
            if hand.total() == 21:
                break
            action = self.get_action(player, hand)
            if not self.perform_action(action, hand, name):
                break
        else:
            print('{}: {}'.format(name, hand.print_hand()))
            print('{} busted!'.format(name))
            if (split and player.check_bust()) or not player.split_hand:
                self.active_players.remove(player)

    def get_name(self, player, split):
        if split:
            return '{} (hand 2)'.format(player.name)
        elif player.split_hand:
            return '{} (hand 1)'.format(player.name)
        else:
            return player.name

    def get_action(self, player, hand):
        actionlist = [ACTION_HIT, ACTION_STAND]
        actioncheck = 'hs'
        lowchipscheck = ''
        if len(hand.cards) == 2 and not player.split_hand:
            if hand.check_split():
                if player.check_bet():
                    actionlist.append(ACTION_SPLIT)
                    actioncheck += 'p'
                else:
                    lowchipscheck += 'p'
            if hand.check_double():
                if player.check_bet():
                    actionlist.append(ACTION_DOUBLE)
                    actioncheck += 'd'
                else:
                    lowchipscheck += 'd'
            actionlist.append(ACTION_SURRENDER)
            actioncheck += 'u'
        actions = ', '.join(actionlist)
        return console.get_action(actions + '? ', actioncheck, lowchipscheck)

    def perform_action(self, action, hand, name):
        if action == 'h':
            hand.hit()
            return True
        elif action == 's':
            return False
        elif action == 'p':
            hand.split()
            return True
        elif action == 'd':
            hand.double_down()
            print('{}: {}'.format(name, hand.print_hand()))
            return False
        elif action == 'u':
            hand.surrender()
            self.active_players.remove(hand)  # hand == player
            return False

    def pay_winners(self):
        for player in self.active_players:
            self.resolve_hand(player, player)
            if player.split_hand:
                self.resolve_hand(player, player.split_hand)

    def resolve_hand(self, player, hand):
        if hand is player:
            msg = ''
        else:
            msg = ' on the split hand'
        if hand.check_bust():
            return
        elif (self.dealer.check_bust() or
                hand.total() > self.dealer.total()):
            player.chips += player.bet * 2
            print('{} wins{}!'.format(player.name, msg))
        elif hand.total() == self.dealer.total():
            player.chips += player.bet
            print('{} pushes{}.'.format(player.name, msg))
        else:
            print('{} loses{}.'.format(player.name, msg))


def setup():
    numplayers = console.get_int(
        'Enter number of players [1-6] or [q]uickstart: ', 1, 6, "q"
    )
    if numplayers == 'q':
        return Game()

    players = []
    for n in range(numplayers):
        name = console.get_str('Enter name for player {}: '.format(n))
        players.append(name)

    chips = console.get_int('Enter starting chips: ', min=0)

    decks = console.get_int('Enter number of decks in the shoe: ', 1, 8)

    hit_soft_17 = console.get_yes_no('Should dealer hit on soft 17?')

    return Game(players, chips, decks, hit_soft_17)


def main():
    print('Welcome to PyBlackjack!')
    game = setup()
    game.mainloop()
    print('Thanks for playing!')
    return 0


if __name__ == '__main__':
    sys.exit(main())
