import cardlib


def test_value():
    "Test of correct value of given value"""
    jack_value=cardlib.JackCard(cardlib)
    assert jack_value.get_value() == 11

    queen_value=cardlib.QueenCard(cardlib)
    assert queen_value.get_value() == 12

    king_value=cardlib.KingCard(cardlib)
    assert king_value.get_value() == 13

    ace_value=cardlib.AceCard(cardlib)
    assert ace_value.get_value() == 14


def test_suit():
    "Test of correct suit of given suit"""
    suit_one = cardlib.Suit.Diamonds
    assert suit_one == 0

    suit_two = cardlib.Suit.Hearts
    assert suit_two == 1

    suit_three = cardlib.Suit.Clubs
    assert suit_three == 2

    suit_four = cardlib.Suit.Spades
    assert suit_four == 3


def test_card():
    "Test correct suit of given cards"""
    card_one=cardlib.NumberedCard(10, cardlib.Suit.Spades)
    assert card_one.get_value() == 10
    assert card_one.get_suit() == 3

    "Test correct value given of given cards"
    card_two = cardlib.AceCard(cardlib.Suit.Hearts)
    assert card_two.get_value() == 14
    assert card_two.get_suit() == 1


def test_compare_value():
    "Test comparison of values"""
    card_1 = cardlib.NumberedCard(3, cardlib.Suit.Spades)
    card_2 = cardlib.NumberedCard(4, cardlib.Suit.Spades)
    card_3 = cardlib.NumberedCard(7, cardlib.Suit.Diamonds)
    card_4 = cardlib.NumberedCard(9, cardlib.Suit.Diamonds)

    assert card_1 < card_2
    assert card_3 != card_4
    assert card_4 > card_3


def test_compare_suit():
    "Test comparison of suits"""
    suit_1= cardlib.Suit.Spades
    suit_2=cardlib.Suit.Diamonds
    suit_3=cardlib.Suit.Hearts

    assert suit_1 > suit_2
    assert suit_2 < suit_3

def test_deck():
    "Test shuffle cards"""
    deck_one = cardlib.StandardDeck()
    deck_one.construct()
    deck_two = cardlib.StandardDeck()
    deck_two.construct()

    deck_one.shuffle()
    deck_two.shuffle()
    assert deck_one != deck_two

    "Test that there is 52 cards in the deck"
    deck=cardlib.StandardDeck()
    assert len(deck) == 52

    "Test draw card"
    deck.draw()
    assert 52 > len(deck)
    deck.draw()
    assert 51 > len(deck)


def test_hand():
    "Test sort card value by value and suit"""
    sort_card = cardlib.Hand()
    sort_card.add_card(cardlib.NumberedCard(4, cardlib.Suit.Diamonds))
    sort_card.add_card(cardlib.NumberedCard(6, cardlib.Suit.Spades))
    sort_card.add_card(cardlib.AceCard(cardlib.Suit.Clubs))
    sort_card.add_card(cardlib.QueenCard(cardlib.Suit.Spades))
    sort_card.sort()
    assert (sort_card[3].get_value()) >= (sort_card[2].get_value()) >= (sort_card[1].get_value())
    assert (sort_card[0].get_suit()) <= (sort_card[1].get_suit()) <= (sort_card[2].get_suit())

    "Test add card"
    d = cardlib.StandardDeck()
    d.shuffle()

    h=cardlib.Hand()
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    assert len(h) == 5

    "Test drop card"
    h.drop_cards([4])
    h.drop_cards([3])
    h.drop_cards([2])
    hand_cards_now=len(h)
    assert len(h) == hand_cards_now


Suit=cardlib.Suit
JackCard=cardlib.JackCard
QueenCard=cardlib.QueenCard
KingCard=cardlib.KingCard
AceCard=cardlib.AceCard
NumberedCard=cardlib.NumberedCard
PokerHand=cardlib.PokerHand
HandType=cardlib.HandType


