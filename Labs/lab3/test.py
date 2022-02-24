from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys



app = QApplication(sys.argv)

box = QVBoxLayout()
box.addWidget()
box.addWidget()
player_view = QGroupBox("Player 1")
player_view.setLayout(box)
player_view.show()

app.exec_()