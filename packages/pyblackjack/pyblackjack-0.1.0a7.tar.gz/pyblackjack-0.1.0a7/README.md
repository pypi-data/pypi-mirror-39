# pyblackjack

**pyblackjack** is a fun way to waste time at the terminal playing
blackjack with a computerized dealer.

## Installation

`pip install pyblackjack`

## Getting Started

Type `blackjack` at the terminal to launch the game. At the first
prompt, you may press `q` to jump straight into the action, using a
default player name, six-deck shoe, and 1,000 starting chips, with the
dealer hitting on soft 17.

You can also configure the game to your liking by going through the
prompts. The first prompt asks you for the number of players (human; CPU
players may come in the future but are not available yet). You can
select from one to six players, and enter a name for each. Next, you
will be asked for the number of starting chips per player, followed by
the number of decks in the shoe (up to eight). The last prompt will ask
you if the dealer should hit on a soft 17 (which increases the house
edge slightly). After this, you're ready to start playing!

## Playing

Your first task for every hand is to enter your bet. After all players
have placed a bet, the cards will be dealt and displayed. At this point,
if the dealer is showing an Ace, each player will be asked whether they
wish to buy insurance, the cost of which is one-half of your bet.

After this, or if the dealer is not showing an Ace, blackjacks will be
checked. If the dealer has a blackjack, it will be revealed, the hand
ends immediately, and all players lose unless they also have blackjack,
in which case it is a push. If anyone bought insurance, they will lose
their bet but be paid 2:1 on the insurance.

If the dealer does not have blackjack, but a player does, that player is
paid at 3:2 and takes no further part in the hand.

After this, if any active players remain, the first player in turn order
will be shown their hand and asked for an action. Available actions are
listed below. Except for hit and stand, all actions are only available
as your first action before doing anything else, and then sometimes only
under certain circumstances as noted.

* Hit (`h`): Deal another card to your hand. If this results in a hard
  total over 21, the game will display a message that you busted, and
  your turn will end and you will lose your bet.

* Stand (`s`): End your turn.

* Double down (`d`): Double your bet, deal one (and only one) additional
  card to the hand, and end your turn. This option is only available
  when your first two cards total 9, 10, or 11.

* Split (`p`): Split your two starting cards into two separate hands,
  placing a second bet identical to your original bet on the second
  hand. This is only available if both starting cards form a pair (e.g.
  two sixes or two queens). A second card will then be dealt to each
  hand, which will be played separately from the other. After splitting,
  the only actions available on the split hands will be to hit or stand,
  except that if you split a pair of aces, your turn will end
  immediately after the second card is dealt to each hand (i.e. you
  cannot hit split aces).

* Surrender (`u`): Give up and drop out of the hand, with half your bet
  being returned.

Once the first player has completed their turn, the next player will be
asked for actions, and so on until all players have played. At this
point, the dealer will reveal the downcard and play their hand. The
dealer will hit on 16 or below and stand on 17 or higher, except that if
the option for the dealer to hit on soft 17 was enabled in setup (or the
quickstart option was chosen), the dealer will do so.

Once the dealer has played their hand, the dealer pays the winners. If
the dealer busts, all players who did not also bust are paid 1:1. If the
dealer did not bust, players with a higher total than the dealer are
paid 1:1, players with the same total push (receive their bet back), and
players with a lower total lose their bet.

The game will then return to the prompt to enter a bet. At this prompt,
any player wishing to quit may enter `q` to do so and will be removed
from the game. If the last player in the game quits, the program will
terminate.
