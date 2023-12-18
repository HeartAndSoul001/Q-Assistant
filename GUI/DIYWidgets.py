from PySide6.QtCore import (Qt, QEvent, QRegularExpression, Signal, QMimeData)
from PySide6.QtWidgets import (QWidget, QLineEdit, QHBoxLayout, QLabel, QAbstractItemView, 
                               QTableWidget, QHeaderView, QTableWidgetItem, QToolTip, QTabWidget, 
                               QGridLayout, QTextEdit, QPushButton, QVBoxLayout,QMessageBox,QPlainTextEdit)
from PySide6.QtGui import (QRegularExpressionValidator,QClipboard,QTextOption)
from IPTOOL.iptool import (ip_to_subnetlist,iprangeStr_To_cidrStr,cidrStr_To_iprangeStr,ipsetStr_and,ipsetStr_or,ipsetStr_not)
from GUI.initMainGUI import (QApplication)
import qtawesome as qta


# IP地址输入框
class IpInputWidget(QWidget):
    # 定义ipv4地址的4个段
    ip = ["192","168","0","1"]
    # 定义ipv4地址某一段的校验正则
    ip_validator = QRegularExpressionValidator(QRegularExpression("((2[0-4]\d)|(25[0-5])|(1\d{2})|(\d{1,2}))"))

    # 是否输入完成
    ipCompleted = Signal(str)


    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # 创建四个 QLineEdit 分别用于输入 IPv4 地址的四个段
        self.segment_inputs = [QLineEdit() for _ in range(4)]

        for index, input_field in enumerate(self.segment_inputs):
            input_field.setMaxLength(3)  # 设置最大长度为3
            input_field.setValidator(self.ip_validator)
            input_field.setPlaceholderText(self.ip[index])  # 设置初始字段
            input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
            # 修改点击输入框的时候自动调整为拉丁文输入法
            input_field.setInputMethodHints(Qt.InputMethodHint.ImhLatinOnly)
            input_field.installEventFilter(self)  
            


            layout.addWidget(input_field)

            if index < 3:
                # 在每两个输入框之间添加一个点，用 QLabel 实现
                dot_label = QLabel(".")
                dot_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(dot_label)

        self.setLayout(layout)

    def eventFilter(self, obj, event):
        index = self.segment_inputs.index(obj)
        # 如果按下的键是点字符 '.', 移动焦点到下一个输入框
        if index < 3 and event.type() == QEvent.Type.KeyPress and event.text() == ".":
            self.segment_inputs[index + 1].setFocus()

        # 如果按下的键是回车键，清除当前输入框的焦点
        elif index == 3 and event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Return:
            self.segment_inputs[index].clearFocus()

        # 如果所有输入框都已经输入内容，检查是否全部失去焦点
        if all(input_field.text() for input_field in self.segment_inputs):
            all_inputs_lost_focus = all(not input_field.hasFocus() for input_field in self.segment_inputs)
            if all_inputs_lost_focus:
                ip_address = ".".join(input_field.text() for input_field in self.segment_inputs)
                self.ipCompleted.emit(ip_address)
        
        return super().eventFilter(obj, event)
    


# class IpLineEdit(QLineEdit):
#     pass


# 子网显示框
class SubnetsTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        
        self.setRowCount(33)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['子网前缀','子网掩码','反掩码','地址范围','子网id','广播地址','地址数量'])
        self.horizontalHeader().setStyleSheet("QHeaderView::section{background:grey;}")
        self.setShowGrid(False)
        self.verticalHeader().setHidden(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)     
        # 设置单元格被选中以后的背景颜色
        self.setStyleSheet("QTableWidget::item:selected { background-color: lightblue; }")
        # 设置默认显示信息
        self.update_table("192.168.0.1")
        # 设置捕捉双击事件
        self.itemDoubleClicked.connect(self.copyContentToClipboard)
        
    # 根据输入地址进行实时显示子网
    def update_table(self, ip_address):
        subnetsTableList = ip_to_subnetlist(ip_address)
        for i in range(0,32):
            for j in range(0,7):
                item = QTableWidgetItem(subnetsTableList[i][j])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(i,j,item)
        
    # 捕捉双击事件，将内容复制到剪贴板
    def copyContentToClipboard(self, item):
        # 捕捉双击事件，将内容复制到剪贴板
        clipboard = QApplication.clipboard()
        mime_data = QMimeData()
        mime_data.setText(item.text())
        clipboard.setMimeData(mime_data)

        # 显示气泡提示信息
        rect = self.visualItemRect(item)
        # 将局部坐标转换为全局坐标
        global_pos = self.mapToGlobal(rect.topRight())
        QToolTip.showText(global_pos, '已复制到剪贴板', self)


