import sys
import random
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow, QProgressBar
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QMainWindow
from multiprocessing import Queue, Process
from MyProject.princessMovement import PrincessMovement
from MyProject.GorilaMovement import GorilaMovement
from random import randint
from MyProject.Fire import FireMovement
from MyProject.barrelMovement import BarrelMovement
from MyProject.key_notifier import KeyNotifier
from MyProject.key_notifier2 import KeyNotifier2
import time

brLevel = 0

class MainWindow(QMainWindow):
    def __init__(self, brojIgraca, lvlNumber):
        super().__init__()

        oImage = QImage("images\\dk.jpg")
        sImage = oImage.scaled(QSize(1000, 562))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)

        self.pix112 = QPixmap('images\\luigiL.png')
        self.pix11 = QPixmap('images\\luigi.png')
        self.pix12 = QPixmap('images\\marioL.jpg')
        self.pix1 = QPixmap('images\\mario.jpg')
        self.pix2 = QPixmap('images\\p.png')
        self.pix22 = QPixmap('images\\pL.png')

        self.pix3 = QPixmap('images\\donkeykong1.png')
        self.pixBottleR = QPixmap('images\\barrel.png')
        self.pixBottleL = QPixmap('images\\barelR.png')
        self.pix32 = QPixmap('images\\donkeykong1.png')

        self.hitSide = False

        self.label2 = QLabel(self)
        self.label12 = QLabel(self)
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

        self.key_notifier = KeyNotifier()
        if (brojIgraca == 1):
            self.key_notifier.key_signal.connect(self.__update_position__)
            self.brojIgracaJedan = True

        else:
            self.brojIgracaJedan = False
            self.key_notifier2 = KeyNotifier2()
            self.key_notifier.key_signal.connect(self.__update_position__)  # -----------------
            self.key_notifier2.key_signal2.connect(self.__update_position2__)  # -----------------
            self.key_notifier2.start()

        self.key_notifier.start()

        self.__init_ui__(brLevel, brojIgraca)

    def __init_ui__(self, brLevel, brojIgraca):
        self.setWindowTitle('Donkey Kong')

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label1.setPixmap(self.pix1)
        self.label1.setGeometry(250, 460, 36, 50)


        self.label2.setPixmap(self.pix2)
        self.label2.setGeometry(475, 3, 36, 50)

        self.label3.setPixmap(self.pix3)
        self.label3.setGeometry(455, 84, 50, 70)




        brLevel += 1

        font = QtGui.QFont()
        font.setPointSize(20)



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

        if (brojIgraca == 2):
            self.label4.setPixmap(self.pix112)
            self.label4.setGeometry(730, 436, 75, 100)

            self.brojIgracaJedan = False
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

            #self.label30.setPixmap(self.pix112)
           # self.label30.setGeometry(350, 475, 36, 50)

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
        self.timerP1.start(5000)
        self.timerP1.timeout.connect(self.invertImage)

    def invertImage(self):
         self.label2.setPixmap(self.pix2)

    def invertMarioL(self):
        self.label1.setPixmap(self.pix12)
    def invertMarioR(self):
        self.label1.setPixmap(self.pix1)

    def invertLuigiL(self):
        self.label4.setPixmap(self.pix112)
    def invertLuigiR(self):
        self.label4.setPixmap(self.pix11)





    def keyPressEvent(self, event):
        a = event.key()
        self.key_notifier.add_key(a)
        if (self.brojIgracaJedan == False):
            b = event.key()
            self.key_notifier2.add_key(b)

    def keyReleaseEvent(self, event):
        a = event.key()
        self.key_notifier.rem_key(a)
        if (self.brojIgracaJedan == False):
            b = event.key()
            self.key_notifier2.rem_key(b)



    def __update_position__(self, key):
        rec1 = self.label1.geometry()

        if key == Qt.Key_Right:
            if rec1.x() < 880:
                self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                self.invertMarioR()
        elif key == Qt.Key_Left:
            if rec1.x() > 110:
                self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                self.invertMarioL()
        elif key == Qt.Key_Up:
                if (rec1.x() > 149 and rec1.x() < 180 ):
                    self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                elif (rec1.x() > 480 and rec1.x() < 507):
                    self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                elif (rec1.x() > 833 and rec1.x() < 856):
                    self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())

        elif key == Qt.Key_Down:
            if rec1.y() < 460:
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())

    def __update_position2__(self, key):
        rec4 = self.label4.geometry()

        if key == Qt.Key_D:
            if rec4.x() < 880:
                self.label4.setGeometry(rec4.x() + 10, rec4.y(), rec4.width(), rec4.height())
                self.invertLuigiR()
        elif key == Qt.Key_A:
            if rec4.x() > 120:
                self.label4.setGeometry(rec4.x() - 10, rec4.y(), rec4.width(), rec4.height())
                self.invertLuigiL()
        elif key == Qt.Key_W:
            self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
        elif key == Qt.Key_S:
            if rec4.y() < 436:
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())



    def moveDonkeyKong(self):
        rec2 = self.label3.geometry()

        if (rec2.x() >= 673):
            self.hitSide = True
            self.label3.setPixmap(self.pix3)
        elif (rec2.x() <= 322):
            self.hitSide = False
            self.label3.setPixmap(self.pix32)

        if (self.hitSide):
            self.label3.setGeometry(rec2.x() - 10, rec2.y(), rec2.width(), rec2.height())
        else:
            self.label3.setGeometry(rec2.x() + 10, rec2.y(), rec2.width(), rec2.height())

    def closeEvent(self, event):
        self.princesMovement.die()
        self.gorilaMovement.die()
        self.key_notifier.die()
        self.key_notifier2.die()

    def shutdown(self, event):
        self.close()

if __name__ == '__main__':
     app = QApplication(sys.argv)
     ex = MainWindow(1, 1)
     sys.exit(app.exec_())