from PyQt6.QtCore import Qt, QEvent, QRegularExpression, pyqtSignal, QItemSelectionModel
from PyQt6.QtWidgets import QWidget, QLineEdit, QHBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, QAbstractItemView, QTableWidget, QHeaderView
from PyQt6.QtGui import QRegularExpressionValidator
from IPTOOL.iptool import ip_to_subnetlist

class IpInputWidget(QWidget):
    # 定义ipv4地址的4个段
    ip = ["192","168","0","1"]
    # 定义ipv4地址某一段的校验正则
    ip_validator = QRegularExpressionValidator(QRegularExpression("((2[0-4]\d)|(25[0-5])|(1\d{2})|(\d{1,2}))"))

    # 是否输入完成
    ipCompleted = pyqtSignal(str)


    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # 创建四个 QLineEdit 分别用于输入 IPv4 地址的四个段
        self.segment_inputs = [IpLineEdit() for _ in range(4)]

        for index, input_field in enumerate(self.segment_inputs):
            input_field.setMaxLength(3)  # 设置最大长度为3
            input_field.setValidator(self.ip_validator)
            input_field.setPlaceholderText(self.ip[index])  # 设置初始字段
            input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
            input_field.installEventFilter(self)  # 安装事件过滤器

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


class IpLineEdit(QLineEdit):
    pass

class SubnetsTableWidget(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setRowCount(33)
        self.setColumnCount(7)
        self.setHorizontalHeaderLabels(['子网前缀','子网掩码','反掩码','地址范围','子网id','广播地址','地址数量'])
        self.setShowGrid(False)
        self.verticalHeader().setHidden(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resizeColumnsToContents()
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # self.setColumnCount(3)
        # self.setHeaderLabels(['子网前缀','子网掩码','反掩码','地址范围','子网id','广播地址','地址数量'])
        # self.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.setAlternatingRowColors(True)
        # subnetsTableList = []
        # for i in range(32,-1,-1):
        #     top_item = QTreeWidgetItem(self)
        #     top_item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsUserCheckable)
        #     subnetsTableList.append(top_item)
        # self.addTopLevelItems(subnetsTableList)
        
        # self.update_table("192.168.0.1")
        

    def update_table(self, ip_address):
        subnetsTableList = ip_to_subnetlist(ip_address)
        for top_index in range(self.topLevelItemCount()-1):
            top_item = self.topLevelItem(top_index)
            for col in range(self.columnCount()):
                top_item.setText(col,subnetsTableList[top_index][col])
                top_item.setTextAlignment(col,Qt.AlignmentFlag.AlignCenter)
                self.resizeColumnToContents(col)