import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QDialog)
from PyQt6.QtGui import (QIcon, QAction)


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
        about_us = QDialog(self)


def main():

    app = QApplication(sys.argv)
    ex = homepage()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()