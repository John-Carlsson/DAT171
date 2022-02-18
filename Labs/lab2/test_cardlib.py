import pytest
from enum import Enum
from cardlib import *


# This test assumes you call your suit class "Suit" and the colours "Hearts and "Spades"
def test_cards():
    h5 = NumberedCard(4, Suit.Hearts)
    assert isinstance(h5.suit, Enum)
    
    sk = KingCard(Suit.Spades)
    assert sk.get_value() == 13

    assert h5 < sk
    assert h5 == h5

    with pytest.raises(TypeError):
        pc = PlayingCard(Suit.Clubs)
    

# This test assumes you call your shuffle method "shuffle" and the method to draw a card "draw"
def test_deck():
    d = StandardDeck()
    c1 = d.draw()
    c2 = d.draw()
    assert not c1 == c2

    d2 = StandardDeck()
    d2.shuffle()
    c3 = d2.draw()
    c4 = d2.draw()
    assert not ((c3, c4) == (c1, c2))
    print("second test done")

# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    assert len(h.cards) == 5

    h.sort()
    for i in range(3):
        assert h.cards[i] < h.cards[i+1] or h.cards[i] == h.cards[i+1]

    cards = h.cards.copy()
    h.drop_cards([3, 0, 1])
    assert len(h.cards) == 2
    assert h.cards[0] == cards[2]
    assert h.cards[1] == cards[4]
    print("third test done")

def test_pokerhands():
    h1 = Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))

    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(AceCard(Suit.Hearts))

    cl = [NumberedCard(10, Suit.Diamonds), NumberedCard(9, Suit.Diamonds),
          NumberedCard(8, Suit.Clubs), NumberedCard(6, Suit.Spades)]

    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    ph2 = h2.best_poker_hand(cl)
    # assert ph1 == PokerHand( <insert your handtype class and data here> )
    # assert ph2 == PokerHand( <insert your handtype class and data here> )

    assert ph1 < ph2

    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    ph3 = h1.best_poker_hand(cl)
    ph4 = h2.best_poker_hand(cl)
    assert ph3 < ph4
    assert ph1 < ph2

    # assert ph3 == PokerHand( <insert your handtype class and data here> )
    # assert ph4 == PokerHand( <insert your handtype class and data here> )

    cl = [QueenCard(Suit.Clubs), QueenCard(Suit.Spades), KingCard(Suit.Clubs), KingCard(Suit.Spades)]
    ph5 = h1.best_poker_hand(cl)
    # assert ph5 == PokerHand( <insert your handtype for a Full House and data here> )

# Test more cardtypes
def test_more_card_types():
    """ testing More card types and their methods"""
    hace = AceCard(Suit.Hearts)
    c6 = NumberedCard(6,Suit.Clubs)
    h6 = NumberedCard(6,Suit.Hearts)
    
    assert hace.get_suit().name == 'Hearts'
    assert hace.get_suit().value == 0
    assert hace.get_value() == 14
    assert isinstance(hace, AceCard)

    assert c6.get_suit().name == 'Clubs'
    assert c6.get_suit().value == 2
    assert c6.get_value() == 6
    assert isinstance(c6, NumberedCard)

    assert hace > c6
    assert c6 != h6 # Check so that to cards with the same value but different suit is not worth the same
    assert str(c6) == '6 of Clubs' # Check so that it prints correctly
    

# This test further tests the deck and the cards within it, 
# such as making sure the cards are no longer in the deck, that the correct number of cards are drawn
# and if the deck is empty and a message is returned
def test_deck_further():
    """ Further testing the deck and its methods"""
    deck = StandardDeck()
    deck2 = StandardDeck()
    assert (deck.deck == deck2.deck) and len(deck.deck) == len(deck2.deck) # Check so that two decks are the same when created

    deck.shuffle()
    assert deck.deck != deck2.deck # Check so that the shuffle function works
    for i in deck.deck:
        assert i in deck2.deck # Check so all cards are in the deck 

    p1 = Hand()
    for i in range(10):
        p1.add_card(deck.draw())

    assert len(deck.deck) < len(deck2.deck) # Check so that cards are drawn
    for card in p1.cards:
        assert card not in deck.deck # Check so that drawn cards are not in the deck anymore

    assert len(deck.deck) == (52-10) # Check so that the correct number of cards are drawn

    for i in range(42):
        deck.draw()
    assert deck.draw() == 'inga kort kvar' # Check so that when no cards are left it returns something else


# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
# The test checks so that cards are correctly drawn and added to the hand
# and that dropping cards are limited to the hand size and that the same index "dropped" twice does not remove two cards, only one at the index
# Checks so that a PokerHand object is created when the best_poker_hand method is called
def test_more_hands():
    """ testing More hand methods """
    deck = StandardDeck()
    deck.shuffle()
    
    p1 = Hand()
    p2 = Hand()
    for i in range(5): # Draw 5 cards from the top of the deck, random becase of shuffle
        p1.add_card(deck.draw())
        p2.add_card(deck.draw())

    assert p1 != p2 # Check so that the hand are not the same
    assert len(p1.cards) == 5 # Check so that the correct number of cards are drawn

    p1.drop_cards([4,4,3]) # make sure that submitting the same index twice and removing the rightmost card twice only happens once
    assert len(p1.cards) == 3
    assert p1.drop_cards([len(p1.cards)]) == 'Too few cards in hand' # Make sure you can't drop a card thats out of index
    
    p1_best = p1.best_poker_hand()
    assert p1_best.best_hand in HandType and isinstance(p1_best.best_hand,HandType) # Make sure that a HandType can be created and that its of the correct Type

# Testing Card combinations giving different or the same pokerhands
def test_pokerhands():
    p1 = Hand()
    p2 = Hand()

    p1.add_card(NumberedCard(2,Suit.Diamonds))
    p1.add_card(AceCard(Suit.Diamonds))
    p2.add_card(AceCard(Suit.Clubs))
    p2.add_card(NumberedCard(2,Suit.Clubs))

    assert p1.best_poker_hand() > p2.best_poker_hand() # Check so that if the same pokerhand is compared, the Suit of the highest card decide who wins

    table = Hand()
    table.add_card(AceCard(Suit.Spades))
    table.add_card(NumberedCard(6,Suit.Clubs))
    table.add_card(NumberedCard(2,Suit.Hearts))
    table.add_card(NumberedCard(2,Suit.Diamonds))
    p1.sort()
    p1.drop_cards([0])
    p1.add_card(AceCard(Suit.Hearts))

    assert p1.best_poker_hand(table.cards) > p2.best_poker_hand(table.cards) # Check so that a full house of 3 aces and two 2's are better than a three of a kind of twos 

def test_compare_pokerhands():
    """ Comparison between different poker-hands """
    p1 = Hand()
    p2 = Hand()
    table = Hand()

    table.add_card(NumberedCard(2,Suit.Diamonds))
    table.add_card(NumberedCard(7,Suit.Diamonds))
    table.add_card(NumberedCard(8,Suit.Diamonds))
    table.add_card(NumberedCard(3,Suit.Diamonds))

    p1.add_card(JackCard(Suit.Diamonds))
    p1.add_card(NumberedCard(10,Suit.Spades))

    p2.add_card(NumberedCard(3,Suit.Diamonds))
    p2.add_card(KingCard(Suit.Spades))
   
    # Here player 1 has a flush with his highest card of the suit being a Jack,
    # player 2 has a flush with the highest vard of the suit being a 8 on table but has a king on hand
    # Here i take in to account that the highest card in the flush determines who win and not highest card over all.
    assert p1.best_poker_hand(table.cards) > p2.best_poker_hand(table.cards)
    
    
    
    

def test_same_pokerhands():

    """ Comparison between hands with card combinations giving the same poker hand, but different card values
        for both the cards making up the poker hand (for example 2 kings in a pair of kings) and the remaining 3
        cards 
        """
    p1 = Hand()
    p2 = Hand()
    table = Hand()
    p1.add_card(KingCard(Suit.Diamonds))
    p1.add_card(KingCard(Suit.Hearts))

    p2.add_card(QueenCard(Suit.Diamonds))
    p2.add_card(QueenCard(Suit.Diamonds))

    assert p1.best_poker_hand() > p2.best_poker_hand() # Check so that pairs work

    table.add_card(NumberedCard(4,Suit.Spades))
    table.add_card(NumberedCard(4,Suit.Clubs))
    assert p1.best_poker_hand(cards = table.cards) > p2.best_poker_hand(cards = table.cards)

    p1.drop_cards([0])
    p2.drop_cards([0])
    p1.add_card(NumberedCard(4,Suit.Hearts))
    p2.add_card(NumberedCard(4,Suit.Diamonds))

    table.add_card(KingCard(Suit.Spades))
    table.add_card(NumberedCard(4,Suit.Spades))
    table.add_card(NumberedCard(4,Suit.Clubs))

    p1 = Hand()
    p2 = Hand()
    table = Hand()
    p1.add_card(NumberedCard(4,Suit.Hearts))
    p1.add_card(NumberedCard(2,Suit.Hearts))
    p2.add_card(NumberedCard(4,Suit.Diamonds))
    p2.add_card(NumberedCard(2,Suit.Diamonds))
    table.add_card(NumberedCard(4,Suit.Spades))
    table.add_card(NumberedCard(4,Suit.Clubs))
    table.add_card(NumberedCard(2,Suit.Clubs))
    assert p2.best_poker_hand(table.cards) > p1.best_poker_hand(table.cards) # Chekc so that two full houses with the exact same values check for suit
    
