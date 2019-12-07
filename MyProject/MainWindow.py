from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
import sys
from PyQt5.QtGui import QPixmap
class Window(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Donkey Kong"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        vbox = QVBoxLayout()
        labelImage = QLabel(self)
        pixmap = QPixmap("dk.jpg")
        labelImage.setPixmap(pixmap)
        vbox.addWidget(labelImage)
        self.setLayout(vbox)
        self.show()



App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())