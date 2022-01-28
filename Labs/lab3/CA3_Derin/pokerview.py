from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import cardlib
from pokermodel import *


class Player(QWidget):
    def __init__(self,player):
        super().__init__()
        self.player=player

        h_box = QHBoxLayout()

        player_section=QLabel(player.player_name)
        h_box.addWidget(player_section)

        self.money_section=QLabel()
        self.new_cash()
        player.indicator.connect(self.new_cash())

        self.cards = QLabel()
        self.new_cards()
        player.card.connect(self.new_cards())

        f_box = QVBoxLayout()
        f_box.addWidget(self.cards)
        f_box.addWidget(self.money_section)
        f_box.addLayout(h_box)
        self.setLayout(f_box)

    def new_cards(self):
        self.cards.setText(str([card.__str__() for card in self.player.hand.cards]))

    def new_cash(self):
        self.money_section.setText(str(self.player.cash))




class TableScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        #self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))




class Card(QWidget):
    def __init__(self,game):
        super().__init__()
        self.game =game
        string_card = [card.__str__() for card in game.add_card_signal]
        self.str_cards = string_card
        vbox = QVBoxLayout()
        string=str(string_card)
        self.card_text = QLabel(string)
        game.add_card()
        game.add_card.connect(self.new_card_str)
        vbox.addWidget(self.card_label)

        self.setLayout(vbox)

    def new_card_str(self):
        self.card_text.setText(str([card.__str__() for card in self.model.table.hand.cards]))




class Window(QGroupBox):
    def __init__(self, game):
        super().__init__("Main Window")
        self.game = game

        self.button_call=QPushButton("Call")
        self.button_fold = QPushButton('Fold')
        self.button_raise = QPushButton('Bet')
        self.button_raise_section=QLineEdit(self)

        h_box=QHBoxLayout()
        h_box.addWidget(self.button_raise_section)
        h_box.addWidget(self.button_raise)

        q_box = QVBoxLayout()
        q_box.addWidget(self.button_call)
        q_box.addLayout(h_box)
        q_box.addWidget(self.button_fold)
        self.setGeometry(400, 500, 500, 400)

        self.setLayout(q_box)

        self.button_call.clicked.connect(TexasHoldEm.call)
        self.button_fold.clicked.connect(TexasHoldEm.fold)

