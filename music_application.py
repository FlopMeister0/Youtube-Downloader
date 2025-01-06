import site
import PyQt5 as py
from PyQt5 import QtCore, QtWidgets, QtGui
import random
import sys

class Music_Application(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QWidget.QPushButton("Click Me!")
        self.text = QWidget.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)

        self.layout = QWidget = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

        @QtCore.Slot()
        def magic(self):
            self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = Music_Application()
    widget.resize(800,600)
    widget.show()

    sys.exit(app.exec())