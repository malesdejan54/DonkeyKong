import sys
from MyProject.MainWindow import MainWindow
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QFont, QPixmap
from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication, QPushButton
from PyQt5.QtCore import Qt


class Menu(QMainWindow):

    def __init__(self):
        super().__init__()

        oImage = QImage("images\\menu.jpg")

        self.label = QLabel(self)
        self.label1Player = QLabel(self)
        self.oneplayer = QPixmap('images\\1p.png')

        self.label2Player = QLabel(self)
        self.twoplayer = QPixmap('images\\2p.png')

        self.left = 400
        self.top = 200
        self.width = 1000
        self.height = 562

        palette = QPalette()
        sImage = oImage.scaled(QSize(1000, 562))
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.__init_ui__()

    def __init_ui__(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('donkeykong.png'))
        #self.setWindowState(Qt.WindowFullScreen)

        self.setWindowTitle("Menu")

        button4 = QPushButton('QUIT', self)
        button4.resize(220, 43)
        button4.move(400, 390)
        button4.clicked.connect(self.quit_on_click)

        self.label1Player.setPixmap(self.oneplayer)
        self.label1Player.setGeometry(300, 280, 395, 43)
        self.label1Player.mousePressEvent = self.one_players_on_click

        self.label2Player.setPixmap(self.twoplayer)
        self.label2Player.setGeometry(300, 340, 395, 43)
        self.label2Player.mousePressEvent = self.two_players_on_click

        self.show()

    def one_players_on_click(self, event):
        self.one = MainWindow(1, 1, self)
        self.one.show()
        self.hide()

    def two_players_on_click(self, event):
        self.two = MainWindow(2,1,self)
        self.two.show()
        self.hide()

    def quit_on_click(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    sys.exit(app.exec_())
