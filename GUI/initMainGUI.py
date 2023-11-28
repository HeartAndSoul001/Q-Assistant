from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import qtawesome as qta

class homepage(QMainWindow):

    def __init__(self):
        super().__init__()

        # 获取屏幕参数
        screen = QGuiApplication.primaryScreen().geometry()
        # 设置软件宽和高为屏幕参数的80%
        self.resize(int(screen.width()*0.8), int(screen.height()*0.8))
        # 移动软件居中
        self.move(int(screen.width()*0.1),int(screen.height()*0.1))
        self.setWindowTitle('小Q助手')

        self.initUI()


    def initUI(self):
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.setFont(font)

        # 菜单栏
        menubar = self.menuBar()
        menubar.setFont(QFont())
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
        leftMenuBg = QToolBar()
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, leftMenuBg)
        leftMenuBg.setMovable(False)
        leftMenuBg.setFloatable(True)
        leftMenuBg.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.setObjectName((u"导航栏"))
        leftMenuBg.setMinimumSize(QSize(100, 0))
        leftMenuBg.setMaximumSize(QSize(100, 16777215))
        
        ## IP地址转换
        ip_conversion = QToolButton()
        ip_conversion.setFont(font)
        ip_conversion.setText(u"IP地址转换")
        ip_conversion.setIcon(qta.icon('fa.retweet'))
        ip_conversion.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.addWidget(ip_conversion)
        # leftMenuBg.addSeparator()

        ## IP地址探测
        ip_detection = QToolButton()
        ip_detection.setFont(font)
        ip_detection.setText(u"IP地址探测")
        ip_detection.setIcon(qta.icon('fa.binoculars'))
        ip_detection.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.addWidget(ip_detection)
        # leftMenuBg.addSeparator()




        # tool_bar.addAction(qta.icon('fa.retweet'),"IP地址转换")
        # tool_bar.addSeparator()
        # tool_bar.addAction(qta.icon('fa.binoculars'),"IP地址探测")
        # tool_bar.addSeparator()


                                    
    def showAbout(self):
        about_us = QMessageBox(self)
        about_us.setWindowTitle("关于我们")
        about_us.setWindowModality(Qt.WindowModality.ApplicationModal)
        about_us.setFont(self.font())
        # 设置弹窗宽和高为软件尺寸的25%
        about_us.resize(int(self.width()*0.25),int(self.height()*0.25))
        about_us.setIconPixmap(QPixmap("./icons/about_us.png")
            .scaled(int(self.width()*0.08),int(self.height()*0.08),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation))
        about_us.setText("宗旨：永不加班！\n\n"
                         "作者：wzq\n\n"
                         "版本：alpha 0.0")
        about_us.exec()