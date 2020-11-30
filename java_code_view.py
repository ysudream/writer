from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QFontMetrics
from PyQt5.QtWidgets import QScrollArea, QVBoxLayout, QWidget, QTextEdit, QDialog

from overlay import OverlayTip, Overlay, OverlayUnit


class PyJavaCode(QScrollArea):
    def __init__(self, parent=None):
        super(PyJavaCode, self).__init__(parent)

        self.__plain: QTextEdit = None

        layout = QVBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        layout.setAlignment(Qt.AlignTop)

        self._widget = QWidget()
        self._widget.setLayout(layout)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self._widget)

    def set_plain_view(self, text: QTextEdit):
        self.__plain = text

    def parse_plain(self):
        if self.__plain is None:
            return

        str_list = []
        max = self._widget.layout().count()
        for i in range(0, max):
            widget: PyJavaCodeBlock = self._widget.layout().itemAt(i).widget()
            str_list.append(widget.toPlainText())

        self.__plain.setText('\n'.join(str_list))

    def resizeEvent(self, event):
        print(self.size())
        print("resize")

        max = self._widget.layout().count()
        for i in range(0, max):
            widget = self._widget.layout().itemAt(i).widget()
            widget.resized(self.size().width())

    def get_total_count(self):
        return self._widget.layout().count()

    def get_block(self, row):
        total = self._widget.layout().count()
        verified = min([total - 1, max([0, row])])
        block = self._widget.layout().itemAt(verified).widget()

        return block

    def remove_plain(self, row):
        qvbox: QVBoxLayout = self._widget.layout()
        block = self._widget.layout().itemAt(row).widget()
        qvbox.removeWidget(block)

        self.renumber_rows()

    def insert_plain(self, plain, row):
        block = PyJavaCodeBlock(self)
        block.setText(plain)

        #
        qvbox: QVBoxLayout = self._widget.layout()
        qvbox.insertWidget(row, block)

        self.renumber_rows()

        return block

    def append_plain(self, plain):
        block = PyJavaCodeBlock(self)
        block.setText(plain)

        row_count = self._widget.layout().count()
        block.set_index(row_count)

        self._widget.layout().addWidget(block)

        return block

    def renumber_rows(self):
        row_count = self._widget.layout().count()
        for i in range(0, row_count):
            widget = self._widget.layout().itemAt(i).widget()
            widget.set_index(i)
            widget.resized(self.size().width())

    def clear_widgets(self):
        while self._widget.layout().count() > 0:
            item = self._widget.layout().takeAt(0)

            if not item:
                continue

            w = item.widget()
            if w:
                w.deleteLater()


