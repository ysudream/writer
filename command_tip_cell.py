from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel


class CommandTipCell(QPushButton):
    def __init__(self, *__args):
        super(CommandTipCell, self).__init__(*__args)
        self.setMinimumSize(196, 48)

    def set_content(self, title, desc):
        self.setText("")

        #
        inner = QVBoxLayout()
        inner.setSpacing(0)

        #
        title = QLabel(title)
        title.setStyleSheet("color: white; font-size: 10pt;")
        inner.addWidget(title)

        #
        desc = QLabel(desc)
        desc.setStyleSheet("color: gray; font-size: 10px; font-weight:100;")
        inner.addWidget(desc)

        self.setLayout(inner)

        return self