# IP地址处理框
class IPHandleWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # 创建两个选项卡
        ipFormatTrans_tab = QWidget()
        ipSetCalcu_tab = QWidget()


        
        # 将选项卡添加到QTabWidget
        self.addTab(ipFormatTrans_tab, qta.icon('fa.retweet'), "格式转换")
        self.addTab(ipSetCalcu_tab, qta.icon('fa.gg'), "IP集合运算")
        self.setTabToolTip(0,"支持IP地址掩码与范围之间格式转换")
        self.setTabToolTip(1,"支持IP地址集合的合并、拆分等等")
        self.tabBar().setDocumentMode(True)
        self.tabBar().setExpanding(True)
        
        ipFormatTrans_layout = QHBoxLayout()
        # IP地址输入框
        self.ipFormatTrans_content = oneInputoneOutput(ipFormatTrans_tab)
        
        self.ipFormatTrans_func = QWidget()
        ipFormatTrans_func_layout = QVBoxLayout()
        self.ipFormatTrans_func.setLayout(ipFormatTrans_func_layout)
        ## 功能按钮1(地址范围-->CIDR)
        self.iprange_to_cidr_button = QPushButton()
        self.iprange_to_cidr_button.setText("地址范围 --> CIDR")
        self.iprange_to_cidr_button.setToolTip("以掩码格式显示所有输入IP")
        self.iprange_to_cidr_button.clicked.connect(
            lambda: self.iprange_to_cidr_func(self.ipFormatTrans_content.ipInput_tab_1.toPlainText(),
            self.ipFormatTrans_content.ipOutput_tab))
        ## 功能按钮2(CIDR-->地址范围)
        self.cidr_to_iprange_button = QPushButton()
        self.cidr_to_iprange_button.setText("CIDR --> 地址范围")
        self.cidr_to_iprange_button.setToolTip("以IP范围格式显示所有输入IP")
        self.cidr_to_iprange_button.clicked.connect(
            lambda: self.cidr_to_iprange_func(self.ipFormatTrans_content.ipInput_tab_1.toPlainText(),
            self.ipFormatTrans_content.ipOutput_tab))
        
        ipFormatTrans_func_layout.addWidget(self.iprange_to_cidr_button)
        ipFormatTrans_func_layout.addWidget(self.cidr_to_iprange_button)
        
        ipFormatTrans_layout.addWidget(self.ipFormatTrans_func,1)
        ipFormatTrans_layout.addWidget(self.ipFormatTrans_content,5)
        ipFormatTrans_tab.setLayout(ipFormatTrans_layout)
        
        
        
        ipSetCalcu_layout = QHBoxLayout()
        self.ipSetCalcu_content = twoInputoneOutput(ipSetCalcu_tab)
        ipSetCalcu_tab.setLayout(ipSetCalcu_layout)
        
        self.ipSetCalcu_func = QWidget()
        ipSetCalcu_func_layout = QVBoxLayout()
        self.ipSetCalcu_func.setLayout(ipSetCalcu_func_layout)
        ## 功能按钮1(IP地址集合--交集)
        self.ipset_And = QPushButton()
        self.ipset_And.setText("IP地址集合--交集")
        ## 功能按钮2(IP地址集合--并集)
        self.ipset_Or = QPushButton()
        self.ipset_Or.setText("IP地址集合--并集")
        ## 功能按钮3(IP地址集合--差集)
        self.ipset_Not = QPushButton()
        self.ipset_Not.setText("IP地址集合--差集")
        ipSetCalcu_func_layout.addWidget(self.ipset_And)
        ipSetCalcu_func_layout.addWidget(self.ipset_Or)
        ipSetCalcu_func_layout.addWidget(self.ipset_Not)
        
        ipSetCalcu_layout.addWidget(self.ipSetCalcu_func,1)
        ipSetCalcu_layout.addWidget(self.ipSetCalcu_content,5)
        
    def iprange_to_cidr_func(self,intextStr,where_to_outtext):
        try:
            outtextStr = iprangeStr_To_cidrStr(intextStr)
        except ValueError as v:
            error_info = QMessageBox.critical(self,"IP地址输入错误",str(v),QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.NoButton)
            error_info.setWindowModality(Qt.WindowModality.ApplicationModal)
        where_to_outtext.setPlainText(outtextStr)
            
    
    def cidr_to_iprange_func(self,intextStr,where_to_outtext):
        try:
            outtextStr = cidrStr_To_iprangeStr(intextStr)
        except ValueError as v:
            error_info = QMessageBox.critical(self,"IP地址输入错误",str(v),QMessageBox.StandardButton.Ok,QMessageBox.StandardButton.NoButton)
            error_info.setWindowModality(Qt.WindowModality.ApplicationModal)
        where_to_outtext.setPlainText(outtextStr)
    
    def ipset_and_func():
        pass
    
    def ipset_and_func():
        pass
        
    def ipset_not_func():
        pass
        
        