class PyJavaCodeBlock(QTextEdit):
    overlay: QDialog = None
    command_pos: int = 0

    def __init__(self, parent, *args, **kwargs):
        super(PyJavaCodeBlock, self).__init__(*args, **kwargs)

        # private
        self.__parent: PyJavaCode = parent

        # protected
        self._max_width = 1000
        self._first_released = False
        self._index = 0
        self._key_pressed = set()

        # public
        self.document().contentsChanged.connect(self.size_changed)
        self.document().contentsChanged.connect(self.__parent.parse_plain)
        self.textChanged.connect(self.text_changed)

        self.heightMin = 40
        self.heightMax = 65000

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setReadOnly(True)
        self.setStyleSheet("background-color: #00000000;")

    def keyReleaseEvent(self, event):
        if self._first_released:
            self.process_multi_keys(self._key_pressed)

        if event.key() in self._key_pressed:
            self._key_pressed.remove(event.key())

        self._first_released = False

    def process_multi_keys(self, key_set: set):
        if Qt.Key_Return in key_set and Qt.Key_Shift in key_set and len(key_set) == 2:
            self.append("")

    def keyPressEvent(self, event):
        self._first_released = True
        self._key_pressed.add(event.key())

        if Qt.Key_Shift not in self._key_pressed:
            if event.key() == Qt.Key_Return:
                p: PyJavaCode = self.__parent
                new = p.insert_plain("", self._index + 1)
                new.setFocus()
                return

            if event.key() == Qt.Key_Backspace:
                if self.textCursor().position() == 0:
                    if self._index == 0:
                        return

                    p: PyJavaCode = self.__parent
                    index = self._index
                    prev_block: PyJavaCodeBlock = p.get_block(index - 1)
                    if index - 1 >= 0:
                        self.insertPlainText(prev_block.toPlainText())
                        p.remove_plain(index - 1)

                    return

            if event.key() == Qt.Key_Up:
                if self._index == 0:
                    return

                p: PyJavaCode = self.__parent
                prev_block: PyJavaCodeBlock = p.get_block(self._index - 1)
                prev_block.setFocus()
                return

            if event.key() == Qt.Key_Down:
                p: PyJavaCode = self.__parent
                if self._index == p.get_total_count() - 1:
                    return

                next_block: PyJavaCodeBlock = p.get_block(self._index + 1)
                next_block.setFocus()
                return

        super(PyJavaCodeBlock, self).keyPressEvent(event)

    def focusInEvent(self, event):
        self.setReadOnly(False)
        self.setStyleSheet("background-color: #ff000000;")

        super(PyJavaCodeBlock, self).focusInEvent(event)

        PyJavaCodeBlock.hide_overlay()

    def focusOutEvent(self, event):
        self.setReadOnly(True)
        self.setStyleSheet("background-color: #00000000;")

        super(PyJavaCodeBlock, self).focusOutEvent(event)

        # PyJavaCodeBlock.hide_overlay()

    def get_widget(self):
        text = QTextEdit()
        text.setText(self.__plain)

        return text

    def text_changed(self):
        plain = self.toPlainText()
        if len(plain) <= 0:
            PyJavaCodeBlock.hide_overlay()
            return

        self.do_command(plain)

    def do_command(self, plain):
        if PyJavaCodeBlock.overlay:
            return

        #
        if "/unit" in plain.split(' '):
            PyJavaCodeBlock.hide_overlay()
            PyJavaCodeBlock.overlay = TipCommand.display_unit(self,
                                                              self.__parent,
                                                              self.pos().x(),
                                                              self.pos().y() + self.size().height() + 10)
        elif "/blackboard" in plain.split(' '):
            PyJavaCodeBlock.hide_overlay()
            PyJavaCodeBlock.overlay = TipCommand.display_blackboard(self,
                                                                    self.__parent,
                                                                    self.pos().x(),
                                                                    self.pos().y() + self.size().height() + 10)
        elif '/' in plain.split(' '):
            PyJavaCodeBlock.hide_overlay()
            PyJavaCodeBlock.overlay = TipCommand.display_default(self,
                                                                 self.__parent,
                                                                 self.pos().x(),
                                                                 self.pos().y() + self.size().height() + 10)

    @staticmethod
    def hide_overlay():
        if PyJavaCodeBlock.overlay:
            PyJavaCodeBlock.overlay.hide()
            PyJavaCodeBlock.overlay = None

    def size_changed(self):
        font = self.document().defaultFont()
        fontMetrics = QFontMetrics(font)
        textSize = fontMetrics.size(0, self.toPlainText())

        w = textSize.width() + 10
        row_count = 1
        while w > self._max_width:
            row_count += 1
            w -= self._max_width

        h = (textSize.height() + 4) * row_count + 4

        self.setMinimumSize(w, h)
        self.setMaximumSize(self._max_width, h)
        self.resize(self._max_width, h)

        self.contentsMargins().setLeft(10)
        self.contentsMargins().setRight(10)

    def set_index(self, index):
        self._index = index

    def resized(self, width):
        self._max_width = width
        self.size_changed()

    def set_cursor_end(self):
        prev = self.textCursor().position()
        self.textCursor().setPosition(len(self.document().toRawText()))
        now = self.textCursor().position()

        print(prev)
        print(len(self.document().toRawText()))
        print(now)


