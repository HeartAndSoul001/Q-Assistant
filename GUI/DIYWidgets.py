from PyQt6.QtCore import (QRegularExpression,Qt)
from PyQt6.QtWidgets import (QWidget,QLineEdit,QGridLayout,QLabel)
from PyQt6.QtGui import (QRegularExpressionValidator,QFont)





class Ip_input_widget(QWidget):

    ip_a = "192"
    ip_b = "168"
    ip_c = "0"
    ip_d = "1"

    ip_validator = QRegularExpressionValidator(QRegularExpression("((2[0-4]\d)|(25[0-5])|(1\d{2})|(\d{1,2}))"))

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        






        subnet_font = QFont()

        ip_input_layout = QGridLayout()

        subnet_font.setFamily(u"Courier")
        subnet_font.setPointSize(8)
        subnet_font.setBold(True)
        subnet_font.setItalic(False)

        ipv4_a_input =  QLineEdit()
        ipv4_a_input.setPlaceholderText(self.ip_a)
        ipv4_a_input.setValidator(self.ip_validator)
        ipv4_a_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ipv4_a_input.setFont(subnet_font)
        
        ipv4_a_dot = QLabel(".")
        ipv4_a_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ipv4_a_dot.setFont(subnet_font)
        ipv4_b_input =  QLineEdit()
        ipv4_b_input.setPlaceholderText(self.ip_b)
        ipv4_b_input.setValidator(self.ip_validator)
        ipv4_b_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ipv4_b_input.setFont(subnet_font)
        ipv4_b_dot = QLabel(".")
        ipv4_b_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ipv4_b_dot.setFont(subnet_font)
        ipv4_c_input =  QLineEdit()
        ipv4_c_input.setPlaceholderText(self.ip_c)
        ipv4_c_input.setValidator(self.ip_validator)
        ipv4_c_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ipv4_c_input.setFont(subnet_font)
        ipv4_c_dot = QLabel(".")
        ipv4_c_dot.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ipv4_c_dot.setFont(subnet_font)
        ipv4_d_input =  QLineEdit()
        ipv4_d_input.setPlaceholderText(self.ip_d)
        ipv4_d_input.setValidator(self.ip_validator)
        ipv4_d_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ipv4_d_input.setFont(subnet_font)
        # ipv4_d_input.end(True)
        ip_input_layout.setSpacing(0)
        self.setLayout(ip_input_layout)
        ip_input_layout.addWidget(ipv4_a_input,0,0,1,6)
        ip_input_layout.addWidget(ipv4_a_dot,0,7)
        ip_input_layout.addWidget(ipv4_b_input,0,8,1,6)
        ip_input_layout.addWidget(ipv4_b_dot,0,14)
        ip_input_layout.addWidget(ipv4_c_input,0,15,1,6)
        ip_input_layout.addWidget(ipv4_c_dot,0,21)
        ip_input_layout.addWidget(ipv4_d_input,0,22,1,6)

