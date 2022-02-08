""" Dat 171, Computer Assignment 2, written by John Carlsson and Derin Ismail, spring of 2022 """

from abc import ABCMeta, abstractmethod
import enum
from math import fabs
from multiprocessing.sharedctypes import Value
from random import shuffle
import numpy as np


class PlayingCard(metaclass=ABCMeta):
    """ Abstract base class for the playing cards"""
    def __init__(self,suit):
        self.suit = suit

    """ Overloading  the equal operator"""
    def __eq__(self, other):
        if (self.get_suit(),self.get_value()) == (other.get_suit(),other.get_value()): return True
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
    Hearts = 0
    Spades = 1
    Clubs = 2
    Diamonds = 3

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
        return 14
    
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
        index.sort()
        n = 0
        for i in index:
            i -= n
            del self.cards[i]
            n += 1
    
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
        return self.deck.pop()
        
    
def check_diff(cards = []):
    for i in range(0,len(cards)-1):
        if not np.diff((cards[i].get_value(),cards[i+1].get_value())) == 1: return False
    return True

def check_suit(cards = []):
    for i in range(0,len(cards)-1):
        if not cards[i].get_suit() == cards[i+1].get_suit(): return False
    return True



def royal_flush(cards = []):
    cards.sort(key = lambda x: x.get_value())
    print(cards[-1].get_value())
    if cards[-1].get_value() == 14:
        if check_diff(cards):
            if check_suit(cards):
                return HandType.royal_flush
    return False

def straight_flush(cards = []):
    cards.sort(key = lambda x: x.get_value())
    if check_diff(cards):
        if check_suit(cards):
            return HandType.straight_flush
    return False

def four_of_a_kind(cards = []):
    return False

def full_house(cards = []):
    return False

def flush(cards = []):
    return False

def straight(cards = []):
    return HandType.straight
    return False

def three_of_a_kind(cards = []):
    return False

def two_pairs(cards = []):
    return False

def pair(cards = []):
    return False

def high_card(cards = []):
    return HandType.high_Card

class HandType(enum.IntEnum):
    """ Ranking of hands in falling order """
    royal_flush = 9
    straight_flush = 8
    four_of_a_kind = 7
    full_house = 6
    flush = 5
    straight = 4
    three_of_a_kind = 3
    two_pairs = 2
    pair = 1 
    high_Card = 0

class PokerHand():

    def __init__(self, cards = []):
        hands = [royal_flush, straight_flush, four_of_a_kind, full_house, flush, straight, three_of_a_kind, two_pairs, pair, high_card]
        """ Check if the hand can create a pokerhand starting from the top """
        self.hand = False

        """ Lös så att cards bara är fem kort men att alla möjligheter för de 7 olika kortmöjligheterna testas"""
        for hand in hands:
            self.hand = hand(cards)
            if self.hand: break


    def __lt__(self, other):
        if self.value < other.value: return True
        else: return False
        
       
if __name__ == '__main__':

    texas = StandardDeck()
    texas.shuffle()
    
    p1 = Hand()
    p1.add_card(AceCard(Suit.Diamonds))
    p1.add_card(NumberedCard(10,Suit.Diamonds))
    p1.add_card(JackCard(Suit.Diamonds))
    p1.add_card(QueenCard(Suit.Diamonds))
    p1.add_card(KingCard(Suit.Diamonds))

    print(type(p1.cards[0]))
    had = PokerHand(p1.cards)
    print(had.hand)
    