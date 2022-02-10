""" Dat 171, Computer Assignment 2, written by John Carlsson and Derin Ismail, spring of 2022 """

from abc import ABCMeta, abstractmethod
from audioop import reverse
import enum
from random import shuffle
from cv2 import sort
import numpy as np


class PlayingCard(metaclass=ABCMeta):
    """ Abstract base class for the playing cards"""
    def __init__(self,suit):
        self.suit = suit

    """ Overloading  the equal operator"""
    def __eq__(self, other):
        if (self.get_value(),self.get_suit()) == (other.get_value(),other.get_suit()): return True
        else: return False
        
    """ Overloading  the less than operator"""
    def __lt__(self, other):
        if self.get_value() < other.get_value(): return True
        else: return False

    @abstractmethod
    def __str__(self):
        pass

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
    
    def __str__(self):
        return f"{self.get_value()} of {self.get_suit().name}"

    def get_value(self):
        return self.value
    
    def get_suit(self):
        return self.suit
    
class AceCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
    
    def __str__(self):
        return f"Ace of {self.get_suit().name}, with values {self.get_value()} or 1"

    def get_value(self):
        " Fixa så att det kan va 1 eller 14"
        return 14
    
    def get_suit(self):
        return self.suit

class KingCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
    
    def __str__(self):
        return f"King of {self.get_suit().name}, with the value {self.get_value()}"

    def get_value(self):
        return 13
    
    def get_suit(self):
        return self.suit

class QueenCard(PlayingCard):
    def __init__(self, suit):
        super().__init__(suit)
    
    def __str__(self):
        return f"Queen of {self.get_suit().name}, with the value {self.get_value()}"

    def get_value(self):
        return 12
    
    def get_suit(self):
        return self.suit

class JackCard(PlayingCard):

    def __init__(self, suit):
        super().__init__(suit)
    
    def __str__(self):
        return f"Jack of {self.get_suit().name}, with the value {self.get_value()}"

    def get_value(self):
        return 11
    
    def get_suit(self):
        return self.suit

class Hand: 
    """ A players hand containing 2 cards """
    def __init__(self):
        self.cards = []    

    def __str__(self):
        return f"A hand with the cards {self.cards[0]} and {self.cards[1]}"

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
        return PokerHand(cards)

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
        
class HandType(enum.IntEnum):
    """ A class for the different type of pokerhands """
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

def check_diff(cards = []):
    for i in range(0,len(cards)-1):
        if not np.diff((cards[i].get_value(),cards[i+1].get_value())) == 1: return False
    return True

def check_suit(cards = []):
    for i in range(0,len(cards)-1):
        if not cards[i].get_suit() == cards[i+1].get_suit(): return False
    return True



# The functions for checking if a hand can be created, if a hand can be created, return the best scenario for that hand.
def royal_flush(cards = []):
    pass
    # cards.sort(key = lambda x: x.get_value())
    # if cards[-1].get_value() == 14:
    #     if check_diff(cards):
    #         if check_suit(cards):
    #             return HandType.royal_flush.value, cards[-1]
    return 0,0

def straight_flush(cards = []):
    # cards.sort(key = lambda x: x.get_value())
    # if check_diff(cards):
    #     if check_suit(cards):
    #         return HandType.straight_flush.value, cards[-1].get_value()
    pass
    return 0,0

def four_of_a_kind(cards = []):
    return 0,0

def full_house(cards = []):
    return 0,0

def flush(cards = []):
    return 0,0

def straight(cards = []):
    # return HandType.straight
    return 0,0

def three_of_a_kind(cards = []):
    return 0,0

def two_pairs(cards = []):

    return 0,0

def pair(cards = []):
    pair_list = set()
    values = [x.get_value() for x in cards]
    for i,v in enumerate(values):
        for n in range(i+1,len(values)):
            if v == values[n]:
                pair_list.add[v]
    
    if pair_list: return HandType.pair.value, sorted(values,reverse=True)
    else: return [1,sorted(values,reverse=True)]
    

def high_card(cards = []):
    values = [x.get_value() for x in cards]
    return HandType.high_Card.value, set(values)

    

class PokerHand:
    
    def __init__(self, cards = []):
        """ Create a bunch of pokerhands and return the best one, each pokerhand function should be able to handle any amount cards """
        self.poker_hands = [] # a list of tuples with the value of the hand and the ighest card value
        self.bh = None # Best hand
        self.card = None # Best card in the best hand
        self.hand = None # Just a name for the hand
        # A list of the functions for checking various pokerhands
        hands = [royal_flush, straight_flush, four_of_a_kind, full_house, flush, straight, three_of_a_kind, two_pairs, pair, high_card]
        list_of_hands = ['Royal Flush', 'Straight Flush', 'Four of a kind', 'Full House', 'Flush', 'Straight', 'Three of a kind', 'Two Pairs', 'Pair', 'High Card']
        list_of_hands.reverse() # reverse since i didn't write it in the correct order :))))

        # This loop takes out all possible pokerhands able to be constructed with any number of given cards
        for hand in hands:
            hand_value, card_values = hand(cards) # returns hand value and a set of the values for the cards in the hand
            self.poker_hands.append((hand_value,card_values)) # The values for possible pokerhands
            
       
    """ att göra här:
    en funktion som rangordnar och sorterar ut vem som vinner
    self.best_hand = den bästa handen som en sträng från listan
    self.card = högsta värdet på kortet i handen. Inte nödvändigt tror jag
    
    
    
    """
        
                
            
    def __str__(self):
        return f"A {'g'} with {self.card} as the highest value card!"
        

    def __lt__(self, other):
        if self.bh < other.bh: return True
        return False
                


if __name__ == '__main__':

    texas = StandardDeck()
    texas.shuffle()
    
    p1 = Hand()
    p1.add_card(AceCard(Suit.Diamonds))
    p1.add_card(NumberedCard(10,Suit.Diamonds))
    p1.add_card(JackCard(Suit.Diamonds))
    p1.add_card(QueenCard(Suit.Diamonds))
    p1.add_card(KingCard(Suit.Diamonds))

    #print(type(p1.cards[0]))
    f = PokerHand(p1.cards)
    print(f)
    