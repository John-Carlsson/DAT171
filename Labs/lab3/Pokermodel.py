from PyQt5.QtCore import *
from cardlib import *


class Money(QObject):
    """ A class for handling all kinds of money, on the table, such as the pot, last bet made
    All signals regarding money will be here
    
    """
    total_pot_signal = pyqtSignal()
    current_bet_signal = pyqtSignal()

    def __init__(self, players=[]):
        super().__init__()
        self.pot = 0
        self.last_bet_placed = 0
        self.current_bet = 0
        self.call = 0
        self.player_bets = dict()
        if players:
            for player in players:
                self.player_bets[
                    player] = 0  # A dict for the players(key) and the bets they have placed this turn as values

    def reset(self):
        for key in self.player_bets.keys():
            self.player_bets[key] = 0

        self.current_bet = 0
        self.last_bet_placed = 0
        self.call = 0

    def clear_pot(self):
        self.current_bet = 0
        self.current_bet_signal.emit()

    def change_current_bet(self, amount):
        self.current_bet = amount
        self.current_bet_signal.emit()

    def update_pot(self, amount):
        self.pot += amount
        self.total_pot_signal.emit()

    def update_fold(self):
        self.pot = self.pot - self.pot
        self.total_pot_signal.emit()

        self.current_bet = 0
        self.current_bet_signal.emit()

    def players_pot(self):
        self.total_pot_signal.emit()


class PlayerModel(QObject, Hand):
    """Everything thats going on regarding a player
    Args:
        :QObject: A QObject
        :Hand: A Hand object
    """
    card_signal = pyqtSignal()
    cash_signal = pyqtSignal()

    def __init__(self, name, cash=100):
        super().__init__()
        self.hand = Hand()
        self.cash = cash
        self.name = name
        self.played = False
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.card_signal.emit()

    def add_card(self, card):
        super().add_card(card)
        self.card_signal.emit()

    def reset(self):
        super().drop_cards([x for x in range(len(self.cards))])  # drop all cards
        self.card_signal.emit()

    def place_bet(self, amount):
        self.cash -= amount
        self.cash_signal.emit()

    def players_cash(self):
        self.cash_signal.emit()


class TexasHoldEm(QObject):
    def __init__(self, names):
        super().__init__()
        self.players = [PlayerModel(name) for name in names]
        self.money = Money(self.players)
        self.table = TableModel()
        self.deck = StandardDeck()
        self.deck.shuffle()

        for player in self.players:
            player.cash = 100
            for i in range(2):
                player.add_card(self.deck.draw())
        for i in range(3):
            self.table.add_card(self.deck.draw())

        self.active_player = self.players[0]
        self.not_active_player = self.players[1]
        self.not_active_player.flip()

    def bet(self, amount):
        """ Place a bet with the Qspin thingy in the widget
        Args:
            :amount: An int chosen in the widget with the Qspin thingy
        """
        self.money.player_bets[self.active_player] += amount
        self.active_player.place_bet(amount)
        self.money.change_current_bet(amount)
        self.money.update_pot(amount)

    def fold(self):
        """ Fold and surrender to your opponents
        """
        self.not_active_player.cash = self.not_active_player.cash + self.money.pot
        self.not_active_player.players_cash()
        self.money.update_fold()
        self.money.clear_pot()

        self.new_round()

    def call(self):
        amount = self.money.player_bets[self.not_active_player] - self.money.player_bets[self.active_player]
        self.bet(amount)

    def end_turn(self):
        """ Switching players or see if someone wins
        """
        self.active_player.played = True

        # Check to see if both players have betted the same amount
        if self.money.player_bets[self.active_player] == self.money.player_bets[self.not_active_player] and (
                len(self.table.cards) < 5) and \
                (self.active_player.played == True and self.not_active_player.played == True):
            self.table.add_card(self.deck.draw())
            self.active_player.played = False
            self.not_active_player.played = False
            self.swap_player()

        # If all cards are on table and both players have bet the same amount, check the winner
        elif self.money.player_bets[self.active_player] == self.money.player_bets[self.not_active_player] and (
                len(self.table.cards) == 5) and \
                (self.active_player.played == True and self.not_active_player.played == True):
            self.check_winner()

            return

        elif self.money.player_bets[self.active_player] >= self.money.player_bets[self.not_active_player]:
            self.swap_player()

        elif self.money.player_bets[self.active_player] < self.money.player_bets[self.not_active_player]:
            return

    def new_round(self):
        """ A method for resetting the game for a new round
        """
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.table.reset()
        self.money.reset()
        self.active_player.played = False
        self.not_active_player.played = False
        for player in self.players:
            player.reset()

        # All players draw 2 cards
        for player in self.players:
            for i in range(2):
                player.add_card(self.deck.draw())

        # The table gets 3 cards
        for i in range(3):
            self.table.add_card(self.deck.draw())

    def swap_player(self):
        self.active_player.flip()
        self.not_active_player.flip()
        if self.active_player == self.players[0]:
            self.active_player = self.players[1]
            self.not_active_player = self.players[0]
        else:
            self.active_player = self.players[0]
            self.not_active_player = self.players[1]



    def check_winner(self):
        cards = self.table.cards

        # Give money if the round was equal
        if self.active_player.best_poker_hand(cards) == self.not_active_player.best_poker_hand(cards):
            self.not_active_player.cash += self.money.pot / 2
            self.not_active_player.players_cash()
            self.active_player.cash += self.money.pot / 2
            self.active_player.players_cash()

        # If one of the player wins
        elif self.active_player.best_poker_hand(cards) < self.not_active_player.best_poker_hand(cards):
            self.not_active_player.cash += self.money.pot
            self.not_active_player.players_cash()
            self.money.pot -= self.money.pot
            self.money.players_pot()
            self.money.current_bet = 0
            self.money.clear_pot()
            print(self.active_player.name + ' wins' + ' with a ' + str(self.active_player.best_poker_hand(cards)))

        # If the other player wins
        else:
            self.active_player.cash += self.money.pot
            self.active_player.players_cash()
            self.money.pot -= self.money.pot
            self.money.players_pot()


            self.money.current_bet = 0
            self.money.clear_pot()
            print(
                self.not_active_player.name + ' wins' + ' with a ' + str(self.not_active_player.best_poker_hand(cards)))

        self.new_round()


class TableModel(PlayerModel, Money):
    """ A class for the Table, working like a hand. containing cards. Able to drop all cards or adding cards
    """
    cards_signal = pyqtSignal()

    def __init__(self, players=[]):
        super().__init__(players)

    def add_card(self, card):
        super().add_card(card)
        self.cards_signal.emit()

    def reset(self):
        if self.cards:
            super().drop_cards([x for x in range(len(self.cards))])
            self.cards_signal.emit()