class TipCommand:
    @staticmethod
    def display_default(block: PyJavaCodeBlock, parent: QWidget, pos_x, pos_y):
        popup = Overlay(parent, OverlayTip(None, lambda: TipCommand.on_tip_unit(block),
                                           lambda: TipCommand.on_tip_bb(block),
                                           lambda: TipCommand.on_tip_int(block),
                                           lambda: TipCommand.on_tip_float(block),
                                           lambda: TipCommand.on_tip_if(block),
                                           lambda: TipCommand.on_tip_for(block)
                                           ))
        popup.setGeometry(pos_x, pos_y, popup.size().width(), popup.size().height())
        popup.show()
        popup.widget.setFocus()

        return popup

    @staticmethod
    def display_unit(block: PyJavaCodeBlock, parent: QWidget, pos_x, pos_y):
        popup = Overlay(parent, OverlayUnit(None, block))
        popup.setGeometry(pos_x, pos_y, popup.size().width(), popup.size().height())
        popup.show()
        popup.widget.setFocus()

        return popup

    @staticmethod
    def display_blackboard(block: PyJavaCodeBlock, parent: QWidget, pos_x, pos_y):
        popup = Overlay(parent, OverlayTip(None, lambda: TipCommand.on_tip_unit(),
                                           lambda: TipCommand.on_tip_bb(),
                                           lambda: TipCommand.on_tip_int(block),
                                           lambda: TipCommand.on_tip_float(block),
                                           lambda: TipCommand.on_tip_if(block),
                                           lambda: TipCommand.on_tip_for(block)
                                           ))
        popup.setGeometry(pos_x, pos_y, popup.size().width(), popup.size().height())
        popup.show()
        popup.widget.setFocus()

        return popup

    @staticmethod
    def on_tip_unit(text):
        text.hide_overlay()
        # TipCommand.display_unit()

    @staticmethod
    def on_tip_bb(text):
        cursor = text.textCursor()
        cursor.setPosition(PyJavaCodeBlock.command_pos)
        cursor.setPosition(len(text.document().toRawText()), QTextCursor.KeepAnchor)

        print(cursor.selectedText())
        cursor.removeSelectedText()

        text.insertPlainText("int 변수이름 = 0;")
        cursor.setPosition(len(text.document().toRawText()))

        text.hide_overlay()

    @staticmethod
    def on_tip_int(text: PyJavaCodeBlock):
        cursor = text.textCursor()
        cursor.setPosition(PyJavaCodeBlock.command_pos)
        cursor.setPosition(len(text.document().toRawText()), QTextCursor.KeepAnchor)

        print(cursor.selectedText())
        cursor.removeSelectedText()

        text.insertPlainText("int 변수이름 = 0;")
        cursor.setPosition(len(text.document().toRawText()))

        text.hide_overlay()

    @staticmethod
    def on_tip_float(text: PyJavaCodeBlock):
        cursor = text.textCursor()
        cursor.setPosition(PyJavaCodeBlock.command_pos)
        cursor.setPosition(len(text.document().toRawText()), QTextCursor.KeepAnchor)

        print(cursor.selectedText())
        cursor.removeSelectedText()

        text.insertPlainText("float 변수이름 = 0.0f;")
        cursor.setPosition(len(text.document().toRawText()))

        text.hide_overlay()

    @staticmethod
    def on_tip_if(text: PyJavaCodeBlock):
        cursor = text.textCursor()
        cursor.setPosition(PyJavaCodeBlock.command_pos)
        cursor.setPosition(len(text.document().toRawText()), QTextCursor.KeepAnchor)

        print(cursor.selectedText())
        cursor.removeSelectedText()

        text.insertPlainText("if (조건 == true) {\n\n} else if (또 다른 조건) {\n\n} else {\n\n}")
        cursor.setPosition(len(text.document().toRawText()))

        text.hide_overlay()

    @staticmethod
    def on_tip_for(text: PyJavaCodeBlock):
        cursor = text.textCursor()
        cursor.setPosition(PyJavaCodeBlock.command_pos)
        cursor.setPosition(len(text.document().toRawText()), QTextCursor.KeepAnchor)

        print(cursor.selectedText())
        cursor.removeSelectedText()

        text.insertPlainText("for (변수 = 초기값; 종료 조건; 반복 조건) {\n\n}")
        cursor.setPosition(len(text.document().toRawText()))

        text.hide_overlay()
