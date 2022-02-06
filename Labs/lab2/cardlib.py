""" Dat 171, Computer Assignment 2, written by John Carlsson and Derin Ismail, spring of 2022 """

from abc import ABCMeta, abstractmethod
import enum

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
        return self.suit
    
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


class Hand(): 
    def __init__(self) -> None:
        
        pass

    """ Add a card to hand """
    def add(self):
        pass
    
    """ Drop one or several cards """
    def drop(self, index):
        pass
    
    """ Sort the hand from smallest to largest ??"""
    def sort(self):
        pass
    """ Compute the best possible hand with your current cards """
    def best_poker_hand(self):
        pass


class StandardDeck():
    """ Create a standard deck of 52 cards """
    def __init__(self):
        pass

    """ Shuffle the deck """
    def shuffle(self):
        pass
    """ Draw a number of cards from the top of the deck"""
    def draw(self, number):
        pass


class PokerHand:
    """ A class for the different kind of pokerhands there are, there are methods for checking if a hand has a kind of hand """
    def __init__(self):
        pass
