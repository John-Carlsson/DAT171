from PyQt5.QtCore import *
from cardlib import *
import sys


class Player(QObject):
    indicator = pyqtSignal()
    card = pyqtSignal()

    def __init__(self, player_name):
        super().__init__()
        self.player_name = player_name
        self.credit = 0
        self.cash = 0
        self.hand = Hand

    def bet(self, tot_bet):
        self.cash = self.cash - tot_bet
        self.indicator.emit()

    def fold(self,tot_pot):
        self.money = self.money + tot_pot
        self.indicator.emit()


    def call(self,tot_call):
        self.money = self.money - tot_call
        self.indicator.emit()


class TexasHoldEm(QObject):
    pot = pyqtSignal()
    add_card = pyqtSignal()

    def __init__(self, players):
        super().__init__()
        self.current_bet = 0
        self.deck = None
        self.round = 0

        self.last_bet = 0
        self.table_cards = 0
        self.table = Table()

        # FOLD
        self.player_active = 0
        self.players = players
        #self.new_round()
        #self.next_player()

        # CALL
        #self.previous_pot=0
        self.following_pot=0
        self.number=0

        # BET
        self.total_bet = 0
        self.previous_pot = 0
        self.pot = 0
        self.next_pot = 0
        self.bet_load = 0

        self.table = Table()
        self.amount_hand = list()
        self.card_deck=[]


    def call(self):
        tot_call = self.following_pot - self.pot_before
        self.pot = self.pot + tot_call
        self.potemit()
        self.players[self.player_active].call(tot_call)
        self.player_active = (self.player_active + 1) % 2
        self.add_card.emit()
        self.number = 1 + self.number
        if self.number == 4:
            self.winner()

    def winner(self):
        pot = self.pot
        result = 0
        amount=self.amount_hand
        length=len(amount)
        if length == 5:

            one=Table().hand.best_poker_hand(self.players[0].card_deck)
            two = Table().hand.best_poker_hand(self.players[1].card_deck)

            if one > two:
                result = self.players[0]
            else:
                result = self.players[1]

        result.money = pot+ result.money

        result.indicator.emit()
        self.new_round()

    def new_round(self):
        self.deck = StandardDeck()
        self.deck.shuffle()

        self.add_card.emit()
        self.round = self.round+ 1

        self.pot = 0
        #self.pot.emit()
        for p in self.players:
            p.hand = Hand()
            d=self.deck.draw()

            p.hand.cards = list()
            p.hand.cards.append(d)
            p.hand.cards.append(d)
            p.player_card_signal.emit()

        self.table_cards = 0
        self.player_active = (self.round + 1) % 2
        self.last_bet = -1

    #####Done med fold
    def fold(self):
        player_winning = (self.player_active + 1) % 2
        self.players[player_winning].bet(self.pot)
        self.new_round()
        #self.next_player()


    #####Done with bet
    def bet(self):
        total_amount = self.bet_load
        self.total_bet = self.total_bet + total_amount
        self.previous_pot = self.pot
        self.pot = self.pot + total_amount
        self.pot.emit()
        self.next_pot = self.pot
        self.players[self.player_active].bet(total_amount)
        self.player_active = (self.player_active + 1) % 2





class Table():
    def __init__(self):
        hand_cards = Hand()
        self.hand = hand_cards




