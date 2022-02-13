""" Dat 171, Computer Assignment 2, written by John Carlsson and Derin Ismail, spring of 2022 """

from abc import ABCMeta, abstractmethod
import enum
from random import shuffle
from unittest import suite
import numpy as np


class PlayingCard(metaclass=ABCMeta):
    """ Abstract base class for the playing cards
    param value: suit
    """
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
    """ A class for the different kind of suits in a deck of cards"""
    Hearts = 0
    Spades = 1
    Clubs = 2
    Diamonds = 3

class NumberedCard(PlayingCard):
    """ A class for the numbered playingcards in a deck of cards"""
    
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
    """ A class for the aces in deck of cards"""

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
    """ A class for the kings in a deck of cards """
    def __init__(self, suit):
        super().__init__(suit)
    
    def __str__(self):
        return f"King of {self.get_suit().name}, with the value {self.get_value()}"

    def get_value(self):
        return 13
    
    def get_suit(self):
        return self.suit

class QueenCard(PlayingCard):
    """ A class for the queens in a deck of cards """

    def __init__(self, suit):
        super().__init__(suit)
    
    def __str__(self):
        return f"Queen of {self.get_suit().name}, with the value {self.get_value()}"

    def get_value(self):
        return 12
    
    def get_suit(self):
        return self.suit

class JackCard(PlayingCard):
    """ A class for the jacks in a deck of cards """

    def __init__(self, suit):
        super().__init__(suit)
    
    def __str__(self):
        return f"Jack of {self.get_suit().name}, with the value {self.get_value()}"

    def get_value(self):
        return 11
    
    def get_suit(self):
        return self.suit

class Hand: 
    """ A players hand containing in this instance of texas hold em, 2 cards """

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


def royal_flush(cards = []):

    
    values = [(x.get_value(), x.get_suit()) for x in cards] 

    cardvalues = [x.get_value() for x in cards]
    if not 14 in cardvalues: return 0,0

    c = sorted(cards, reverse=True) # Starting point (high card)
    # Check if we have the value - k in the set of cards:
    found_straight = True
    for k in range(1,5):
        if (c[0].get_value() - k, c[0].get_suit()) not in values:
            found_straight = False
    if found_straight:
        return HandType.royal_flush.value, sorted(cardvalues,reverse=True)
    return 0,0
    

def straight_flush(cards = []):
    """
    Checks for the best straight flush in a list of cards (may be more than just 5)
    :param cards: A list of playing cards.
    :return: None if no straight flush is found, else the value of the top card.
    """
    
    values = [(x.get_value(), x.get_suit()) for x in cards] \
        +[(1, x.suit) for x in cards if x.get_value() == 14] # Add the aces value 1!

    cardvalues = [x.get_value() for x in cards]

    for c in reversed(sorted(cards)): # Starting point (high card)
        # Check if we have the value - k in the set of cards:
        found_straight = True
        for k in range(1,5):
            if (c.get_value() - k, c.get_suit()) not in values:
                found_straight = False

        if found_straight:
            return HandType.straight_flush.value, sorted(cardvalues,reverse=True)
        return 0,0

def four_of_a_kind(cards = []):
    counts = []
    values = [x.get_value() for x in cards]
    if 14 in values:
        values.append(1)
    for v in values:
        counts.append(values.count(v))
    if 4 in counts: return HandType.four_of_a_kind.value, sorted(values,reverse=True)
    return 0,0

def full_house(cards = []):
    counts = []
    values = [x.get_value() for x in cards]
    for v in values:
        counts.append(values.count(v))
    if (3 in counts) and (2 in counts): return HandType.full_house.value, sorted(values,reverse=True)
    return 0,0

def flush(cards = []):
    suits = [x.get_suit() for x in cards]
    values = set(x.get_value() for x in cards)
    counts = []
    for s in suits:
        counts.append(suits.count(s))
    if 5 in counts: return HandType.flush.value, sorted(values,reverse=True)
    return 0,0
   

def straight(cards = []):
    values = set(x.get_value() for x in cards) # sort an take out duplicates to check if you can make a straight
    values = list(values)
    if 14 in values: # If you have an ace you need to add the value 1
        values.append(1)
    values.sort()
    
    check_straight = 1
    for i in range(len(values)-1):
        if not values[i]-values[i+1] == -1:
            check_straight = 1
            continue
        check_straight += 1
        if check_straight == 5: return HandType.straight.value, sorted(values,reverse=True)
    
    return 0,0
    
    


def three_of_a_kind(cards = []):
    counts = []
    values = [x.get_value() for x in cards]
    if 14 in values:
        values.append(1)
    for v in values:
        counts.append(values.count(v))

    if 3 in counts: return HandType.three_of_a_kind.value, sorted(values,reverse=True)
    return 0,0

def two_pairs(cards = []):
    pair_list = set()
    values = [x.get_value() for x in cards]
    if 14 in values:
        values.append(1)
    for i,v in enumerate(values):
        for n in range(i+1,len(values)):
            if v == values[n]:
                pair_list.add(v)
    
    if len(pair_list) == 2: return HandType.two_pairs.value, sorted(values,reverse=True)
    return 0,0

def pair(cards = []):
    pair_list = set()
    values = [x.get_value() for x in cards]
    if 14 in values: # if you have an ace you need to add the value 1
        values.append(1)
    for i,v in enumerate(values):
        for n in range(i+1,len(values)):
            if v == values[n]:
                pair_list.add(v)
    
    if pair_list: return HandType.pair.value, sorted(values,reverse=True)
    return 0,0
    

def high_card(cards = []):
    values = [x.get_value() for x in cards]
    return HandType.high_Card.value, set(values)

class PokerHand:
    """ A pokerhand of 5 cards """
    
    def __init__(self, cards = []):
        """ Create a bunch of pokerhands and return the best one, each pokerhand function should be able to handle any amount cards 
        param value: cards
        type value: list och Playingcards
        
        """
        self.poker_hands = [] # a list of tuples with the value of the hand and the ighest card value
        self.bh = None # Best hand
        self.card = None # Best card in the best hand
        self.hand = None # Just a name for the hand
        # A list of the functions for checking various pokerhands
        hands = [royal_flush, straight_flush, four_of_a_kind, full_house, flush, straight, three_of_a_kind, two_pairs, pair, high_card]
        list_of_hands = ['Royal Flush', 'Straight Flush', 'Four of a kind', 'Full House', 'Flush', 'Straight', 'Three of a kind', 'Two Pairs', 'Pair', 'High Card']
        list_of_hands.reverse() # reverse since i didn't write it in the correct order :))))
        self.list_of_hands = list_of_hands

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
        return f"Your best pokerhand is a {self.list_of_hands[max(self.poker_hands)[0]]}!"
        

    def __lt__(self, other):
        if self.poker_hands < other.poker_hands: return True
        return False
                


if __name__ == '__main__':

    texas = StandardDeck()
    texas.shuffle()
    
    p1 = Hand()
    p1.add_card(AceCard(Suit.Diamonds))
    p1.add_card(NumberedCard(10,Suit.Diamonds))
    p1.add_card(JackCard(Suit.Diamonds))
    p1.add_card(JackCard(Suit.Hearts))
    p1.add_card(JackCard(Suit.Spades))
    p1.add_card(JackCard(Suit.Clubs))
    p1.add_card(QueenCard(Suit.Diamonds))
    p1.add_card(QueenCard(Suit.Spades))
    p1.add_card(KingCard(Suit.Diamonds))
    p1.add_card(NumberedCard(8,Suit.Diamonds))

    #print(type(p1.cards[0]))
    f = PokerHand(p1.cards)
    print(f)
    