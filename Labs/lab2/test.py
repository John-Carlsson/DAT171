
from abc import ABCMeta, abstractmethod
from cmath import log10
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
        return self.value
    
    def get_suit(self):
        return self.suit
    

class StandardDeck:
    """ Create a standard deck of 52 cards """
    def __init__(self):
        self.deck = []
        for suit in Suit:
            for i in range(2,11):
                self.deck.append(NumberedCard(i,suit))
            self.deck.append
       

    """ Shuffle the deck """
    def shuffle(self):
        pass
    """ Draw a number of cards from the top of the deck"""

    def draw(self, number):
        pass

li = [(3,(2,1)), (3,(3,2))]
l1 = [2,1]
l2 = [2,1,0]
m = max(li)
print(l1<l2)