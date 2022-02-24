from signal import signal
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys


qt_app = QApplication.instance()
class TexasHoldEm(QObject):
    
    cash_signal = pyqtSignal()
    winner = pyqtSignal((str,))
    total_pot_signal = pyqtSignal()
    current_pot_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__() # Don't forget super init when inheriting!
        self.players = ['Player1', 'Player2']
        self.cash = dict()
        self.total_pot = 0
        self.current_pot = 0

        for player in self.players: # Give players money
            self.cash[player] = 100
        
        self.active_player = self.players[0]
    

    def bet_click(self, amount): # Fixa till det här
        prev = self.cash[self.active_player]
        self.cash[self.active_player] =- amount+prev
        self.cash_signal.emit()
        self.current_pot =+ amount+prev
        
        self.total_pot =+ amount
        self.total_pot_signal.emit()


    
    def passing(self):
        pass

    def fold(self):
        pass

    def call(self):
        pass
        
    def end_turn(self):

        if self.active_player == self.players[0]: self.active_player = self.players[1]
        else: self.active_player = self.players[0]
        


class GameView(QWidget):
    def __init__(self, game_model):
        super().__init__()
        
        # The init method for views should always be quite familiar; it has a section for creating widgets
        # buttons = [QPushButton(game_model.players[0]), QPushButton(game_model.players[1])]
        self.labels = dict()
        for i in range(len(game_model.players)):
            self.labels[game_model.players[i]] = QLabel(game_model.players[i] +'\t\t'+ str(game_model.cash[game_model.players[i]]))

        self.labels['pot'] = QLabel('Total pot' +'\t' + str(game_model.total_pot))
        # then arranging them in the desired layout
        vbox = QVBoxLayout()
        for label in self.labels.values():
            vbox.addWidget(label)
        
        bet_button = QPushButton('Bet')
        bet_scale = QSpinBox()
        pass_button = QPushButton('Pass')
        fold_button = QPushButton('Fold')
        call_button = QPushButton('Call')
        end_turn_button = QPushButton('End turn')

        buttons = [bet_scale, bet_button, pass_button, fold_button, call_button, end_turn_button]
        for button in buttons:
            vbox.addWidget(button)

        self.setLayout(vbox)

        # Controller part happens to be inside this widget as well application
        # def player0_click(): game_model.player_click(0)
        # buttons[0].clicked.connect(player0_click)
        # 
        # def player1_click(): game_model.player_click(1)

        # buttons[1].clicked.connect(player1_click)
        # reset_button.clicked.connect(game_model.reset)

        
        
        
        


        def bet_click():
            game_model.bet_click(bet_scale.value())
        
        # def pass_click():
            # game_model.bet_click()
        
        # def fold_click():
            # game_model.bet_click(bet_scale.value())

        # def call_click():
            # game_model.bet_click(bet_scale.value())

        def end_turn_click():
            game_model.end_turn_click()

        
        

        bet_button.clicked.connect(bet_click)
        pass_button.clicked.connect(game_model.passing)
        fold_button.clicked.connect(game_model.fold)
        call_button.clicked.connect(game_model.call)
        end_turn_button.clicked.connect(game_model.end_turn)
        
        
        # almost always storing a reference to the related model
        self.game = game_model

    
        # and connecting some method for updating the state to the corresponding signals
        game_model.total_pot_signal.connect(self.update_pot)
        game_model.cash_signal.connect(self.update_cash)


        # game_model.winner.connect(self.alert_winner)
        # and giving it an initial update so that we show the initial state
        # self.update_labels()
        
        # This also happens to be the main window, so we can opt to show it immediately
        # (we could also very well leave this up to the caller)
        self.show()
      
        
    def update_pot(self):
        self.labels['pot'].setText('Total pot' +'\t' + str(self.game.total_pot))
    
    def update_cash(self):
        self.labels[self.game.active_player].setText(str(self.game.active_player) +'\t\t' + str(self.game.cash[self.game.active_player]))

    def alert_winner(self, text: str):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()


qt_app = QApplication(sys.argv)
qt_app = QApplication.instance()
game = TexasHoldEm()
view = GameView(game)
qt_app.exec_()