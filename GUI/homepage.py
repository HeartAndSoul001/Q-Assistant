import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class homepage(QMainWindow):

    def __init__(self):
        super().__init__()

        # 窗口居中
        self.centralWidget()
        self.resize(1280, 720)
        self.setMinimumSize(QSize(940, 560))
        self.setWindowTitle('小Q助手')
        self.setWindowIcon(QIcon("./icons/about_us.png"))
        # 背景颜色
        self.initUI()


    def initUI(self):
        # 菜单栏
        menubar = self.menuBar()
            #文件
        file_menu = menubar.addMenu('文件')
            # 分割线
        file_menu.addSeparator()
            # 软件退出
        exitAct = QAction('退出', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exitAct)
            #帮助
        help_menu = menubar.addMenu('帮助')
            # 关于展示相关信息
        about_us = QAction('关于我们', self)
        about_us.triggered.connect(self.show_About_us)
        help_menu.addAction(about_us)
        help_menu.addAction(QAction('检查更新', self))

        # 创建窗口主部件
        self.main_widget = QWidget(self)
        self.main_layout = QGroupBox(self.main_widget)
        self.main_layout.setCheckable(True)
        self.main_layout.setChecked(False)
        self.toggle_button = QPushButton("展开")
        self.toggle_button.clicked.connect(self.on_toggled)

        self.content_area = QVBoxLayout()
        self.main_layout.setLayout(self.content_area)

    def on_toggled(self, checked):
        if checked:
            self.toggle_button.setText("折叠")
            self.content_area.show()
        else:
            self.toggle_button.setText("展开")
            self.content_area.hide()
        


                                    
    def show_About_us(self):
        about_us = QMessageBox(self)
        about_us.setModal(True)
        about_us.setWindowTitle("关于我们")
        about_us.setWindowModality(Qt.WindowModality.ApplicationModal)
        about_us.resize(300,300)
        about_us_icon = QPixmap("./icons/about_us.png")
        about_us.setIconPixmap(about_us_icon)
        about_us.setText("宗旨：永不加班！！！\n\n"
                         "作者：魏兆卿\n\n"
                         "版本：alpha 0.0")
        about_us.exec()


def main():

    app = QApplication(sys.argv)
    ex = homepage()
    ex.show()
    sys.exit(app.exec())
