from PyQt5.QtCore import QStringListModel, Qt
from PyQt5.QtGui import QIcon, QPalette, QColor, QCursor
from PyQt5.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QFontComboBox,
                             QPushButton, QSizePolicy,
                             QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QListView, QSplitter, QAction, QMainWindow, QDialog)

from java_code_view import PyJavaCode
from jmethod import PyJavaMethod


class KOWRaidEditor(QMainWindow):
    def __init__(self):
        super(KOWRaidEditor, self).__init__()

        self.setWindowTitle("Raid Editor v0.1")
        self.setGeometry(100, 100, 960, 640)

        # todo: file import/export system 추가 필요
        self.init_ui()

        self._methods = []
        self._popup = QDialog()

        # test
        self.test_data()

        #
        self.__top_splitter = self.create_top_group_box()
        self.__top_splitter.setStretchFactor(1, 1)

        #
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.__top_splitter)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def test_data(self):
        self._methods.append(PyJavaMethod("test1", "sfsfsfs"))
        self._methods.append(PyJavaMethod("test2", "gasdfwqerasdf"))
        self._methods.append(PyJavaMethod("test3", "basdfinerlih"))
        self._methods.append(PyJavaMethod("test4", "gqwerasdf\nqfwe"))
        self._methods.append(PyJavaMethod("test5",
                                          "sfsfsfs\nhgqwrgaswwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwdf\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhgqw\nhg3qw\nhgq412w"))

    def init_ui(self):
        # menu bar
        act_newfile = QAction(QIcon('newfile.png'), '새로운 기사', self)
        act_newfile.setShortcut('Ctrl+N')
        act_newfile.setStatusTip('Create New File')
        #act_newfile.triggered.connect(self.new_windows)
        # todo: link action creating new document

        act_openfile = QAction(QIcon('openfile.png'), '기사 불러오기', self)
        act_openfile.setShortcut('Ctrl+O')
        act_openfile.setStatusTip('Open Existing Article')

        act_savefile = QAction(QIcon('savefile.png'), '기사 저장하기', self)
        act_savefile.setShortcut('Ctrl+S')
        act_savefile.setStatusTip('Save Current Article')

        act_export = QAction(QIcon('export.png'), '&Export', self)
        act_export.setShortcut('Ctrl+E')
        act_export.setStatusTip('Export to Java SourceCode')
        act_export.triggered.connect(self.export_java)

        act_import = QAction(QIcon('import.png'), '&Import', self)
        act_import.setShortcut('Ctrl+I')
        act_import.setStatusTip('Import lua code')
        act_import.triggered.connect(self.import_lua)

        status_bar = self.statusBar()
        status_bar.showMessage('글자 수 표시 장소')
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)
        print(menu_bar.height())

        menu_file = menu_bar.addMenu('&File')
        menu_file.addAction(act_newfile)
        menu_file.addAction(act_openfile)
        menu_file.addAction(act_export)
        menu_file.addAction(act_import)

        #tool bar
        fontbox = QFontComboBox(self)
        fontbox.InsertPolicy()
        fontbox.setMinimumContentsLength(3)

        format_bar = self.addToolBar('Format')
        format_bar.addAction(act_newfile)
        format_bar.addAction(act_openfile)
        format_bar.addAction(act_savefile)
        format_bar.addSeparator()
        format_bar.addWidget(fontbox)

    def import_lua(self):
        return

    def export_java(self):
        return

    def create_top_group_box(self):
        top_splitter = QSplitter()
        top_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 좌
        top_left_group_box = QGroupBox("레이드 함수 목록")
        top_left_group_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        names = list(map(lambda i: i.get_name(), self._methods))
        model = QStringListModel(names)
        view = QListView()
        view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        view.setModel(model)
        view.clicked.connect(self.on_show_method)

        add_function = QPushButton("함수 추가")

        layout = QVBoxLayout()
        layout.addWidget(add_function)
        layout.addWidget(view)

        top_left_group_box.setLayout(layout)

        # 우
        top_right_group_box = QGroupBox("레이드 함수")

        # 우 - 텍스트
        tab_method_body = QTabWidget()

        tab_block = QWidget()

        tab_plain = QWidget()
        self._edit_method_body_plain = QTextEdit()
        tab_hbox_plain = QHBoxLayout()
        tab_hbox_plain.setContentsMargins(5, 5, 5, 5)
        tab_hbox_plain.addWidget(self._edit_method_body_plain)

        self._edit_method_body_block = PyJavaCode()
        self._edit_method_body_block.set_plain_view(self._edit_method_body_plain)
        tab_hbox_block = QHBoxLayout()
        tab_hbox_block.setContentsMargins(5, 5, 5, 5)
        tab_hbox_block.addWidget(self._edit_method_body_block)

        tab_block.setLayout(tab_hbox_block)
        tab_plain.setLayout(tab_hbox_plain)

        tab_method_body.addTab(tab_block, "&Block")
        tab_method_body.addTab(tab_plain, "&Plain")

        # 배치
        label_method_name = QLabel("name")
        self._edit_method_name = QLineEdit()
        label_method_body = QLabel("body")
        self._edit_method_body = tab_method_body

        #
        layout = QVBoxLayout()
        layout.addWidget(label_method_name)
        layout.addWidget(self._edit_method_name)
        layout.addWidget(label_method_body)
        layout.addWidget(self._edit_method_body)

        top_right_group_box.setLayout(layout)

        # test
        # top_left_group_box.setStyleSheet("color: blue;"
        #                       "background-color: #87CEFA;"
        #                       "border-style: dashed;"
        #                       "border-width: 3px;"
        #                       "border-color: #1E90FF")
        #
        # top_right_group_box.setStyleSheet("color: blue;"
        #                       "background-color: #87CEFA;"
        #                       "border-style: dashed;"
        #                       "border-width: 3px;"
        #                       "border-color: #1E90FF")

        # spliter
        top_splitter.addWidget(top_left_group_box)
        top_splitter.addWidget(top_right_group_box)

        return top_splitter

    def on_show_method(self, index):
        method = self._methods[index.row()]
        self._edit_method_name.setText(method.get_name())

        self.plain_to_block(method.get_body())
        self._edit_method_body_plain.setText(method.get_body())

        #
        pos_x = QCursor.pos().x() - self.pos().x()
        pos_y = QCursor.pos().y() - self.pos().y() - 30

        if self._popup:
            self._popup.hide()

        # self._popup = method.display_overlay(self, pos_x, pos_y)

    def plain_to_block(self, plain):
        self._edit_method_body_block.clear_widgets()

        for row in plain.split('\n'):
            self._edit_method_body_block.append_plain(row)


if __name__ == '__main__':
    import sys

    #
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Now use a palette to switch to dark colors:
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)

    #
    editor = KOWRaidEditor()
    editor.show()
    sys.exit(app.exec_())
