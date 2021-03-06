""" Dat 171, Computer Assignment 2, written by John Carlsson and Derin Ismail, spring of 2022 """

from abc import ABCMeta, abstractmethod
import enum
from random import shuffle

from pandas import value_counts


class PlayingCard(metaclass=ABCMeta):
    """
    A class for the playingcards in a standard deck of 52 cards

    Args:
        :metaclass:  Defaults to ABCMeta.
    """
    def __init__(self,suit):
        self.suit = suit

    """ Overloading  the equal operator"""
    def __eq__(self, other):
        return (self.get_value(),self.get_suit()) == (other.get_value(),other.get_suit())
        
    """ Overloading  the less than operator"""
    def __lt__(self, other):
        return (self.get_value(),self.get_suit()) < (other.get_value(),other.get_suit())
        

    @abstractmethod
    def __str__(self):
        """ Overloading the str operator. Returns a nice text of the card """
        

    @abstractmethod
    def get_value(self):
        """ Return the cards value """
        
    @abstractmethod
    def get_suit(self):
        """ Returns the suit of the card """

class Suit(enum.IntEnum):
    """
    A class for the suits in a deck of cards 

    Args:
        :enum: To make it possible to iterate and value the suits
    """
    Hearts = 0
    Spades = 1
    Clubs = 2
    Diamonds = 3

class NumberedCard(PlayingCard):
    
    """ A class for the numbered playingcards in a deck of cards, value can be between 2 and 10 """
    
    def __init__(self, value, suit):
        """Args:    
        :suit: A Suit type object for one of the suits in the deck
        """
        super().__init__(suit)
        if value>10 or value<2: return 'Min value is 2 and max value is 10'
        self.value = value
    
    def __str__(self):
        return f"{self.get_value()} of {self.get_suit().name}"

    def get_value(self):
        return self.value
    
    def get_suit(self):
        return self.suit
    

class AceCard(PlayingCard):
    """ A class for the aces in deck of cards, value is set at 14, since Aces are normaly seen as the most valuable card. """

    def __init__(self, suit):
        """Args:    
        :suit: A Suit type object for one of the suits in the deck
        """
        super().__init__(suit)
    
    def __str__(self):
        return f"Ace of {self.get_suit().name}, with values {self.get_value()} or 1"

    def get_value(self):
        return 14 # Value is set at 14, since its the most common use of the ace. The value
    
    def get_suit(self):
        return self.suit

class KingCard(PlayingCard):
    """ A class for the kings in a deck of cards """
    def __init__(self, suit):
        """Args:    
        :suit: A Suit type object for one of the suits in the deck
        """
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
        """Args:    
        :suit: A Suit type object for one of the suits in the deck
        """
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
        """

        Args:
            :suit: A Suit type object for one of the suits in the deck
        """
        super().__init__(suit)
    
    def __str__(self):
        return f"Jack of {self.get_suit().name}, with the value {self.get_value()}"

    def get_value(self):
        return 11
    
    def get_suit(self):
        return self.suit

class Hand: 
    """ A players hand containing any number of cards"""

    def __init__(self):
        """ Create a hand """
        self.cards = []    

    def __str__(self):
        return "A hand with the cards: " + ', '.join([str(x) for x in self.cards])

    
    def add_card(self, card):
        """ Add cards to hand """
        self.cards.append(card)
        
    
    def drop_cards(self, index) -> list:
        """ Drop one or several cards by index """
        index = list(set(index)) # remove any duplicates from the list
        if max(index) >= len(self.cards): return 'Too few cards in hand'
        
        index.sort(reverse=True)
       
        for i in index:
            
            del self.cards[i]
    
    def sort(self):
        """ Sort the hand from smallest to largest"""
        self.cards.sort()

   
    def best_poker_hand(self, cards = []):
        """ Compute the best possible hand with your current cards 

        Args:
            :cards: A list of cards. Defaults to an empty list: [].

        Returns:
            :PokerHand: A pokerhand object of the best hand
        """
        return PokerHand(self.cards + cards)

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
       

    
    def shuffle(self):
        """ Shuffle the deck """
        shuffle(self.deck)
    
    
    def draw(self):
        """ Draw the top card from the deck"""
        if len(self.deck) == 0: return 'inga kort kvar'
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

    def __str__(self) -> str:
        return self.name.replace('_', ' ')


