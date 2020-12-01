from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QPainter, QPainterPath, QRegion, QPen
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QScrollArea, QLabel, QTextEdit

from command_tip_cell import CommandTipCell


class OverlayTip(QScrollArea):
    def __init__(self, parent=None, *args):
        super(OverlayTip, self).__init__(parent)

        self.__buttons = []

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 20, 5)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        #
        label_var = QLabel("정보 가져오기")
        label_var.setMargin(10)
        layout.addWidget(label_var)

        # https://docs.google.com/spreadsheets/d/1_A_-5kjsyE5Fmd8882MKfkj0g_WiMcU9A9RpHKDMAbM/edit#gid=0
        tip_unit = CommandTipCell().set_content("unit", "unit의 함수 접근")
        tip_unit.clicked.connect(args[0])
        layout.addWidget(tip_unit)
        self.__buttons.append(tip_unit)
        tip_bb = CommandTipCell().set_content("blackboard", "blackboard의 값 접근")
        tip_bb.clicked.connect(args[1])
        layout.addWidget(tip_bb)
        self.__buttons.append(tip_bb)

        #
        label_var = QLabel("변수 선언")
        label_var.setMargin(10)
        layout.addWidget(label_var)

        tip_int = CommandTipCell().set_content("정수", "int")
        tip_int.clicked.connect(args[2])
        layout.addWidget(tip_int)
        self.__buttons.append(tip_int)
        tip_float = CommandTipCell().set_content("소수", "float")
        tip_float.clicked.connect(args[3])
        layout.addWidget(tip_float)
        self.__buttons.append(tip_float)

        #
        label_iter = QLabel("조건문 선언")
        label_iter.setMargin(10)
        layout.addWidget(label_iter)

        btn_if = CommandTipCell().set_content("if", "if ~ else if ~ else")
        btn_if.clicked.connect(args[4])
        layout.addWidget(btn_if)
        self.__buttons.append(btn_if)

        #
        label_iter = QLabel("반복문 선언")
        label_iter.setMargin(10)
        layout.addWidget(label_iter)

        btn_for = CommandTipCell().set_content("for", "지정한 횟수만큼 반복")
        btn_for.clicked.connect(args[5])
        layout.addWidget(btn_for)
        self.__buttons.append(btn_for)

        self._widget = QWidget()
        self._widget.setLayout(layout)
        self._focused_button_index = 0

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setWidgetResizable(True)
        self.setWidget(self._widget)

        #
        self.__buttons[self._focused_button_index].setFocus()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Up:
            self._focused_button_index = max(0, self._focused_button_index - 1)
        elif event.key() == Qt.Key_Down:
            self._focused_button_index = min(len(self.__buttons) - 1, self._focused_button_index + 1)
        elif event.key() == Qt.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key_Return:
            button: QPushButton = self.__buttons[self._focused_button_index]
            button.animateClick()
            return

        self.__buttons[self._focused_button_index].setFocus()

    def get_total_count(self):
        return self._widget.layout().count()


class OverlayUnit(QScrollArea):
    def __init__(self, parent=None, *args):
        super(OverlayUnit, self).__init__(parent)

        self.__buttons = []
        getter = ["getHP", "getMaxHP", "getDataId", "getUnitID", "getTarget", "getField", "getJumpTimer",
                  "getDirection", "getDirectionInt", "getLevel"]
        setter = ["setCustomSkill", "addBuff", "removeBuff", "setAnimationTrigger", "setAnimationKey",
                  "addBasicAttackSkill", "setJumpToPos", "setDir4ToTarget", "addHP"]
        is_func = ["isUsableBasicAttack", "isUsableSkill", "hasBuff", "isDead"]
        others = ["useSkill", "doSkillCoolTime", "clearBasicAttackSkill", "boxCast", "stopMoving", "leaveField"]

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 20, 5)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        #
        block: QTextEdit = args[0]

        #
        label_var = QLabel("getter")
        label_var.setMargin(10)
        layout.addWidget(label_var)
        for name in getter:
            bt_tip = CommandTipCell().set_content(name, name)
            bt_tip.clicked.connect(lambda: block.insertPlainText(name))
            layout.addWidget(bt_tip)
            self.__buttons.append(bt_tip)

        #
        label_var = QLabel("setter")
        label_var.setMargin(10)
        layout.addWidget(label_var)
        for name in setter:
            bt_tip = CommandTipCell().set_content(name, name)
            bt_tip.clicked.connect(lambda: block.insertPlainText(name))
            layout.addWidget(bt_tip)
            self.__buttons.append(bt_tip)

        #
        label_var = QLabel("is_func")
        label_var.setMargin(10)
        layout.addWidget(label_var)
        for name in is_func:
            bt_tip = CommandTipCell().set_content(name, name)
            bt_tip.clicked.connect(lambda: block.insertPlainText(name))
            layout.addWidget(bt_tip)
            self.__buttons.append(bt_tip)

        #
        label_var = QLabel("others")
        label_var.setMargin(10)
        layout.addWidget(label_var)
        for name in others:
            bt_tip = CommandTipCell().set_content(name, name)
            bt_tip.clicked.connect(lambda: block.insertPlainText(name))
            layout.addWidget(bt_tip)
            self.__buttons.append(bt_tip)

        #
        self._widget = QWidget()
        self._widget.setLayout(layout)
        self._focused_button_index = 0

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setWidgetResizable(True)
        self.setWidget(self._widget)

        #
        self.__buttons[self._focused_button_index].setFocus()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Up:
            self._focused_button_index = max(0, self._focused_button_index - 1)
        elif event.key() == Qt.Key_Down:
            self._focused_button_index = min(len(self.__buttons) - 1, self._focused_button_index + 1)
        elif event.key() == Qt.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key_Return:
            button: QPushButton = self.__buttons[self._focused_button_index]
            button.animateClick()
            return

        self.__buttons[self._focused_button_index].setFocus()

    def get_total_count(self):
        return self._widget.layout().count()


class CtmWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.button = QPushButton("Close Overlay")
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.button)

        self.button.clicked.connect(self.hide_overlay)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()), 10, 10)
        mask = QRegion(path.toFillPolygon().toPolygon())
        pen = QPen(Qt.white, 1)
        painter.setPen(pen)
        painter.fillPath(path, Qt.white)
        painter.drawPath(path)
        painter.end()

    def hide_overlay(self):
        self.parent().hide()


class Overlay(QWidget):
    def __init__(self, parent, widget: QWidget):
        QWidget.__init__(self, parent)
        #
        # #
        # palette = QPalette(self.palette())
        # palette.setColor(palette.Background, Qt.transparent)
        # self.setPalette(palette)

        self.widget = widget
        self.widget.setParent(self)
        self.widget.resize(196 + 25, parent.height() / 2 - 40)

        w: QWidget = self.widget
        self.resize(w.size())

    #
    # def paintEvent(self, event):
    #     painter = QPainter()
    #     painter.begin(self)
    #     painter.setRenderHint(QPainter.Antialiasing)
    #     painter.fillRect(event.rect(), QBrush(QColor(0, 0, 0, 127)))
    #     painter.end()

    # def resizeEvent(self, event):
    #     position_x = (self.frameGeometry().width()-self.widget.frameGeometry().width())/2
    #     position_y = (self.frameGeometry().height()-self.widget.frameGeometry().height())/2
    # 
    #     self.widget.move(position_x, position_y)
    #     event.accept()
