import sys
import random
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QProgressBar
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from multiprocessing import Queue, Process
from princessMovement import PrincessMovement
from GorilaMovement import  GorilaMovement
from random import randint
from Fire import FireMovement
from barrelMovement import BarrelMovement
import time
br = 1
brLevel = 0

class MainWindow(QMainWindow):
    def __init__(self, brojIgraca, lvlNumber):
        super().__init__()

        oImage = QImage("images\\dk.jpg")
        sImage = oImage.scaled(QSize(1000, 562))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.pix1 = QPixmap('images\\luigiL.png')
        self.pix11 = QPixmap('images\\luigi.png')
        self.pix12 = QPixmap('images\\marioL.png')
        self.pix112 = QPixmap('images\\mario.png')
        self.pix2 = QPixmap('images\\princes')
        self.pix22 = QPixmap('images\\princesL')

        self.pix3 = QPixmap('images\\donkeykong')
        self.pixBottleR = QPixmap('images\\barrel.png')
        self.pixBottleL = QPixmap('images\\barellR.png')
        self.pix32 = QPixmap('images\\donkeykong')

        self.hitSide = False

        self.label2 = QLabel(self)
        self.label4 = QLabel(self)
        self.label5 = QLabel(self)
        self.label6 = QLabel(self)
        self.label7 = QLabel(self)
        self.label3 = QLabel(self)
        self.label30 = QLabel(self)
        self.labelScore = QLabel(self)
        self.labelLifes1 = QLabel(self)
        self.labelLifes2 = QLabel(self)
        self.life1ispis = QLabel(self)
        self.life2ispis = QLabel(self)
        self.label1 = QLabel(self)
        self.label11 = QLabel(self)
        self.one = None

        self.labelLevel = QLabel(self)
        self.ispisLabel1 = QLabel(self)
        self.playerRez1 = QLabel(self)
        self.playerRez11 = QLabel(self)
        self.playerRez2 = QLabel(self)
        self.playerRez22 = QLabel(self)
        self.gameoverLab = QLabel(self)
        self.izlazIzIgre = QLabel(self)

        self.poeniPL1 = 0
        self.poeniPL2 = 0
        self.trenutniNivo = lvlNumber

        self.ispisLabel1.setText('Level: ')
        self.ispisLabel1.setStyleSheet('color: blue')

        self.playerRez1.setText('P1: ')
        self.playerRez1.setStyleSheet('color: red')

        self.playerRez2.setText('P2: ')

        self.life1ispis.setText('P1 Life: ')
        self.life1ispis.setStyleSheet('color: red')

        self.life2ispis.setText('P2 Life: ')

        self.playerRez11.setText(str(self.poeniPL1))
        self.playerRez11.setStyleSheet('color: red')

        self.playerRez22.setText(str(self.poeniPL2))

        self.left = 400
        self.top = 200
        self.width = 1000
        self.height = 562

        self.__init_ui__(brLevel, brojIgraca)

    def __init_ui__(self, brLevel, brojIgraca):
        self.setWindowTitle('Donkey Kong')

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(325, 475, 75, 75)

        self.label2.setPixmap(self.pix2)
        self.label2.setGeometry(475, -15, 75, 100)

        self.label3.setPixmap(self.pix3)
        self.label3.setGeometry(455, 75, 75, 100)

        #self.izlazIzIgre.setPixmap(self.izadji)
       # self.izlazIzIgre.setGeometry(750, 50, 250, 47)
        #self.izlazIzIgre.mousePressEvent = self.shutdown

        brLevel += 1
        font = QtGui.QFont()
        font.setPointSize(20)

        #        self.labelScore.setText(str(0))
        #       self.labelScore.setGeometry(25, 17, 100, 100)
        #      self.labelScore.setFont(font)

        self.labelLevel.setText(str(self.trenutniNivo))
        self.labelLevel.setGeometry(110, 5, 50, 50)
        self.labelLevel.setFont(font)
        self.labelLevel.setStyleSheet('color: blue')

        self.ispisLabel1.setGeometry(2, -20, 100, 100)
        self.ispisLabel1.setFont(font)

        self.lives1 = 3
        self.lives2 = 3

        self.labelLifes1.setText(str(self.lives1))
        self.labelLifes1.setGeometry(110, 15, 100, 100)
        self.labelLifes1.setFont(font)
        self.labelLifes1.setStyleSheet('color: red')

        self.life1ispis.setGeometry(2, 40, 150, 50)
        self.life1ispis.setFont(font)

        self.playerRez1.setGeometry(2, 40, 120, 100)
        self.playerRez11.setGeometry(110, 40, 100, 100)
        self.playerRez1.setFont(font)
        self.playerRez1.setStyleSheet('color: red')
        self.playerRez11.setFont(font)




        if (br == 2):
            self.playerRez2.setGeometry(2, 110, 100, 100)
            self.playerRez22.setGeometry(110, 110, 100, 100)
            self.playerRez2.setFont(font)
            self.playerRez2.setStyleSheet('color: green')
            self.playerRez22.setFont(font)
            self.playerRez22.setStyleSheet('color: green')

            self.life2ispis.setGeometry(2, 85, 120, 100)
            self.labelLifes2.setGeometry(110, 85, 100, 100)
            self.life2ispis.setFont(font)
            self.life2ispis.setStyleSheet('color: green')
            self.labelLifes2.setText(str(self.lives2))
            self.labelLifes2.setStyleSheet('color: green')
            self.labelLifes2.setFont(font)

            self.label30.setPixmap(self.pix112)
            self.label30.setGeometry(630, 475, 75, 75)

        self.princesMovement = PrincessMovement()
        self.princesMovement.princessMovementSignal.connect(self.movePrinces)
        self.princesMovement.start()

        self.gorilaMovement = GorilaMovement()
        self.gorilaMovement.gorilaMovementSignal.connect(self.moveDonkeyKong)
        self.gorilaMovement.start()

        self.show()

    def movePrinces(self):
        self.label2.setPixmap(self.pix22)
        self.timerP1 = QTimer(self)
        self.timerP1.start(2000)
        self.timerP1.timeout.connect(self.invertImage)

    def invertImage(self):
         self.label2.setPixmap(self.pix2)

    def moveDonkeyKong(self):
        rec2 = self.label3.geometry()

        if (rec2.x() >= 580):
            self.hitSide = True
            self.label3.setPixmap(self.pix3)
        elif (rec2.x() <= 320):
            self.hitSide = False
            self.label3.setPixmap(self.pix32)

        if (self.hitSide):
            self.label3.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())
        else:
            self.label3.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())

    def closeEvent(self, event):
        self.princesMovement.die()
        self.gorilaMovement.die()

    def shutdown(self, event):
        self.close()

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = MainWindow(1, 1)
     sys.exit(app.exec_())