# Here are functions for checking if a certain hand can be created
def royal_flush(cards):    
    """A function for checking if a Royal flush can be created with the cards given

    Args:
        :param cards: A list of PlayingCard objects

    Returns:
        :HandType:, :list: a HandType object and a list of cards
    """
    

    values = [(x.get_value(), x.get_suit()) for x in cards] 
    cardvalues = [x.get_value() for x in cards]
    if not 14 in cardvalues: return

    c = sorted(cards, reverse=True) # Starting point (high card)
    # Check if we have the value - k in the set of cards:
    found_straight = True
    for k in range(1,5):
        if (c[0].get_value() - k, c[0].get_suit()) not in values:
            found_straight = False
    if found_straight:
        return HandType.royal_flush, sorted(cards,reverse=True)
    
def straight_flush(cards):
    """
    Checks for the best straight flush in a list of cards (may be more than just 5)
    :param cards: A list of playing cards.
    :return: None if no straight flush is found, else the value of the top card and the cards in hand
    """
    
    values = [(x.get_value(), x.get_suit()) for x in cards] \
        +[(1, x.suit) for x in cards if x.get_value() == 14] # Add the aces value 1!
    for c in reversed(sorted(cards)): # Starting point (high card)
        # Check if we have the value - k in the set of cards:
        found_straight = True
        for k in range(1,5):
            if (c.get_value() - k, c.get_suit()) not in values:
                found_straight = False

        if found_straight:
            return HandType.straight_flush, sorted(cards,reverse=True)

def four_of_a_kind(cards):
    """ 
    A function checking if a four of kind can be made with the given cards

    Args:
    :cards: A list of PlayingCard objects
    Returns:
    :tuple: A Handtype for the pokerhand and a a tuple of the card thats a four of a kind and a
    list of all the cards in the hand in falling order
    """
    counts = dict()
    values = [x.get_value() for x in cards]
    for v in values:
        counts[values.count(v)] = v
    if 4 in counts.keys(): return HandType.four_of_a_kind, (counts[4], sorted(cards,reverse=True))

def full_house(cards):
    """ 
    A function checking if a full house can be made with the given cards

    Args:
    :cards: A list of PlayingCard objects

    Returns:
    :tuple: A Handtype for the pokerhand and a a tuple of the cards that make up the full house and a
    list of all the cards in the hand in falling order
    """
    counts = dict()
    values = [x.get_value() for x in cards]
    for v in values:
        counts[values.count(v)] = v
        # Fixa s?? att trissens v??rde v??gs in
    if (3 in counts.keys()) and (2 in counts.keys()): 
        three = counts[3]
        two = counts[2]
        return HandType.full_house, ((three,two), sorted(cards,reverse=True))

def flush(cards):
    """ A function checking if a flush can be made with the given cards
    Args:
    :cards: A list of PlayingCard objects

    Returns:
    :tuple: A Handtype for the pokerhand and a
    list of the cards making up the flush in falling order
    """
    card_list = [x.get_suit() for x in cards]
    
    counts = dict()
    for s in Suit:
        counts[s] = card_list.count(s)

    maxi = max(counts.values())
    value_list = list(counts.values())
    pos = value_list.index(maxi)
    key_list = list(counts.keys())
    if maxi >= 5: return HandType.flush, sorted([x for x in cards if x.get_suit() == key_list[pos]],reverse=True)
   
def straight(cards):
    """ A function checking if a straight can be made with the given cards
    Args:
    :cards: A list of PlayingCard objects

    Returns:
    :tuple: A Handtype for the pokerhand and a
    list of all the cards in the hand in falling order
    """
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
        if check_straight == 5: return HandType.straight, sorted(cards,reverse=True)
    
