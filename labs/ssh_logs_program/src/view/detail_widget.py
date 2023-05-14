from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QTextBrowser, QTextEdit, QHBoxLayout
from PySide6.QtCore import Qt
from labs.ssh_logs_program.src.model.ssh_log_entry import SSHLogEntry
from PySide6.QtGui import QFont
from labs.ssh_logs_program.src.model import regex_ssh_utilis


class DetailWidget(QWidget):

    def __init__(self):
        super(DetailWidget, self).__init__()

        details_widget = QWidget()

        detail_widget_layout = QGridLayout(self)
        detail_widget_layout.rowStretch(6)
        detail_widget_layout.columnStretch(3)

        detail_widget_layout.addWidget(QLabel("PID"), 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.pid_widget = QLineEdit()
        self.pid_widget.setReadOnly(True)
        detail_widget_layout.addWidget(self.pid_widget, 0, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        detail_widget_layout.addWidget(QLabel("Host"), 1, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.host_widget = QLineEdit()
        self.host_widget.setReadOnly(True)
        detail_widget_layout.addWidget(self.host_widget, 1, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        detail_widget_layout.addWidget(QLabel("Date"), 2, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.date_widget = QLineEdit()
        self.date_widget.setReadOnly(True)
        detail_widget_layout.addWidget(self.date_widget, 2, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        detail_widget_layout.addWidget(QLabel("IPv4 Address"), 3, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.ipv4_address_widget = QLineEdit()
        self.ipv4_address_widget.setReadOnly(True)
        detail_widget_layout.addWidget(self.ipv4_address_widget, 3, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        detail_widget_layout.addWidget(QLabel("Message"), 4, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.message_widget = QTextEdit()
        self.message_widget.setReadOnly(True)
        detail_widget_layout.addWidget(self.message_widget, 4, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        detail_widget_layout.addWidget(QLabel("Type"), 5, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        self.type_widget = QLabel()
        detail_widget_layout.addWidget(self.type_widget, 5, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)

        details_widget.setLayout(detail_widget_layout)

        header_widget = QWidget()
        header_widget_layout = QVBoxLayout()
        header_label = QLabel("Details Section")
        header_widget_layout.addWidget(header_label)
        header_widget.setLayout(header_widget_layout)

        empty_widget = QWidget()

        layout = QVBoxLayout()
        layout.addWidget(header_widget)
        layout.addWidget(details_widget)
        layout.addWidget(empty_widget)
        self.setLayout(layout)

    def display_detailed_view(self, item: SSHLogEntry):
        self.pid_widget.setText(str(item.pid))
        self.host_widget.setText(item.host)
        self.date_widget.setText(str(item.date))
        self.ipv4_address_widget.setText(item.ipv4_address if item.has_ip else "unknown")
        self.message_widget.setText(item.message)
        self.type_widget.setText(regex_ssh_utilis.get_message_type(item).format())

    def clear(self):
        self.pid_widget.clear()
        self.host_widget.clear()
        self.date_widget.clear()
        self.ipv4_address_widget.clear()
        self.message_widget.clear()

