import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QMessageBox)
from PyQt6.QtGui import (QPixmap, QAction)
from PyQt6.QtCore import Qt


class homepage(QMainWindow):

    def __init__(self):
        super().__init__()

        # 窗口居中
        self.centralWidget()
        self.resize(1000, 500)
        self.setWindowTitle('小Q助手')

        self.initUI()


    def initUI(self):
        # 菜单栏
        menubar = self.menuBar()
        #个人中心
        file_menu = menubar.addMenu('文件')
        # 分割线
        file_menu.addSeparator()
        # 软件推出
        exitAct = QAction('退出', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(QApplication.instance().quit)
        file_menu.addAction(exitAct)

        #帮助
        help_menu = menubar.addMenu('帮助')
        # 关于展示相关信息
        about_us = QAction('关于我们', self)
        about_us.triggered.connect(self.showAbout)
        help_menu.addAction(about_us)
        help_menu.addAction(QAction('检查更新', self))
                                    
    def showAbout(self):
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


if __name__ == '__main__':
    main()