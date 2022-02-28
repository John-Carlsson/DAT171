from PyQt5.QtCore import *
from cardlib import *


class TableModel(QObject,Hand):
    """ A class for the Table, working like a hand. containging cards. Able to drop all cards or adding cards
    """
    cards_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        
    
    def add_card(self, card):
        super().add_card(card)
        self.cards_signal.emit()  # something changed, better emit the signal!
    
    def reset(self):
        if self.cards:
            super().drop_cards([x for x in range(len(self.cards))]) # drop all cards
            self.cards_signal.emit()

    
class Money(QObject):
    """ A class for handling all kinds of money, on the table, such as the pot, last bet made
    """
    total_pot_signal = pyqtSignal()
    current_bet_signal = pyqtSignal()
    def __init__(self, players = []):
        super().__init__()
        self.pot = 0
        self.last_bet_placed = 0
        self.current_bet = 0
        self.call = 0
        self.player_bets = dict()
        if players:
            for player in players:
                self.player_bets[player] = 0 # A dict for the players(key) and the bets they have placed this turn as values

    def reset(self):
        for key in self.player_bets.keys():
            self.player_bets[key] = 0

        self.current_bet = 0
        self.last_bet_placed = 0
        self.call = 0





class PlayerModel(QObject, Hand):
    """Everything thats going on regarding a player
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
        self.players = [PlayerModel('John'), PlayerModel('Derin')] # A list of PlayerModel objects
        self.money = Money(self.players) # keeping track of the money
        self.table = TableModel() # Keeping track of the table
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.passed = False

        for player in self.players: # Give players money and cards
            player.cash = 100
            for i in range(2):
                player.add_card(self.deck.draw())
        for i in range(3):
            self.table.add_card(self.deck.draw())
        
        self.active_player = self.players[0]
        self.not_active_player = self.players[1]
        self.not_active_player.flip()
        

    

    def bet(self, amount): # INTE Klar, pallar inte fixa kolla minuskonto och shit
        """ Place a bet with the Qspin thingy in the widget

        Args:
            :amount: An int chosen in the widget with the Qspin thingy
        """
        self.money.player_bets[self.active_player] += amount
        self.active_player.cash = self.active_player.cash - amount
        self.active_player.cash_signal.emit()
        self.money.current_bet =  amount
        self.money.current_bet_signal.emit()
        
        self.money.pot =  self.money.pot + amount
        self.money.total_pot_signal.emit()

    def fold(self):
        """ Fold and surrender to your opponents
        """
        
        self.not_active_player.cash = self.not_active_player.cash + self.money.pot
        self.not_active_player.cash_signal.emit()

        self.money.pot =  self.money.pot - self.money.pot
        self.money.total_pot_signal.emit()
        self.money.current_bet =  0
        self.money.current_bet_signal.emit()

        
        # Reset the game and prepare for next round
        self.new_round()
             
    def call(self):
        self.bet(self.money.player_bets[self.not_active_player] - self.money.player_bets[self.active_player])
        

    def end_turn(self):
        """ Choose to do nothing
        """
        self.active_player.flip()
        self.not_active_player.flip()
        # check to see if both players have betted the same amount
        if self.money.player_bets[self.active_player] == self.money.player_bets[self.not_active_player] and (len(self.table.cards) < 5):
            self.table.add_card(self.deck.draw())
        
        # If all cards are on table and both players passed, check who won
        elif (self.passed == True) and (len(self.table.cards) == 5):
            self.check_winner()
            return

        if self.money.player_bets[self.active_player] >= self.money.player_bets[self.not_active_player]:
            if self.active_player == self.players[0]: 
                self.active_player = self.players[1] 
                self.not_active_player = self.players[0]
            else: 
                self.active_player = self.players[0]
                self.not_active_player = self.players[1]
        else: 
            self.active_player.flip()
            self.not_active_player.flip()
        self.passed = not self.passed
        
    def new_round(self):
        """ A method for resetting the game for a new round
        """
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.table.reset()  # Reset the deck
        self.money.reset()
        self.passed = False
        for player in self.players: # Drop all cards and hand out two new ones
            player.reset()

        # All players draw 2 cards
        for player in self.players:
            for i in range(2):
                player.add_card(self.deck.draw())

        # The table gets 3 cards
        for i in range(3):
            self.table.add_card(self.deck.draw())


    def check_winner(self):
        cards = self.table.cards
        if self.active_player.best_poker_hand(cards) < self.not_active_player.best_poker_hand(cards):
            print(self.active_player.name + ' wins' + ' with a ' + str(self.active_player.best_poker_hand(cards)))
        else: print(self.not_active_player.name + ' wins' + ' with a ' + str(self.not_active_player.best_poker_hand(cards)))
        self.new_round()





