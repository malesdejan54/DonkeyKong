import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import QLabel, QApplication, QMainWindow
from MyProject.princessMovement import PrincessMovement
from MyProject.GorilaMovement import GorilaMovement
from random import randint
from MyProject.Fire import FireMovement
from MyProject.barrelMovement import BarrelMovement
from MyProject.key_notifier import KeyNotifier
from MyProject.key_notifier2 import KeyNotifier2
from MyProject.Pogodak import isHit, restartPlayer,generateBarrel,GorilaFreezeProcess
from MyProject.GameOver import GameOver
from multiprocessing import Process,Queue

brLevel = 0


class MainWindow(QMainWindow):
    def __init__(self, brojIgraca, lvlNumber, menu_widnow):
        super().__init__()

        self.menu_window = menu_widnow
        oImage = QImage("images\\dk.jpg")
        sImage = oImage.scaled(QSize(1000, 562))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))  # 10 = Windowrole
        self.setPalette(palette)
        self.barrelsMovement = None
        self.pix112 = QPixmap('images\\luigiL.png')
        self.pix11 = QPixmap('images\\luigi.png')
        self.pix12 = QPixmap('images\\marioL.jpg')
        self.pix1 = QPixmap('images\\mario.jpg')
        self.pix2 = QPixmap('images\\p.png')
        self.pix22 = QPixmap('images\\pL.png')

        self.pix3 = QPixmap('images\\donkeykong1.png')
        self.pixBottleR = QPixmap('images\\barrelR.png')
        self.pix32 = QPixmap('images\\donkeykong1.png')
        self.pixfire = QPixmap('images\\fire.png')

        self.hitSide = False
        self.barrels_speed = 0.1 #promeljiva za brzinu




        self.label2 = QLabel(self)
        self.label12 = QLabel(self)
        self.label4 = QLabel(self)


        self.label3 = QLabel(self)
        self.labelScore = QLabel(self)
        self.labelLifes1 = QLabel(self)
        self.labelLifes2 = QLabel(self)
        self.life1ispis = QLabel(self)
        self.life2ispis = QLabel(self)
        self.label1 = QLabel(self)

        self.labelLevel = QLabel(self)
        self.ispisLabel1 = QLabel(self)
        self.playerRez1 = QLabel(self)
        self.playerRez11 = QLabel(self)
        self.playerRez2 = QLabel(self)
        self.playerRez22 = QLabel(self)

        self.barrelQueue = Queue()
        self.barrelProcess = Process(target=generateBarrel, args=[self.barrelQueue])
        self.barrels = []
        self.barrelProcess.start()

        self.gorilaStop = Queue()
        self.gorilaStart = Queue()
        self.gorilaBug = Process(target=GorilaFreezeProcess, args=[self.gorilaStart, self.gorilaStop])
        self.gorilaBug.start()

        self.fire_positions = [[400, 400], [500, 400], [550, 400],[700,310],[220,310]]
        self.firelabel = QLabel(self)
        self.firelabel.setPixmap(self.pixfire)



        self.zaustavio = False

        self.PointsM = 0
        self.PointsL = 0
        self.trenutniNivo = lvlNumber
        self.kraj = None

        self.quit_menu = QLabel(self)
        self.quit_img = QPixmap('images\\menubutton.png')
        self.quit_menu.setPixmap(self.quit_img)
        self.quit_menu.setGeometry(800, 50, 75, 50)
        self.quit_menu.mousePressEvent = self.go_to_menu

        self.ispisLabel1.setText('Level: ')
        self.ispisLabel1.setStyleSheet('color: blue')

        self.playerRez1.setText('P1: ')
        self.playerRez1.setStyleSheet('color: red')

        self.playerRez2.setText('P2: ')

        self.life1ispis.setText('P1 Life: ')
        self.life1ispis.setStyleSheet('color: red')

        self.life2ispis.setText('P2 Life: ')

        self.playerRez11.setText(str(self.PointsM))
        self.playerRez11.setStyleSheet('color: red')

        self.playerRez22.setText(str(self.PointsL))

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
            self.brojIgracaJedan = False

            self.label4.setPixmap(self.pix112)
            self.label4.setGeometry(730, 436, 75, 100)

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



        self.princesMovement = PrincessMovement()
        self.princesMovement.princessMovementSignal.connect(self.movePrinces)
        self.princesMovement.start()

        self.barrelsMovement = BarrelMovement(self.barrels_speed)
        self.barrelsMovement.barrelMovementSignal.connect(self.moveBarrels)
        self.barrelsMovement.start()

        self.fires = FireMovement(2)  # napravio tred
        self.fires.fireMovementSignal.connect(self.fire)  # konetovan na fun fire i poziva na svaih 0.08
        self.fires.start()  # pokrece tred

        self.gorilaMovement = GorilaMovement()
        self.gorilaMovement.gorilaMovementSignal.connect(self.moveDonkeyKong)
        self.gorilaMovement.start()

        self.show()

    def movePrinces(self):
        self.label2.setPixmap(self.pix22)
        self.timerP1 = QTimer(self)
        self.timerP1.start(1000)
        self.timerP1.timeout.connect(self.invertImage)

        if isHit(self.label2, self.label1):
            self.newLevel()
        if isHit(self.label2, self.label4):
            self.newLevel()

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
            if rec1.y() >= 460:
                if rec1.x() < 880:
                    self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioR()
            elif rec1.y() < 460 and rec1.y() > 370:
                return

            elif rec1.y() >= 370:
                if rec1.x() < 840:
                    self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioR()
            elif rec1.y() < 370 and rec1.y() > 280:
                return
            elif rec1.y() >= 280:
                if rec1.x() < 790:
                    self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioR()
            elif rec1.y() < 280 and rec1.y() > 190:
                return
            elif rec1.y() >= 185:
                if rec1.x() < 745:
                    self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioR()
            elif rec1.y() < 185 and rec1.y() > 100:
                return
            elif rec1.y() >= 100:
                if rec1.x() < 700:
                    self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioR()
            elif rec1.y() < 100 and rec1.y() > 0:
                return
            elif rec1.y() >= 0:
                if rec1.x() < 620:
                    self.label1.setGeometry(rec1.x() + 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioR()







        elif key == Qt.Key_Left:

            if rec1.y() >= 460:
                if (rec1.x() > 110):
                    self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioL()
            elif rec1.y() < 460 and rec1.y() > 370:
                return

            elif rec1.y() >= 370:
                if rec1.x() > 160:
                    self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioL()
            elif rec1.y() < 370 and rec1.y() > 280:
                return

            elif rec1.y() >= 280:
                if rec1.x() > 200:
                    self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioL()
            elif rec1.y() < 280 and rec1.y() > 190:
                return

            elif rec1.y() >= 185:
                if rec1.x() > 255:
                    self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioL()
            elif rec1.y() < 185 and rec1.y() > 100:
                return

            elif rec1.y() >= 100:
                if rec1.x() > 310:
                    self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioL()
            elif rec1.y() < 100 and rec1.y() > 0:
                return
            elif rec1.y() >= 0:
                if rec1.x() > 380:
                    self.label1.setGeometry(rec1.x() - 10, rec1.y(), rec1.width(), rec1.height())
                    self.invertMarioL()




        elif key == Qt.Key_Up:
            if (rec1.x() > 149 and rec1.x() < 180 and rec1.y() > 378):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 390):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))

            elif (rec1.x() > 480 and rec1.x() < 507 and rec1.y() > 378):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 390):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif (rec1.x() > 833 and rec1.x() < 856 and rec1.y() > 378):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 390):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 176 and rec1.x() < 207) and (rec1.y() > 284 and rec1.y() < 378)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 300):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 585 and rec1.x() < 616) and (rec1.y() < 378 and rec1.y() > 284)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 300):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 221 and rec1.x() < 252) and (rec1.y() > 190 and rec1.y() < 284)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 220):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 738 and rec1.x() < 770) and (rec1.y() > 190 and rec1.y() < 284)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 220):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 693 and rec1.x() < 720) and (rec1.y() < 191 and rec1.y() > 107)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 130):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 356 and rec1.x() < 383) and (rec1.y() < 191 and rec1.y() > 107)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 130):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 383 and rec1.x() < 418) and (rec1.y() > 1 and rec1.y() < 107)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 30):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))
            elif ((rec1.x() > 600 and rec1.x() < 630) and (rec1.y() > 1 and rec1.y() < 107)):
                self.label1.setGeometry(rec1.x(), rec1.y() - 10, rec1.width(), rec1.height())
                if (rec1.y() == 30):
                    self.PointsM = self.PointsM + 1
                    self.playerRez11.setText(str(self.PointsM))

        elif key == Qt.Key_Down:
            if (rec1.x() >= 140 and rec1.x() <= 170 and rec1.y() >= 370 and rec1.y() < 460):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif (rec1.x() >= 480 and rec1.x() <= 507 and rec1.y() >= 370 and rec1.y() < 460):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif (rec1.x() >= 833 and rec1.x() <= 856 and rec1.y() >= 370 and rec1.y() < 460):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 189 and rec1.x() <= 220) and (rec1.y() >= 254 and rec1.y() < 370)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 600 and rec1.x() <= 631) and (rec1.y() < 370 and rec1.y() >= 254)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 221 and rec1.x() <= 252) and (rec1.y() >= 182 and rec1.y() < 274)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 738 and rec1.x() <= 770) and (rec1.y() >= 182 and rec1.y() < 274)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 693 and rec1.x() <= 720) and (rec1.y() < 190 and rec1.y() >= 99)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 356 and rec1.x() <= 383) and (rec1.y() < 190 and rec1.y() >= 99)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 383 and rec1.x() <= 418) and (rec1.y() >= -10 and rec1.y() < 97)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())
            elif ((rec1.x() >= 600 and rec1.x() <= 630) and (rec1.y() >= -10 and rec1.y() < 97)):
                self.label1.setGeometry(rec1.x(), rec1.y() + 10, rec1.width(), rec1.height())

    def __update_position2__(self, key):
        rec4 = self.label4.geometry()

        if key == Qt.Key_D:

            if rec4.y() >= 436:
                if rec4.x() < 880:
                    self.label4.setGeometry(rec4.x() + 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiR()
            elif rec4.y() < 436 and rec4.y() > 355:
                return
            elif rec4.y() >= 340:
                if rec4.x() < 840:
                    self.label4.setGeometry(rec4.x() + 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiR()
            elif rec4.y() < 340 and rec4.y() > 274:
                return
            elif rec4.y() >= 250:
                if rec4.x() < 790:
                    self.label4.setGeometry(rec4.x() + 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiR()
            elif rec4.y() < 250 and rec4.y() > 170:
                return
            elif rec4.y() >= 165:
                if rec4.x() < 750:
                    self.label4.setGeometry(rec4.x() + 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiR()
            elif rec4.y() < 165 and rec4.y() > 85:
                return
            elif rec4.y() >= -40:
                if rec4.x() < 700:
                    self.label4.setGeometry(rec4.x() + 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiR()
            elif rec4.y() < -40 and rec4.y() >= 100:
                return
        elif key == Qt.Key_A:
            if rec4.y() >= 436:
                if rec4.x() > 120:
                    self.label4.setGeometry(rec4.x() - 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiL()
            elif rec4.y() < 436 and rec4.y() > 355:
                return
            elif rec4.y() >= 340:
                if rec4.x() > 160:
                    self.label4.setGeometry(rec4.x() - 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiL()
            elif rec4.y() < 340 and rec4.y() > 274:
                return
            elif rec4.y() >= 250:
                if rec4.x() > 210:
                    self.label4.setGeometry(rec4.x() - 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiL()
            elif rec4.y() < 250 and rec4.y() > 170:
                return
            elif rec4.y() >= 165:
                if rec4.x() > 250:
                    self.label4.setGeometry(rec4.x() - 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiL()
            elif rec4.y() < 165 and rec4.y() > 85:
                return
            elif rec4.y() >= 0:
                if rec4.x() > 310:
                    self.label4.setGeometry(rec4.x() - 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiL()
            elif rec4.y() >= -40:
                if rec4.x() > 360:
                    self.label4.setGeometry(rec4.x() - 10, rec4.y(), rec4.width(), rec4.height())
                    self.invertLuigiL()




        elif key == Qt.Key_W:
            if (rec4.x() > 149 and rec4.x() < 180 and rec4.y() > 350):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= 362):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif (rec4.x() > 480 and rec4.x() < 507 and rec4.y() > 350):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= 362):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif (rec4.x() > 833 and rec4.x() < 856 and rec4.y() > 350):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= 362):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 176 and rec4.x() < 207) and (rec4.y() > 256 and rec4.y() < 350)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() == 286):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 575 and rec4.x() < 606) and (rec4.y() < 350 and rec4.y() > 256)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() == 286):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 221 and rec4.x() < 252) and (rec4.y() > 170 and rec4.y() < 284)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= 180):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 738 and rec4.x() < 770) and (rec4.y() > 170 and rec4.y() < 284)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= 180):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 693 and rec4.x() < 720) and (rec4.y() < 191 and rec4.y() > 83)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= 93):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 356 and rec4.x() < 383) and (rec4.y() < 191 and rec4.y() > 83)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= 93):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 383 and rec4.x() < 418) and (rec4.y() > -20 and rec4.y() < 107)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= -10):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
            elif ((rec4.x() > 600 and rec4.x() < 630) and (rec4.y() > -20 and rec4.y() < 107)):
                self.label4.setGeometry(rec4.x(), rec4.y() - 10, rec4.width(), rec4.height())
                if (rec4.y() <= -10):
                    self.PointsL = self.PointsL + 1
                    self.playerRez22.setText(str(self.PointsL))
        elif key == Qt.Key_S:
            if (rec4.x() >= 140 and rec4.x() <= 170 and rec4.y() >= 330 and rec4.y() < 430):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif (rec4.x() >= 480 and rec4.x() <= 507 and rec4.y() >= 330 and rec4.y() < 430):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif (rec4.x() >= 833 and rec4.x() <= 856 and rec4.y() >= 330 and rec4.y() < 430):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 189 and rec4.x() <= 220) and (rec4.y() >= 214 and rec4.y() < 340)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 600 and rec4.x() <= 631) and (rec4.y() < 340 and rec4.y() >= 214)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 221 and rec4.x() <= 252) and (rec4.y() >= 152 and rec4.y() < 254)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 738 and rec4.x() <= 770) and (rec4.y() >= 152 and rec4.y() < 254)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 693 and rec4.x() <= 720) and (rec4.y() < 160 and rec4.y() >= 59)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 356 and rec4.x() <= 383) and (rec4.y() < 160 and rec4.y() >= 59)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 383 and rec4.x() <= 418) and (rec4.y() >= -50 and rec4.y() < 67)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())
            elif ((rec4.x() >= 600 and rec4.x() <= 630) and (rec4.y() >= -50 and rec4.y() < 67)):
                self.label4.setGeometry(rec4.x(), rec4.y() + 10, rec4.width(), rec4.height())

    def fire(self):


        random_postion = randint(0, len(self.fire_positions) - 1)
        self.firelabel.setGeometry(self.fire_positions[random_postion][0], self.fire_positions[random_postion][1], 20,20)


    def moveBarrels(self):

        if isHit(self.firelabel, self.label1):
            self.lives1 -= 1
            self.labelLifes1.setText(str(self.lives1))
            restartPlayer(self.label1, 1)
            if self.lives1 == 0:
                if self.brojIgracaJedan:
                    self.kraj = GameOver(0, self.PointsM)
                    self.label1.hide()
                else:
                    if self.lives2 <= 0:
                        self.kraj = GameOver(1, self.PointsM)
                        self.label1.hide()
                    else:
                        self.kraj = GameOver(2, self.PointsL)
                        self.label1.hide()

        if isHit(self.firelabel, self.label4):
            self.lives2 -= 1
            self.labelLifes2.setText(str(self.lives2))
            restartPlayer(self.label4, 2)
            if self.lives2 == 0:
                if self.lives1 <= 0:
                    self.kraj = GameOver(2, self.PointsL)
                    self.label4.hide()
                else:
                    self.kraj = GameOver(1, self.PointsM)
                    self.label4.hide()

        rec = self.label3.geometry()

        a = randint(0, 100)
        if a % 30 == 0:
            barrel = QLabel(self)
            self.barrels.append(barrel)
            self.barrels[len(self.barrels) - 1].setPixmap(self.pixBottleR)
            self.barrels[len(self.barrels) - 1].setGeometry(rec.x(), rec.y(), 40, 40)
            self.barrels[len(self.barrels) - 1].show()

        for barrel in self.barrels:
            recb = barrel.geometry()
            barrel.setGeometry(recb.x(), recb.y() + 10, recb.width(), recb.height())

            if recb.y() > 500:
                barrel.hide()
                self.barrels.remove(barrel)

            if isHit(barrel, self.label1):
                self.lives1 -= 1
                self.labelLifes1.setText(str(self.lives1))
                barrel.hide()
                self.barrels.remove(barrel)
                restartPlayer(self.label1, 1)

                if self.lives1 == 0:
                    if self.brojIgracaJedan:
                        self.kraj = GameOver(0, self.PointsM)
                        self.label1.hide()


                    else:
                        if self.lives2 <= 0:
                            self.kraj = GameOver(1, self.PointsM)
                            self.label1.hide()
                        else:
                            self.kraj = GameOver(2, self.PointsL)
                            self.label1.hide()



            if isHit(barrel, self.label4):
                self.lives2 -= 1
                self.labelLifes2.setText(str(self.lives2))
                barrel.hide()
                self.barrels.remove(barrel)
                restartPlayer(self.label4, 2)

                if self.lives2 == 0:
                    if self.lives1 <= 0:
                        self.kraj = GameOver(2, self.PointsL)
                        self.label4.hide()
                    else:
                        self.kraj = GameOver(1, self.PointsM)
                        self.label4.hide()



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
        if isHit(self.label1, self.label3):
            self.lives1 -= 1
            self.labelLifes1.setText(str(self.lives1))
            if self.lives1 == 0:
                if self.brojIgracaJedan:
                    self.kraj = GameOver(0, self.PointsM)
                    self.label1.hide()
                else:

                    if self.lives2 <= 0 and self.lives1 != 0:
                        self.kraj = GameOver(1, self.PointsM)
                        self.label4.hide()
                    elif self.lives2 <= 0 and self.lives1 == 0:
                        self.kraj = GameOver(1, self.PointsM)
                        self.label1.hide()
                    elif self.lives1 <= 0 and self.lives2 == 0:
                        self.kraj = GameOver(2, self.PointsL)
                        self.label1.hide()
                    elif self.lives1 <= 0 and self.lives2 != 0:
                        self.kraj = GameOver(2, self.PointsL)
                        self.label1.hide()
            restartPlayer(self.label1, 1)

        if isHit(self.label3, self.label4):
            self.lives2 -= 1
            self.labelLifes2.setText(str(self.lives2))
            if self.lives2 == 0:
                self.kraj = GameOver(0, self.PointsM)
                self.label4.hide()

            restartPlayer(self.label4, 2)


    def newLevel(self):
        if self.brojIgracaJedan == 1:
            restartPlayer(self.label1, 1)
            self.trenutniNivo += 1
            self.labelLevel.setText(str(self.trenutniNivo))


        else:
            restartPlayer(self.label1, 1)
            restartPlayer(self.label4, 2)
            self.trenutniNivo += 1
            self.labelLevel.setText(str(self.trenutniNivo))

        self.barrelsMovement.die()
        self.barrelsMovement = BarrelMovement(self.barrels_speed - 0.01)
        self.barrelsMovement.barrelMovementSignal.connect(self.moveBarrels)
        self.barrelsMovement.start()


    def closeEvent(self, event):
        self.princesMovement.die()
        self.gorilaMovement.die()
        self.key_notifier.die()
        self.key_notifier2.die()
        self.barrelsMovement.die()
        self.barrelProcess.terminate()
        self.movingBarrels.die()
        self.gorilaBug.terminate()

    def shutdown(self, event):
        self.close()

    def go_to_menu(self, event):
        self.hide()
        self.menu_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow(1, 1)
    sys.exit(app.exec_())