def three_of_a_kind(cards):
    """ A function checking if three of a kind can be made with the given cards
    Args:
    :cards: A list of PlayingCard objects

    Returns:
    :tuple: A Handtype for the pokerhand and a a tuple of the value fpr the three of a kind and a
    list of all the cards in the hand in falling order
    """
    counts = dict()
    values = [x.get_value() for x in cards]
    for v in values:
        counts[values.count(v)] = v
    if 3 in counts.keys(): return HandType.three_of_a_kind, (counts[3],sorted(cards,reverse=True))

def two_pairs(cards):
    """ A function checking if two pairs can be made with the given cards
    Args
    :cards: A list of PlayingCard objects
    Return:
    :tuple: A Handtype for the pokerhand and a tuple of the value of the pairs and a
    list of all the cards in the hand in falling order
    """
    pair_list = set()
    values = [x.get_value() for x in cards]
    if 14 in values:
        values.append(1)
    for i,v in enumerate(values):
        for n in range(i+1,len(values)):
            if v == values[n]:
                pair_list.add(v)
    
    if len(pair_list) == 2: return HandType.two_pairs, (sorted(pair_list,reverse=True),sorted(cards,reverse=True))

def pair(cards):
    """ A function checking if a pair can be made with the given cards
    Args:
    :param cards: A list of PlayingCard objects
    Returns:
    :HandType:, :tuple: A Handtype for the pokerhand and a tuple of the value of the pair and a
    list of all the cards in the hand in falling order
    """
    counts = dict()
    values = [x.get_value() for x in cards]
    for v in values:
        counts[values.count(v)] = v
    if 2 in counts.keys(): return HandType.three_of_a_kind, (counts[2],sorted(cards,reverse=True))
    


    
    
def high_card(cards):
    """ A function checking if a pair can be made with the given cards
    Args:
    :cards: A list of PlayingCard objects
    Returns:
    :tuple: A Handtype for the pokerhand  and a
    list of all the cards in the hand in falling order
    """
    return HandType.high_Card, sorted(cards,reverse=True)

class PokerHand:
    
    def __init__(self, cards):
        """ Create a bunch of pokerhands, each pokerhand function should be able to handle any amount cards 

        param cards: A list of cards
        type value: list och Playingcards
        
        """
        # A list of the functions for checking various pokerhands, any amount of cards can be checked
        hands = [royal_flush, straight_flush, four_of_a_kind, full_house, flush, straight, three_of_a_kind, two_pairs, pair, high_card]
        # This loop takes out all possible pokerhands able to be constructed with any number of given cards
        for hand in hands:
            if hand(cards) is not None:
                self.best_hand, self.values = hand(cards)
                break

    def __str__(self):
        return f"Your best pokerhand is a {self.best_hand.name}!"

    def __lt__(self, other):
        return (self.best_hand, self.values) < (other.best_hand, other.values)

    def __eq__(self, other):
        return (self.best_hand, self.values) == (other.best_hand, other.values)


if __name__ == '__main__':

        texas = StandardDeck()
        texas.shuffle()

        p1 = Hand()
        p1.add_card(NumberedCard(2,Suit.Hearts))
        p1.add_card(NumberedCard(3,Suit.Hearts))
        p1.add_card(NumberedCard(4,Suit.Hearts))
        p1.add_card(NumberedCard(6,Suit.Hearts))
        p1.add_card(NumberedCard(7,Suit.Hearts))
        p1.add_card(NumberedCard(9,Suit.Hearts))
        print(p1.best_poker_hand())
        # 
        # p1 = Hand()
        # p2 = Hand()
        # table = Hand()
        # for i in range(2):
            # p1.add_card(texas.draw())
            # p2.add_card(texas.draw())
    
        # for i in range(5):  
            # table.add_card(texas.draw())
        # 
        # p1_best = p1.best_poker_hand(table.cards)
        # p2_best = p2.best_poker_hand(table.cards)

        # print(p1, '\n', p2, '\n', table)
        # if p2_best < p1_best:
            # print('Spelare 1 vinner')
        # elif p1_best < p2_best:
            # print('Spelare 2 vinner')
        # print(p1_best,'\n', p2_best)
        # print(p1_best < p2_best)
        # 
    
    