class oneInputoneOutput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        content_layout = QVBoxLayout(self)
        
        # ip地址输入区域1
        self.ipInput_box1 = QWidget(self)
        self.ipInput_box1_layout = QGridLayout(self.ipInput_box1)
        self.ipInput_box1_layout.setSpacing(10)
        self.ipInput_box1.setLayout(self.ipInput_box1_layout)
        ## ip地址多行输入框
        self.ipInput_tab_1 = QPlainTextEdit(self.ipInput_box1)
        ## ip地址输入框功能按钮1----从剪贴板粘贴内容
        self.ipInput_1_button_pastefromclipboard = QPushButton(qta.icon('fa.paste'),"从剪贴板粘贴")
        self.ipInput_1_button_pastefromclipboard.clicked.connect(lambda: self.pastefromclipboard(self.ipInput_tab_1))
        ## ip地址输入框功能按钮2----清除内容
        self.ipInput_1_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")
        self.ipInput_1_button_clean.clicked.connect(lambda: self.textClean(self.ipInput_tab_1))
        self.ipInput_box1_layout.addWidget(self.ipInput_tab_1,0,0,1,2)
        self.ipInput_box1_layout.addWidget(self.ipInput_1_button_pastefromclipboard,1,0,1,1)
        self.ipInput_box1_layout.addWidget(self.ipInput_1_button_clean,1,1,1,1)
        
        # ip地址输出区域
        self.ipOutput_box = QWidget(self)
        self.ipOutput_box_layout = QGridLayout(self.ipOutput_box)
        self.ipOutput_box_layout.setSpacing(10)
        self.ipOutput_box.setLayout(self.ipOutput_box_layout)
        
        ## ip地址多行输出框
        self.ipOutput_tab = QPlainTextEdit(self.ipOutput_box)
        self.ipOutput_tab.setLineWrapMode
        self.ipOutput_tab.setReadOnly(True)
        ## ip地址输入框功能按钮1----复制到剪贴板
        self.ipOutput_button_copytoclipboard = QPushButton(qta.icon('fa.copy'),"复制内容到剪贴板")
        self.ipOutput_button_copytoclipboard.clicked.connect(lambda: self.copytoclipboard(self.ipOutput_tab))
        ## ip地址输入框功能按钮2----清除内容
        self.ipOutput_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")
        self.ipOutput_button_clean.clicked.connect(lambda: self.textClean(self.ipOutput_tab))

        self.ipOutput_box_layout.addWidget(self.ipOutput_tab,0,0,1,2)
        self.ipOutput_box_layout.addWidget(self.ipOutput_button_copytoclipboard,1,0,1,1)
        self.ipOutput_box_layout.addWidget(self.ipOutput_button_clean,1,1,1,1)
        
        
        content_layout.addWidget(self.ipInput_box1)
        content_layout.addWidget(self.ipOutput_box)
        self.setLayout(content_layout)
        
    
    def pastefromclipboard(self, input_edit):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        if clipboard_text:
            input_edit.setPlainText(clipboard_text)
    
    def textClean(self,input_edit):
        input_edit.clear()
        
    def copytoclipboard(self,output_edit):
        result_text = output_edit.toPlainText()
        # 获取粘贴板
        clipboard = QApplication.clipboard()

        # 将文本复制到粘贴板
        clipboard.setText(result_text, mode=QClipboard.Clipboard)
        clipboard.setText(result_text, mode=QClipboard.Selection)
    
    
    
