from PyQt5.QtCore import *
from cardlib import *
import sys

class PlayerModel(QObject, Hand):
    """Everything thats going to change within the game

    Args:

        :QObject: A QObject
        :Hand: A Hand object

    """
    cards = pyqtSignal()
    indicator = pyqtSignal()

    def __init__(self, name):
        self.hand = Hand()
        self.cash = 100
        self.name = name
        
        # Additional state needed by the UI
        self.flipped_cards = False
    def __iter__(self):
        return iter(self.cards)
        
    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.cards.emit()  # something changed, better emit the signal!


    def add_card(self, card):
        super().add_card(card)
        self.cards.emit()  # something changed, better emit the signal!

    
    def bet(self, tot_bet):
        """method for when placing a bet

        Args:
            tot_bet (Int): Amount betted
        """
        self.cash = self.cash - tot_bet
        self.indicator.emit()

    def call(self,tot_call):
        """For calling in the game

        Args:
            tot_call (Int): Amount of cash in the call
        """
        self.money = self.cash - tot_call
        self.indicator.emit()
        

class TexasHolEm(QObject):
    """ A class for the rules in Texas HoldEm poker

    Args:
        :QObject: A QObject
    """
    pot = pyqtSignal()
    add_card = pyqtSignal()
    def __init__(self):
        self.table = Hand()
        self.pot = 0
        self.players = ['Player1', 'Player2']
        self.deck = StandardDeck().shuffle()
    
    def the_flop(self):
        for i in range(0,3):
            self.table.add_card(self.deck.draw())

    





