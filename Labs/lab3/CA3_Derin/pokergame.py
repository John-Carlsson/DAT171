import sys
from pokermodel import TexasHoldEm
from pokerview import *

player_one = TexasHoldEm("Player One")
player_two = TexasHoldEm("Player Two")
game = ([player_one, player_two])


app = QApplication(sys.argv)

window = Window(game)
window.show()
app.exec_()



