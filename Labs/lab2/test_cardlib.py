from ast import Assert
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

def test_more_card_types():
    """ testing More card types and their methods"""
    hace = AceCard(Suit.Hearts)
    c6 = NumberedCard(6,Suit.Clubs)
    h6 = NumberedCard(6,Suit.Hearts)
    
    print(hace.get_suit().name)
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
    
    
def test_deck_further():
    """ Further testing the deck and its methods"""
    deck = StandardDeck()
    deck2 = StandardDeck()
    assert (deck.deck == deck2.deck) and len(deck.deck) == len(deck2.deck) # Check so that two decks are the same when created

    deck.shuffle()
    assert deck.deck != deck2.deck # Check so that the shuffle function works
    for i in deck.deck:
        assert i in deck2.deck # Check so all cards are in the deck 

    for i in range(10):
        deck.draw()

    assert len(deck.deck) < len(deck2.deck) # Check so that cards are drawn
    assert len(deck.deck) == (52-10) # Check so that the correct number of cards are drawn

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
    assert p1_best.best_hand in HandType and isinstance(p1_best.best_hand,HandType)# Make sure that a HanType can be created and that its of the correct Type


    deck2 = StandardDeck()
    p3 = Hand()
    p4 = Hand()
    for i in range(26): # Draw all cards from the top of the deck
        p3.add_card(deck2.draw())
        p4.add_card(deck2.draw())

    for i in p3.cards: # Check so that no cards show up twice
        assert i not in p4.cards

def test_pokerhands():
    """ Testing Card combinations giving the different poker hands"""
    pass

def test_compare_pokerhands():
    """ Comparison between different poker-hands """
    pass

def test_same_pokerhands():
    """ Comparison between hands with card combinations giving the same poker hand, but different card values
        for both the cards making up the poker hand (for example 2 kings in a pair of kings) and the remaining 3
        cards 
        
        """
    pass

test_more_hands()