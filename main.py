# Main file for window app launch

import sys

from PyQt5 import QtWidgets
from MainWindow import MainWindow

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
