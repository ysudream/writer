from PyQt5.QtGui import QCursor

from overlay import Overlay, CtmWidget


class PyJavaMethod:
    def __init__(self, name, plain):
        self._name = name
        self._plain = plain

    def get_name(self):
        return self._name

    def get_body(self):
        return self._plain

    def display_overlay(self, parent, pos_x, pos_y):
        popup = Overlay(parent, CtmWidget())

        # pos = QPoint(pos_x, pos_y)
        # self._popup.setGeometry(pos)
        popup.setGeometry(pos_x, pos_y, 320, 40)
        popup.show()

        return popup

