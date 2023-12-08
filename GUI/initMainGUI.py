from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import qtawesome as qta
from IPTOOL.iptool import ip_to_subnetlist
from GUI.DIYWidgets import IpInputWidget, SubnetsTableWidget

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

        # 工具栏
        leftMenuBg = QToolBar()
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, leftMenuBg)
        leftMenuBg.setMovable(False)
        leftMenuBg.setFloatable(False)
        leftMenuBg.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.setObjectName((u"导航栏"))
        leftMenuBg.setIconSize(QSize(25,25))
        leftMenuBg.setMinimumSize(QSize(80, 0))
        leftMenuBg.setMaximumSize(QSize(120, 16777215))

        
        central_widget = QWidget()
        content_label = QLabel(central_widget)
        content_label.setText("hello!")
        self.setCentralWidget(central_widget)


        ## IP子网计算器
        subnetTable = QToolButton()
        subnetTable.setFont(font)
        subnetTable.setText(u"IP子网计算器")
        subnetTable.setIcon(qta.icon('fa.calculator'))
        subnetTable.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.addWidget(subnetTable)
        subnetTable.clicked.connect(self.showSubnetTable)

        ## IP地址转换
        ip_convert = QToolButton()
        ip_convert.setFont(font)
        ip_convert.setText(u"IP地址转换")
        ip_convert.setIcon(qta.icon('fa.retweet'))
        ip_convert.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.addWidget(ip_convert)
        # show_IpConvert = QAction(self.ce)
        ip_convert.clicked.connect(self.showIpConvert)
        # leftMenuBg.addSeparator()

        ## IP地址探测
        ip_detect = QToolButton()
        ip_detect.setFont(font)
        ip_detect.setText(u"IP地址探测")
        ip_detect.setIcon(qta.icon('fa.binoculars'))
        ip_detect.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        leftMenuBg.addWidget(ip_detect)
        ip_detect.clicked.connect(self.showIpDetect)
        # leftMenuBg.addSeparator()







                                    
    def showAbout(self):
        about_us = QMessageBox(self)
        about_us.setWindowTitle("关于我们")
        about_us.setWindowModality(Qt.WindowModality.ApplicationModal)
        about_us.setFont(self.font())
        # # 设置弹窗宽和高为软件尺寸的25%
        about_us.resize(int(self.width()*0.25),int(self.height()*0.3))
        about_us.setIconPixmap(QPixmap("./icons/about_us.png"))
        about_us.setText("宗旨：永不加班！\n\n"
                         "作者：wzq\n\n"
                         "版本：alpha 0.0")
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
        
        # ip_input_widget.ipCompleted.connect(subnetsTable_output_widget.update_table)

    

    def showIpConvert(self):
        content_widget = QWidget()
        self.setCentralWidget(content_widget)
        content_layout = QGridLayout()
        content_widget.setLayout(content_layout)

        # ip地址输入区域1
        ipInput_box1 = QWidget()
        ipInput_box1_layout = QGridLayout()
        ipInput_box1_layout.setSpacing(10)
        ipInput_box1.setLayout(ipInput_box1_layout)
        ## ip地址多行输入框
        ipInput_tab_1 = QTextEdit()
        ## ip地址输入框功能按钮1----从剪贴板粘贴内容
        ipInput_1_button_pastefromclipboard = QPushButton(qta.icon('fa.paste'),"从剪贴板粘贴")
        ## ip地址输入框功能按钮2----清除内容
        ipInput_1_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")
        ipInput_box1_layout.addWidget(ipInput_tab_1,0,0,1,2)
        ipInput_box1_layout.addWidget(ipInput_1_button_pastefromclipboard,1,0)
        ipInput_box1_layout.addWidget(ipInput_1_button_clean,1,1)

        # ip地址输入区域2
        ipInput_box2 = QWidget()
        ipInput_box2_layout = QGridLayout()
        ipInput_box2_layout.setSpacing(10)
        ipInput_box2.setLayout(ipInput_box2_layout)
        ## ip地址多行输入框2
        ipInput_tab_2 = QTextEdit()
        ## ip地址输入框功能按钮1----从剪贴板粘贴内容
        ipInput_2_button_pastefromclipboard = QPushButton(qta.icon('fa.paste'),"从剪贴板粘贴")
        ## ip地址输入框功能按钮2----清除内容
        ipInput_2_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")
        ipInput_box2_layout.addWidget(ipInput_tab_2,0,0,1,2)
        ipInput_box2_layout.addWidget(ipInput_2_button_pastefromclipboard,1,0)
        ipInput_box2_layout.addWidget(ipInput_2_button_clean,1,1)


        # ip地址输出区域
        ipOutput_box = QWidget()
        ipOutput_box_layout = QGridLayout()
        ipOutput_box_layout.setSpacing(10)
        ipOutput_box.setLayout(ipOutput_box_layout)
        ## ip地址多行输出框
        ipOutput_tab = QTextEdit()
        ipOutput_tab.setReadOnly(True)
        ## ip地址输入框功能按钮1----复制到剪贴板
        ipOutput_button_copytoclipboard = QPushButton(qta.icon('fa.copy'),"复制内容到剪贴板")
        ## ip地址输入框功能按钮2----清除内容
        ipOutput_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")

        ipOutput_box_layout.addWidget(ipOutput_tab,0,0,1,2)
        ipOutput_box_layout.addWidget(ipOutput_button_copytoclipboard,1,0)
        ipOutput_box_layout.addWidget(ipOutput_button_clean,1,1)


        # 功能选项区域
        func_box =QWidget()
        func_box_layout = QGridLayout()
        func_box_layout.setSpacing(10)
        func_box.setLayout(func_box_layout)

        content_layout.addWidget(func_box,0,0,1,1)
        content_layout.addWidget(ipInput_box1,0,1,2,2)
        content_layout.addWidget(ipInput_box2,0,3,2,2)
        content_layout.addWidget(ipOutput_box,2,1,2,4)


        ## 功能按钮1(地址范围-->CIDR)
        iprange_to_cidr = QPushButton()
        iprange_to_cidr.setText("地址范围 --> CIDR")
        ## 功能按钮2(CIDR-->地址范围)
        cidr_to_iprange = QPushButton()
        cidr_to_iprange.setText("CIDR --> 地址范围")
        ## 功能按钮3(IP地址集合--交集)
        ipset_And = QPushButton()
        ipset_And.setText("IP地址集合--交集")
        ## 功能按钮4(IP地址集合--并集)
        ipset_Or = QPushButton()
        ipset_Or.setText("IP地址集合--并集")
        ## 功能按钮5(IP地址集合--差集)
        ipset_Not = QPushButton()
        ipset_Not.setText("IP地址集合--差集")

        func_box_layout.addWidget(iprange_to_cidr,0,0)
        func_box_layout.addWidget(cidr_to_iprange,1,0)
        func_box_layout.addWidget(ipset_And,2,0)
        func_box_layout.addWidget(ipset_Or,3,0)
        func_box_layout.addWidget(ipset_Not,4,0)

    def showIpDetect(self):
        content_widget = QWidget()
        content_label = QLabel(content_widget)
        content_label.setText("hello!sdfsfdsfdsfdsdfsfdsfsfadsfadsfasfsdf")
        self.setCentralWidget(content_widget)