class twoInputoneOutput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        content_layout = QGridLayout(self)
        self.setLayout(content_layout)

        # ip地址输入区域1
        self.ipInput_box1 = QWidget()
        self.ipInput_box1_layout = QGridLayout()
        self.ipInput_box1_layout.setSpacing(10)
        self.ipInput_box1.setLayout(self.ipInput_box1_layout)
        ## ip地址多行输入框
        self.ipInput_tab_1 = QPlainTextEdit()
        ## ip地址输入框功能按钮1----从剪贴板粘贴内容
        self.ipInput_1_button_pastefromclipboard = QPushButton(qta.icon('fa.paste'),"从剪贴板粘贴")
        self.ipInput_1_button_pastefromclipboard.clicked.connect(lambda: self.pastefromclipboard(self.ipInput_tab_1))
        ## ip地址输入框功能按钮2----清除内容
        self.ipInput_1_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")
        self.ipInput_1_button_clean.clicked.connect(lambda: self.textClean(self.ipInput_tab_1))
        self.ipInput_box1_layout.addWidget(self.ipInput_tab_1,0,0,1,2)
        self.ipInput_box1_layout.addWidget(self.ipInput_1_button_pastefromclipboard,1,0)
        self.ipInput_box1_layout.addWidget(self.ipInput_1_button_clean,1,1)

        # ip地址输入区域2
        self.ipInput_box2 = QWidget()
        self.ipInput_box2_layout = QGridLayout()
        self.ipInput_box2_layout.setSpacing(10)
        self.ipInput_box2.setLayout(self.ipInput_box2_layout)
        ## ip地址多行输入框2
        self.ipInput_tab_2 = QPlainTextEdit()
        ## ip地址输入框功能按钮1----从剪贴板粘贴内容
        self.ipInput_2_button_pastefromclipboard = QPushButton(qta.icon('fa.paste'),"从剪贴板粘贴")
        self.ipInput_2_button_pastefromclipboard.clicked.connect(lambda: self.pastefromclipboard(self.ipInput_tab_2))
        ## ip地址输入框功能按钮2----清除内容
        self.ipInput_2_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")
        self.ipInput_2_button_clean.clicked.connect(lambda: self.textClean(self.ipInput_tab_2))
        self.ipInput_box2_layout.addWidget(self.ipInput_tab_2,0,0,1,2)
        self.ipInput_box2_layout.addWidget(self.ipInput_2_button_pastefromclipboard,1,0)
        self.ipInput_box2_layout.addWidget(self.ipInput_2_button_clean,1,1)


        # ip地址输出区域
        self.ipOutput_box = QWidget()
        self.ipOutput_box_layout = QGridLayout()
        self.ipOutput_box_layout.setSpacing(10)
        self.ipOutput_box.setLayout(self.ipOutput_box_layout)
        ## ip地址多行输出框
        self.ipOutput_tab = QPlainTextEdit()
        self.ipOutput_tab.setReadOnly(True)
        ## ip地址输入框功能按钮1----复制到剪贴板
        self.ipOutput_button_copytoclipboard = QPushButton(qta.icon('fa.copy'),"复制内容到剪贴板")
        self.ipOutput_button_copytoclipboard.clicked.connect(lambda: self.copytoclipboard(self.ipOutput_tab))
        ## ip地址输入框功能按钮2----清除内容
        self.ipOutput_button_clean = QPushButton(qta.icon('fa.undo'),"清除内容")
        self.ipOutput_button_clean.clicked.connect(lambda: self.textClean(self.ipOutput_tab))

        self.ipOutput_box_layout.addWidget(self.ipOutput_tab,0,0,1,2)
        self.ipOutput_box_layout.addWidget(self.ipOutput_button_copytoclipboard,1,0)
        self.ipOutput_box_layout.addWidget(self.ipOutput_button_clean,1,1)
        
        
        content_layout.addWidget(self.ipInput_box1,0,0,1,1)
        content_layout.addWidget(self.ipInput_box2,0,1,1,1)
        content_layout.addWidget(self.ipOutput_box,1,0,1,2)
        
        
    def pastefromclipboard(self, input_edit):
        clipboard = QApplication.clipboard()
        clipboard_text = clipboard.text()
        if clipboard_text:
            input_edit.setPlainText(clipboard_text)
    
    def textClean(self,input_edit):
        input_edit.clear()
        
    def copytoclipboard(self,output_edit):
        result_text = output_edit.toPlainText()
        # 获取粘贴板
        clipboard = QApplication.clipboard()

        # 将文本复制到粘贴板
        clipboard.setText(result_text, mode=QClipboard.Clipboard)
        clipboard.setText(result_text, mode=QClipboard.Selection)