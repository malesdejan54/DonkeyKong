from PyQt5.QtCore import QThread,QObject,pyqtSignal,pyqtSlot
from random import randint
import time


class FireMovement(QObject):
    fireMovementSignal = pyqtSignal()

    def __init__(self, show_after):
        super().__init__()
        self.thread = QThread()
        self.start_after = show_after
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
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        """
        A slot with no params.
        """
        time.sleep(self.start_after)
        while True:
            self.fireMovementSignal.emit()
            time.sleep(5)
