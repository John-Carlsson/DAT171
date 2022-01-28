import enum
import random
from abc import ABCMeta, abstractmethod
from collections import Counter


class PlayingCards(metaclass=ABCMeta):
    """ Class for the playing cards"""

    def __init__(self, suit):
        self.suit = suit

    def __str__(self):
        """ Returns Suit and Value in readable format """
        return "{}, {}".format(str(self.get_suit()), self.get_value())

    def __lt__(self, other):
        """ Executes lesser than operator of values"""
        if self.get_value() < other.get_value():
            return True
        else:
            return False

    def __eq__(self, other):
        """ Executes if cards are equal """
        return (self.get_suit(), self.get_value()) == (other.get_suit(), other.get_value())

    @abstractmethod
    def get_value(self):
        """Returns value of card"""
        pass

    @abstractmethod
    def get_suit(self):
        """Returns suit of card"""
        pass


class Suit(enum.IntEnum):
    """ Class that contains all four suits"""
    Diamonds = 0
    Hearts = 1
    Clubs = 2
    Spades = 3


class NumberedCard(PlayingCards):
    """A subclass to PlayingCards
        Returns class NumberedCard with values (2-10) and suits"""
    def __init__(self, value, suit):
        self.value = value
        super().__init__(suit)

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value


class JackCard(PlayingCards):
    """A subclass to PlayingCards
        Returns class JackCard with value (11) and suits"""
    def __init__(self, suit):
        super().__init__(suit)

    def get_suit(self):
        return self.suit

    def get_value(self):
        return 11


class QueenCard(PlayingCards):
    """A subclass to PlayingCards
        Returns class JackCard with value (12) and suits"""
    def __init__(self, suit):
        super().__init__(suit)

    def get_suit(self):
        return self.suit

    def get_value(self):
        return 12


class KingCard(PlayingCards):
    """A subclass to PlayingCards
        Returns class JackCard with value (13) and suits"""
    def __init__(self, suit):
        super().__init__(suit)

    def get_suit(self):
        return self.suit

    def get_value(self):
        return 13


class AceCard(PlayingCards):
    """A subclass to PlayingCards
        Returns class JackCard with value (14) and suits"""
    def __init__(self, suit):
        super().__init__(suit)

    def get_suit(self):
        return self.suit

    def get_value(self):
        return 14


class StandardDeck:
    """ Class StandardDeck that contains 52 card """
    
    """StandardDeck represents deck of 52 cards"""
    def __init__(self):
        self.cards = []
        self.construct()

    def __len__(self):
        """ Method for length of the list of cards """
        return len(self.cards)

    def construct(self):
        """Constructing the deck with loop"""
        for st in Suit:
            for vl in range(2, 11):
                self.cards.append(NumberedCard(vl, st))
            self.cards.append(JackCard(st))
            self.cards.append(QueenCard(st))
            self.cards.append(KingCard(st))
            self.cards.append(AceCard(st))

    def shuffle(self):
        """Shuffles the cards in the deck"""
        random.shuffle(self.cards)

    def draw(self):
        """Draws the the top card and eliminates it from deck"""
        top_card = self.cards.pop()
        return top_card


class HandType(enum.IntEnum):
    """The rankings of poker hands"""
    high_card = 0
    pair = 1
    two_pair = 2
    three_of_a_kind = 3
    straight = 4
    flush = 5
    full_house = 6
    four_of_a_kind = 7
    straight_flush = 8


class Hand:
    """Players hand represented as the class Hand """
    def __init__(self):
        self.cards = []

    def __len__(self):
        """ Method for length of the list of cards """
        return len(self.cards)

    def __getitem__(self, indices):
        """ Method for getting items in indices """
        return self.cards[indices]

    def add_card(self, card):
        """Method for adding cards to hand"""
        self.cards.append(card)

    def sort(self):
        """Method for sorting cards in hand"""
        self.cards.sort()

    def drop_cards(self, index):
        """Method for dropping cards from hand based on index list"""
        self.cards = [i for j, i in enumerate(self.cards) if j not in index]

    def best_poker_hand(self, cards=[]):
        """Method for determining the best poker hand of cards in the hand"""
        best_ph = PokerHand(cards + self.cards)
        return best_ph


class PokerHand:
    """ Class PokerHand that contains functions for determining the best poker hand """

    def __init__(self, cards):
        self.HandType = None
        self.value = None

        # Poker hand functions in the list possible_hands
        possible_hands = (check_straight_flush, check_four_of_a_kind, check_full_house, check_flush, check_straight, check_three_of_a_kind,
                          check_two_pairs, check_pair, check_high_card)

        # Looping through ranking of the hands
        for hand, hand_type in zip(possible_hands, reversed(HandType)):
            found_hand = hand(cards)
            if found_hand is not None:
                self.value = found_hand
                self.HandType = hand_type
                break

    def __lt__(self, other):
        """ Executes lesser than operator of values"""
        if self.HandType.value < other.HandType.value:
            return True

        elif self.HandType.value == other.HandType.value and self.value < other.value:
            return True
        else:
            return False


