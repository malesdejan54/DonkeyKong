import time
from random import randint


def isHit(first, second):
    rec1 = first.geometry()
    y1 = first.height()
    x1 = first.width()

    rec2 = second.geometry()
    x2 = second.width()
    y2 = second.height()

    if rec1.x() in range(rec2.x(), rec2.x() + x2):
        if rec1.y() in range(rec2.y(), rec2.y() + y2):
            return True
        elif rec1.y() + y1 in range(rec2.y(), rec2.y() + y2):
            return True

    if rec1.x() + x1 in range(rec2.x(), rec2.x() + x2):
        if rec1.y() in range(rec2.y(), rec2.y() + y2):
            return True
        elif rec1.y() + y1 in range(rec2.y(), rec2.y() + y2):
            return True






def restartPlayer(label, p):
    if p == 1:
        label.setGeometry(250, 460, 36, 50)
    else:
        label.setGeometry(730, 436, 75, 100)
