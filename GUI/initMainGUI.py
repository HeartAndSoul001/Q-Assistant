from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *
import qtawesome as qta
from IPTOOL.iptool import ip_to_subnetlist
from GUI.DIYWidgets import (IpInputWidget, SubnetsTableWidget, IPHandleWidget)

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
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.initUI()


    def initUI(self):
        font = QFont()
        font.setFamily(u"Courier")
        font.setPointSize(10)
        font.setBold(True)
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




       
        
        leftMenuBg = QToolBar(self)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, leftMenuBg)
        leftMenuBg.setMovable(False)
        leftMenuBg.setFloatable(False)
        leftMenuBg.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.setObjectName((u"导航栏"))
        # leftMenuBg.setIconSize(QSize(25,25))
        leftMenuBg.setMinimumSize(QSize(80, 0))
        leftMenuBg.setMaximumSize(QSize(120, 16777215))
        leftMenuBg.layout().setSpacing(0)

        
        # central_widget = QWidget()
        # content_label = QLabel(central_widget)
        # content_label.setText("hello!")
        # self.setCentralWidget(central_widget)


        ## IP子网计算器
        subnetTable_Button = QToolButton()
        subnetTable_Button.setFont(font)
        subnetTable_Button.setText(u"IP子网计算器")
        subnetTable_Button.setCheckable(True)
        subnetTable_Button.setIcon(qta.icon('fa.calculator'))
        subnetTable_Button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        subnetTable_Button.setFixedSize(120,50)
        # background-color: rgb(248,248,255)
        subnetTable_Button.setStyleSheet("QToolButton{border-radius:10px;}\
		QToolButton:hover{background-color: rgb(230,230,250);}\
		QToolButton:pressed{background-color: rgb(176,196,222);}\
        QToolButton:checked{background-color: rgb(176,196,222);}")
        leftMenuBg.addWidget(subnetTable_Button)
        subnetTable_Button.clicked.connect(self.showSubnetTable)


        ip_handle_button = QToolButton()
        ip_handle_button.setFont(font)
        ip_handle_button.setText(u"IP地址处理")
        ip_handle_button.setCheckable(True)
        ip_handle_button.setIcon(qta.icon('mdi.ip-network-outline'))
        ip_handle_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        ip_handle_button.setFixedSize(120,50)
        ip_handle_button.setStyleSheet("QToolButton{border-radius:10px;}\
		QToolButton:hover{background-color: rgb(230,230,250);}\
		QToolButton:pressed{background-color: rgb(176,196,222);}\
        QToolButton:checked{background-color: rgb(176,196,222);}")
        leftMenuBg.addWidget(ip_handle_button)
        ip_handle_button.clicked.connect(self.showIPHandle)
        
    


        # IP地址探测
        ip_detect_Button = QToolButton()
        ip_detect_Button.setFont(font)
        ip_detect_Button.setText(u"IP地址探测")
        ip_detect_Button.setCheckable(True)
        ip_detect_Button.setIcon(qta.icon('fa.binoculars'))
        ip_detect_Button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        ip_detect_Button.setFixedSize(120,50)
        ip_detect_Button.setStyleSheet("QToolButton{border-radius:10px;}\
		QToolButton:hover{background-color: rgb(230,230,250);}\
		QToolButton:pressed{background-color: rgb(176,196,222);}\
        QToolButton:checked{background-color: rgb(176,196,222);}")
        leftMenuBg.addWidget(ip_detect_Button)
        ip_detect_Button.clicked.connect(self.showIpDetect)

        toolbuttonGroup = QButtonGroup(self)
        toolbuttonGroup.addButton(subnetTable_Button)
        toolbuttonGroup.addButton(ip_handle_button)
        toolbuttonGroup.addButton(ip_detect_Button)
        # 设置按钮组的互斥性
        toolbuttonGroup.setExclusive(True)
        






                                    
    def showAbout(self):
        about_us = QMessageBox(self)
        about_us.setWindowTitle("关于我们")
        about_us.setWindowModality(Qt.WindowModality.ApplicationModal)
        about_us.setFont(self.font())
        # # 设置弹窗宽和高为软件尺寸的25%
        about_us.resize(int(self.width()*0.25),int(self.height()*0.3))
        about_us.setIconPixmap(QPixmap("./icons/about_us.png")
                               .scaled(int(self.width()*0.05),int(self.height()*0.08), Qt.KeepAspectRatio))
        about_us.setText("宗旨：永不加班！\n\n"
                         "作者：wzq\n\n"
                         "版本：alpha 0.0")
        about_us
        about_us.exec()


    def showSubnetTable(self):
        subnet_font = QFont()
        subnet_font.setFamily(u"Courier")
        subnet_font.setPointSize(8)
        subnet_font.setBold(True)
        subnet_font.setItalic(False)

        content_widget = QWidget()
        self.setCentralWidget(content_widget)
        content_layout = QVBoxLayout()
        content_widget.setLayout(content_layout)

        ip_input_widget = IpInputWidget(content_widget)
        subnetsTable_output_widget = SubnetsTableWidget(content_widget)
        content_layout.addWidget(ip_input_widget)
        content_layout.addWidget(subnetsTable_output_widget)
        
        ip_input_widget.ipCompleted.connect(subnetsTable_output_widget.update_table)

    def showIPHandle(self):
        ip_handle_widget = IPHandleWidget()
        # ip_handle_widget.setStyleSheet("background-color: red;")
        self.setCentralWidget(ip_handle_widget)
        

    def showIpDetect(self):
        content_widget = QWidget()
        content_label = QLabel(content_widget)
        content_label.setText("hello!sdfsfdsfdsfdsdfsfdsfsfadsfadsfasfsdf")
        self.setCentralWidget(content_widget)
        
        