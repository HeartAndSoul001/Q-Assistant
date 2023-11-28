import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class homepage(QMainWindow):

    def __init__(self):
        super().__init__()

        # 窗口居中
        self.centralWidget()
        self.resize(1280, 800)
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

        # 工具栏
        tool_bar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, tool_bar)
        tool_bar.setMovable(False)
        tool_bar.setFloatable(True)
        tool_bar.addSeparator()
        tool_bar.setStyleSheet('''QWidget{background-color:#FFFF00;}''')

        ## ip地址处理
        ip_handle_widget = QWidget()
        ip_handle_layout = QVBoxLayout()
        ip_handle_widget.setLayout(ip_handle_layout)
        ip_handle_text_widget = QWidget()
        ip_handle_text_label = QLabel(ip_handle_text_widget)
        ip_handle_text_label.setText("IP地址处理")
        ip_handle_icon_widget = QWidget()
        ip_handle_icon_label = QLabel(ip_handle_icon_widget)
        ip_handle_icon_label.setPixmap(QPixmap("./icons/ipHandle.png"))
        ip_handle_layout.addChildWidget(ip_handle_icon_widget)
        ip_handle_layout.addChildWidget(ip_handle_text_widget)
                                    
    def showAbout(self):
        about_us = QMessageBox(self)
        about_us.setWindowTitle("关于我们")
        about_us.setWindowModality(Qt.WindowModality.ApplicationModal)
        about_us.resize(800,600)
        about_us.setIconPixmap(QPixmap("./icons/about_us.png"))
        about_us.setText("宗旨：永不加班！\n\n"
                         "作者：wzq\n\n"
                         "版本：alpha 0.0")
        about_us.exec()


def main():

    app = QApplication(sys.argv)
    ex = homepage()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()