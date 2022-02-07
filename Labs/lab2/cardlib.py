""" Dat 171, Computer Assignment 2, written by John Carlsson and Derin Ismail, spring of 2022 """

from abc import ABCMeta, abstractmethod
import enum
from ftplib import parse150
from random import shuffle

class PlayingCard(metaclass=ABCMeta):
    """ Abstract base class for the playing cards"""
    def __init__(self,suit) -> None:
        self.suit = suit

    """ Overloading  the equal operator"""
    def __eq__(self, other):
        if self.get_value() == other.get_value(): return True
        else: return False
        
    """ Overloading  the less than operator"""
    def __lt__(self, other):
        if self.get_value() < other.get_value(): return True
        else: return False



    @abstractmethod
    def get_value(self):
        pass
        
    @abstractmethod
    def get_suit(self):
        pass


class Suit(enum.IntEnum):
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3

class NumberedCard(PlayingCard):
    
    def __init__(self, value, suit):
        super().__init__(suit)
        self.value = value
    
    def get_value(self):
        return self.value
    
    def get_suit(self):
        return self.suit
    
class AceCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
    
    def get_value(self):
        " Fixa så att det kan va 1 eller 14"
        return 1
    
    def get_suit(self):
        return self.suit

class KingCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
    
    def get_value(self):
        return 13
    
    def get_suit(self):
        return self.suit

class QueenCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
    
    def get_value(self):
        return 12
    
    def get_suit(self):
        return self.suit

class JackCard(PlayingCard):

    def __init__(self, suit):
        super().__init__(suit)
    
    def get_value(self):
        return 11
    
    def get_suit(self):
        return self.suit


class Hand: 
    def __init__(self):
        self.cards = []
        

    """ Add cards to hand """
    def add_card(self, card):
        self.cards.append(card)
        
    
    """ Drop one or several cards by index """
    def drop_cards(self, index):
        for i in index:
            del self.cards[i]
    
    """ Sort the hand from smallest to largest ?? """
    def sort(self):
        self.cards.sort()

    """ Compute the best possible hand with your current cards """
    def best_poker_hand(self, cards = []):
        pass

class StandardDeck:
    """ A standard deck of 52 cards """
    def __init__(self):
        self.deck = []
       
        for suit in Suit:
            self.deck.append(AceCard(suit))
            for i in range(2,11):
                self.deck.append(NumberedCard(i,suit))
            self.deck.append(JackCard(suit))
            self.deck.append(QueenCard(suit))
            self.deck.append(KingCard(suit))
       

    """ Shuffle the deck """
    def shuffle(self):
        shuffle(self.deck)
    
    """ Draw the top card from the deck"""
    def draw(self):
        drawn = self.deck[0]
        self.deck.remove(self.deck[0])

        return drawn
        

class PokerHand:
    """ A class for the different kind of pokerhands there are, there are methods for checking if a hand has a kind of hand """
    def __init__(self):
        pass


if __name__ == '__main__':

    texas = StandardDeck()
    texas.shuffle()
    
    p1 = Hand()
    