def test_poker_hands():
    h1 = cardlib.Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))

    h2 = cardlib.Hand()
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

    "Test pair hand type"
    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    ph3 = h1.best_poker_hand(cl)
    ph4 = h2.best_poker_hand(cl)
    assert ph3 < ph4
    assert ph1 < ph2

    assert ph3.HandType == HandType.pair
    assert ph4.HandType == HandType.pair

    cl = [QueenCard(Suit.Clubs), QueenCard(Suit.Spades), KingCard(Suit.Clubs), KingCard(Suit.Spades)]
    ph5 = h1.best_poker_hand(cl)

    assert ph5.HandType == HandType.full_house

    "Test straight hand type"
    ph6 = PokerHand([AceCard(Suit.Spades), NumberedCard(2,Suit.Hearts), NumberedCard(3,Suit.Clubs)
                    , NumberedCard(4,Suit.Hearts), NumberedCard(5,Suit.Hearts)])

    ph7 = PokerHand([AceCard(Suit.Clubs), KingCard(Suit.Diamonds), JackCard(Suit.Hearts)
                    , QueenCard(Suit.Diamonds), NumberedCard(10,Suit.Spades)])
    ph8 = PokerHand([AceCard(Suit.Spades), NumberedCard(2, Suit.Hearts), NumberedCard(3, Suit.Clubs)
                        , NumberedCard(4, Suit.Hearts), NumberedCard(5, Suit.Hearts), NumberedCard(6, Suit.Hearts)])

    assert ph6.HandType == HandType.straight
    assert ph7.HandType == HandType.straight

    assert ph7 > ph6
    assert ph8 > ph6

    "Test straight flush hand type"

    ph9 = PokerHand([NumberedCard(2, Suit.Hearts), NumberedCard(3, Suit.Hearts)
                        , NumberedCard(4, Suit.Hearts), NumberedCard(5, Suit.Hearts), NumberedCard(6, Suit.Hearts)])
    assert ph9.value == 6
    assert ph9.HandType == HandType.straight_flush

    "Test  flush hand type"

    ph10 = PokerHand([NumberedCard(10, Suit.Hearts), NumberedCard(3, Suit.Hearts)
                        , NumberedCard(9, Suit.Hearts), NumberedCard(5, Suit.Hearts), KingCard(Suit.Hearts)])
    ph10_2 = PokerHand([NumberedCard(10, Suit.Spades), NumberedCard(3, Suit.Spades)
                         , NumberedCard(9, Suit.Spades), NumberedCard(6, Suit.Spades), KingCard(Suit.Spades)])
    assert ph10.value == [13, 10, 9, 5, 3]
    assert ph10_2.value == [13, 10, 9, 6, 3]
    assert ph10.HandType == HandType.flush
    assert ph10 <ph10_2

    "Test three of a kind"
    ph11 = PokerHand([NumberedCard(10, Suit.Clubs), NumberedCard(3, Suit.Hearts)
                         , NumberedCard(10, Suit.Diamonds), NumberedCard(10, Suit.Hearts), KingCard(Suit.Hearts)])
    ph11_2 = PokerHand([NumberedCard(10, Suit.Clubs), NumberedCard(3, Suit.Hearts)
                         , NumberedCard(10, Suit.Diamonds), NumberedCard(10, Suit.Hearts), JackCard(Suit.Hearts)])
    assert ph11.value == (10, [13, 3])
    assert ph11.HandType == HandType.three_of_a_kind
    assert ph11 >ph11_2

    "Test four of a kind"
    ph12 = PokerHand([NumberedCard(10, Suit.Clubs), NumberedCard(10, Suit.Hearts)
                         , NumberedCard(10, Suit.Diamonds), NumberedCard(10, Suit.Hearts), KingCard(Suit.Hearts)])
    ph12_2 = PokerHand([NumberedCard(10, Suit.Clubs), NumberedCard(10, Suit.Hearts)
                         , NumberedCard(10, Suit.Diamonds), NumberedCard(10, Suit.Hearts), AceCard(Suit.Hearts)])
    assert ph12.value == (10, [13])
    assert ph12.HandType == HandType.four_of_a_kind
    assert ph12 < ph12_2

    "Test two pairs"
    ph13 = PokerHand([NumberedCard(6, Suit.Clubs), NumberedCard(4, Suit.Hearts)
                         , NumberedCard(6, Suit.Diamonds), NumberedCard(4, Suit.Hearts), KingCard(Suit.Hearts)])
    ph13_2 = PokerHand([NumberedCard(6, Suit.Clubs), NumberedCard(4, Suit.Hearts)
                         , NumberedCard(6, Suit.Diamonds), NumberedCard(4, Suit.Hearts), NumberedCard(2,Suit.Hearts)])
    assert ph13.value == (6, 4, [13])
    assert ph13.HandType == HandType.two_pair
    assert ph13 > ph13_2