def check_high_card(cards):
    """ Method for finding the highest card in the list of cards
        : param cards: list of cards
        : return: value of highest card """

    values = [c.get_value() for c in cards]
    values.sort()

    return values[-1]


def check_pair(cards):
    """ Method for finding pair of cards in the list of cards
        : param cards: list of cards
        : return: card value of the pair """

    values = [c.get_value() for c in cards]
    values.sort()
    value_count = Counter()
    for c in cards:
        value_count[c.get_value()] += 1
    pairs = [value[0] for value in value_count.items() if value[1] == 2]
    if len(pairs) == 1:
        return pairs[0],values[-1]


def check_two_pairs(cards):
    """ Method for finding two pairs of cards in the list of cards
        : param cards: list of cards
        : return: tuple of card values of the pairs """

    value_counter = Counter()
    for c in cards:
        value_counter[c.get_value()] += 1
    twos_1 = [v[0] for v in value_counter.items() if v[1] >= 2]
    twos_1.sort()
    twos_2 = [v[0] for v in value_counter.items() if v[1] >= 2]
    twos_2.sort()
    for two_1 in reversed(twos_1):
        for two_2 in reversed(twos_2):
            if two_2 != two_1:
                return two_1, two_2

    """
    value_count = Counter()
    for c in cards:
        value_count[c.get_value()] += 1
    pairs = [value[0] for value in value_count.items() if value[1] == 2]
    if len(pairs) == 2:
        return pairs[0], (pairs[1])
    """

def check_three_of_a_kind(cards):
    """ Method for finding three of a kind of cards in the list of cards
        : param cards: list of cards
        : return: card value of three of a kind """

    value_counter = Counter()
    for c in cards:
        value_counter[c.get_value()] += 1
    all_three=list()
    for v in value_counter.items():
        if v[1] == 3:
            all_three.append(v[0])
            return all_three[0]

    length = len(all_three)
    if length == 1:
        return all_three[0]



def check_straight(cards):
    """ Method for finding straight of cards in the list of cards
        : param cards: list of cards
        : return: highest card value of the straight """

    cards.sort(reverse=True) # Reverse to find the highest straight (if several exist)
    values = [c.get_value() for c in cards]

    for c in cards:
        if c.get_value() == 14: #add ace as 1 in case of low straight with ace
            values.append(1)

    for c in cards:
        found_straight = True

        for k in range(1, 5):
            if (c.get_value() - k) not in values:
                found_straight = False
                break
        if found_straight:
            return c.get_value()


def check_flush(cards):
    """ Method for finding flush of cards in the list of cards
        : param cards: list of cards
        : return: suit of the flush """

    values = [c.get_value() for c in cards]
    values.sort()
    suit_counter = Counter()
    for c in cards:
        suit_counter[c.suit] += 1

    suits = [s[0] for s in suit_counter.items() if s[1] >= 5]

    length=len(suits)
    if length == 1:
        return values[-1]


def check_full_house(cards):
    """ Method for finding full house of cards in the list of cards
        : param cards: list of cards
        : return: tuple of values from the twos and threes """

    value_counter = Counter()
    for c in cards:
        value_counter[c.get_value()] += 1
    # Find the card ranks that have at least three of a kind
    threes = [v[0] for v in value_counter.items() if v[1] >= 3]
    threes.sort()
    # Find the card ranks that have at least a pair
    twos = [v[0] for v in value_counter.items() if v[1] >= 2]
    twos.sort()

    # Threes are dominant in full house, lets check that value first:
    for three in reversed(threes):
        for two in reversed(twos):
            if two != three:
                return three, two



def check_four_of_a_kind(cards):
    """ Method for finding four of a kind of cards in the list of cards
        : param cards: list of cards
        : return: value from the four of a kind """

    value_counter = Counter()
    for c in cards:
        value_counter[c.get_value()] += 1

    all_four = list()
    for v in value_counter.items():
        if v[1] == 4:
            all_four.append(v[0])
            return all_four[0]

    length=len(all_four)
    if length == 1:
        return all_four[0]


def check_straight_flush(cards):
    """ Method for finding straight flush of cards in the list of cards
        : param cards: list of cards
        : return: value of top card """

    vals = [(c.get_value(), c.suit) for c in cards] \
           + [(1, c.suit) for c in cards if c.get_value() == 14]  # Add the aces!
    for c in reversed(cards): # Starting point (high card)
        # Check if we have the value - k in the set of cards:
        found_straight = True
        for k in range(1, 5):
            if (c.get_value() - k, c.suit) not in vals:
                found_straight = False
                break
        if found_straight:
            return c.get_value()
