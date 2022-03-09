from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys
from Pokermodel import *


class GameView(QWidget):
    def __init__(self, game_model):
        super().__init__()

        self.labels = dict()
        self.labels['pot'] = QLabel('Total pot: ' + str(game_model.money.pot) + " $")
        self.labels['last_bet'] = QLabel('Last bet placed: ' + str(game_model.money.current_bet) + " $")

        # then arranging them in the desired layout
        vbox = QVBoxLayout()
        for label in self.labels.values():
            vbox.addWidget(label)

        bet_button = QPushButton('Bet')
        bet_scale = QSpinBox()
        bet_scale.setMaximum(game_model.active_player.cash)
        fold_button = QPushButton('Fold')
        call_button = QPushButton('Call')
        end_turn_button = QPushButton('End turn/Pass')

        buttons = [bet_scale, bet_button, fold_button, call_button, end_turn_button]
        for button in buttons:
            vbox.addWidget(button)

        self.setLayout(vbox)

        def bet_click():
            game_model.bet(bet_scale.value())
            end_turn_click()

        def fold_click():
            bet_scale.setValue(0)
            game_model.fold()

        def call_click():
            game_model.call()
            end_turn_click()

        def end_turn_click():
            game_model.end_turn()
            bet_scale.setMaximum(game_model.active_player.cash)
            bet_scale.setValue(0)

        bet_button.clicked.connect(bet_click)
        fold_button.clicked.connect(fold_click)
        call_button.clicked.connect(call_click)
        end_turn_button.clicked.connect(end_turn_click)

        # almost always storing a reference to the related model
        self.game = game_model
        # and connecting some method for updating the state to the corresponding signals
        game_model.money.total_pot_signal.connect(self.update_pot)
        game_model.money.current_bet_signal.connect(self.update_current_bet)

    def update_pot(self):
        self.labels['pot'].setText('Total pot: ' + str(self.game.money.pot) + " $")

    def update_current_bet(self):
        self.labels['last_bet'].setText('Last bet placed: ' + str(self.game.money.current_bet) + " $")

    hbox = QHBoxLayout()


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """

    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """

    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    for suit_file, suit in zip('HDSC', range(4)):  # Check the order of the suits here!!!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit_file
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class PlayerView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: PlayerModel, card_spacing: int = 150, padding: int = 10):
        """
        Initializes the view to display the content of the given model
        :cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :card_spacing: Spacing between the visualized cards.
        :padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding
        self.score_labels = QHBoxLayout()
        self.model = card_model
        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        # The view can listen to changes:
        card_model.card_signal.connect(self.change_cards)
        # It is completely optional if you want to do it this way, or have some overreaching Player/GameState
        # call the "change_cards" method instead. z

        # Add the cards the first time around to represent the initial state.
        self.change_cards()

        self.labels = dict()
        self.labels[self.model] = QLabel("Money: " + str(self.model.cash) + " $")

        # then arranging them in the desired layout
        vbox = QVBoxLayout()
        for label in self.labels.values():
            label.setAlignment(Qt.AlignRight)
            label.setFont(QFont('Times', 20))
            vbox.addWidget(label)

        self.model.cash_signal.connect(self.update_cash)

        self.setLayout(vbox)

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model.cards):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit)
            renderer = self.back_card if self.model.flipped_cards else self.all_cards[graphics_key]
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            # We could also do cool things like marking card by making them transparent if we wanted to!
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)

        self.update_view()

    def update_cash(self):
        self.labels[self.model].setText("Money: " + str(self.model.cash) + " $")

    def update_view(self):
        scale = (self.viewport().height() - 2 * self.padding) / 313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding // scale, -self.padding // scale,
                          self.viewport().width() // scale, self.viewport().height() // scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)


class TableView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: TableModel, card_spacing: int = 150, padding: int = 10):
        """
        Initializes the view to display the content of the given model
        :TableModel: A model that represents a set of cards. The table will be treated as player with some modifications.
        :card_spacing: Spacing between the visualized cards.
        :padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding

        self.model = card_model
        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        # The view can listen to changes:
        card_model.cards_signal.connect(self.change_cards)
        # It is completely optional if you want to do it this way, or have some overreaching Player/GameState
        # call the "change_cards" method instead. z

        # Add the cards the first time around to represent the initial state.
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model.cards):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit)
            renderer = self.all_cards[graphics_key]
            c = CardItem(renderer, i)
            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)
            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            # We could also do cool things like marking card by making them transparent if we wanted to!
            # c.setOpacity(0.5 if self.model.marked(i) else 1.0)
            self.scene.addItem(c)
        self.update_view()

    def update_view(self):
        scale = (self.viewport().height() - 2 * self.padding) / 313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding // scale, -self.padding // scale,
                          self.viewport().width() // scale, self.viewport().height() // scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we got to adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)


class MainWindow(QWidget):
    winner_signal = pyqtSignal()

    def __init__(self, names=['John', 'Derin']):
        super().__init__()
        self.box = QHBoxLayout()        # Create large box
        self.game = TexasHoldEm(names)  # Create game
        game = self.game
        card_box = QVBoxLayout()        # Vertical box for table and player information
        player_box = QHBoxLayout()      # Horizontal box for player's cards
        player_labels = QHBoxLayout()   # Box for names
        buttons = QVBoxLayout()         # Box for buttons
        table_box = QHBoxLayout()       # Box for table

        # Add the table at the top
        table = TableView(game.table)
        table_box.addWidget(table)
        card_box.addLayout(table_box)

        # Add the players under the table
        for player in game.players:
            # Player cards
            playerview = PlayerView(player)
            player_box.addWidget(playerview)

            # Player names
            label = QLabel(player.name)
            label.setAlignment(Qt.AlignCenter)
            label.setFont(QFont('Times', 20))
            player_labels.addWidget(label)

        # Add the names and their cards
        card_box.addLayout(player_labels)
        card_box.addLayout(player_box)

        # Add the box with the table and players to the big box
        self.box.addLayout(card_box)

        # Add the buttons
        buttons.addWidget(GameView(game))
        self.box.addLayout(buttons)

        self.setLayout(self.box)
        self.show()

