from Pokerview import *
import sys


qt_app = QApplication(sys.argv)
main = MainWindow(names=['John', 'Derin'])

qt_app.exec_()