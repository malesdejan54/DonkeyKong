from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot

import time
from random import randint

class BarrelMovement(QObject):
    barrelMovementSignal = pyqtSignal()

    def __init__(self, speed):
        super().__init__()
        self.speed = speed
        #self.is_done = False

        self.thread = QThread()
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.__work__)

    def start(self):
        """
        Start notifications.
        """
        self.thread.start()

    def die(self):
        """
        End notifications.
        """
        #self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        """
        A slot with no params.
        """
        while True:
            self.barrelMovementSignal.emit()
            time.sleep(self.speed)
