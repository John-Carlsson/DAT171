from PyQt5.QtCore import *
from cardlib import *


class TableModel(Hand,QObject):
    """ A class for the Table, working like a hand. containging cards. Able to drop all cards or adding cards
    """
    cards = pyqtSignal()
    def __init__(self):
        super().__init__()
    
    def add_card(self, card):
        super().add_card(card)
        self.cards.emit()  # something changed, better emit the signal!
    
    def reset(self):
        super().drop_cards([x for x in range(len(self.cards))]) # drop all cards
        self.cards.emit()

    
class Money(QObject):
    """ A class for handling all kinds of money, on the table, such as the pot, last bet made
    """
    total_pot_signal = pyqtSignal()
    current_bet_signal = pyqtSignal()
    def __init__(self, players = []):
        self.pot = 0
        self.last_bet_placed = 0
        self.current_bet = 0
        self.call = 0
        self.player_bets = dict()
        if players:
            for player in players:
                self.player_bets[player] = 0 # A dict for the players(key) and the bets they have placed this turn as values



class PlayerModel(QObject, Hand):
    """Everything thats going to change within the game
    Args:

        :QObject: A QObject
        :Hand: A Hand object

    """
    card_signal = pyqtSignal()
    indicator = pyqtSignal()
    cash_signal = pyqtSignal() # Players cash

    def __init__(self, name, cash = 100):
        super().__init__()
        self.hand = Hand()
        self.cash = cash
        self.name = name
        
        # Additional state needed by the UI
        self.flipped_cards = False
    def __iter__(self):
        return iter(self.cards)
        
    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.card_signal.emit()  # something changed, better emit the signal!


    def add_card(self, card):
        super().add_card(card)
        self.card_signal.emit()  # something changed, better emit the signal!

    def reset(self):
        super().drop_cards([x for x in range(len(self.cards))]) # drop all cards
        self.card_signal.emit()



class TexasHoldEm(QObject):
    
    
    winner = pyqtSignal((str,))
    
    def __init__(self):
        super().__init__() # Don't forget super init when inheriting!
        self.players = [PlayerModel('John'), PlayerModel('Lucas')] # A list of PlayerModel objects
        self.money = Money() # keeping track of the money
        self.table = TableModel() # Keeping track of the table
        self.deck = StandardDeck()
        self.deck.shuffle()

        for player in self.players: # Give players money
            player.cash = 100
            for i in range(2):
                player.add_card(self.deck.draw())
        
        self.active_player = self.players[0]
        self.active_player.flip()
        self.not_active_player = self.players[1]

    

    def bet(self, amount): # INTE Klar, pallar inte fixa kolla minuskonto och shit
        """ Place a bet with the Qspin thingy in the widget

        Args:
            :amount: An int chosen in the widget with the Qspin thingy
        """
        self.self.active_player.cash = self.self.active_player - amount
        self.money.cash_signal.emit()
        self.money.current_bet =  amount
        self.money.current_bet_signal.emit()
        
        self.money.total_pot =  self.total_pot + amount
        self.money.total_pot_signal.emit()

    def fold(self):
        """ Fold and surrender to your opponents
        """
        if self.active_player == self.players[0]:
            self.players[1].cash = self.players[1].cash + self.total_pot
            self.players[1].cash_signal.emit()
        else: 
            self.players[0].cash = self.players[0].cash + self.total_pot
            self.players[0].cash_signal.emit()

        self.total_pot =  self.total_pot - self.total_pot
        self.total_pot_signal.emit()
        self.current_bet =  0
        self.current_bet_signal.emit()

        
        # Reset the game and prepare for next round
        self.new_round()
             
    def call(self):
        self.bet(self.money.player_bets[self.not_active_player] - self.money.player_bets[self.active_player])
            
    def end_turn(self):
        """ Choose to do nothing
        """
        self.active_player.flip()
        if self.active_player == self.players[0]: 
            self.active_player = self.players[1] 
            self.not_active_player = self.players[0]
        else: 
            self.active_player = self.players[0]
            self.not_active_player = self.players[1]
        
    def new_round(self):
        """ A method for resetting the game for a new round
        """
        self.table.reset()
        for player in self.players:
            player.reset()

        # All players draw 2 cards
        for player in self.players:
            for i in range(2):
                player.add_card(self.deck.draw())

        # The table gets 3 cards
        for i in range(3):
            self.table.add_card(self.deck.draw())





