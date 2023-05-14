import sys
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QWidget, QGridLayout, QLineEdit, \
    QHBoxLayout, QFileDialog, QDialogButtonBox, QDialog, QLabel, QMessageBox
from labs.ssh_logs_program.src.view import master_widget, detail_widget
from labs.ssh_logs_program.src.model import ssh_log_journal, read_logs_from_file, log_factory

# Signals are usually send by users
# Slots are receivers of signals

# TODO: set limits on dates and font/style


class MainWindow(QMainWindow):

    def __init__(self, data_handler: read_logs_from_file.LogHandler):
        super(MainWindow, self).__init__()

        self.setFixedSize((QSize(900, 500)))

        self.setWindowTitle("Log browser")
        self.container = None
        self.data_handler = data_handler
        self.filename = None

        open_widget = QWidget()
        self.open_entry = QLineEdit(open_widget)
        self.open_button = QPushButton(open_widget)
        self.open_button.setText("Open")
        open_widget_layout = QGridLayout()
        open_widget_layout.rowStretch(1)
        open_widget_layout.columnStretch(6)
        open_widget_layout.addWidget(self.open_entry, 0, 0)
        open_widget_layout.addWidget(self.open_button, 0, 5)
        open_widget.setLayout(open_widget_layout)

        data_widget = QWidget()
        data_widgets_layout = QGridLayout(data_widget)
        data_widgets_layout.rowStretch(4)
        data_widgets_layout.columnStretch(4)

        self.detail_widget = detail_widget.DetailWidget()
        self.master_widget = master_widget.MasterWidget(self.detail_widget)

        data_widgets_layout.addWidget(self.master_widget, 0, 0, 4, 3)
        data_widgets_layout.addWidget(self.detail_widget, 0, 4, 4, 1)
        data_widget.setLayout(data_widgets_layout)

        navigation_buttons_layout = QGridLayout()
        navigation_buttons_layout.rowStretch(1)
        navigation_buttons_layout.columnStretch(6)

        self.next_button = QPushButton()
        self.next_button.setText("Next")

        self.prev_button = QPushButton()
        self.prev_button.setText("Previous")

        navigation_buttons_layout.addWidget(self.prev_button, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        navigation_buttons_layout.addWidget(self.next_button, 0, 5, alignment=Qt.AlignmentFlag.AlignRight)

        navigation_button_widget = QWidget()
        navigation_button_widget.setLayout(navigation_buttons_layout)

        widget = QWidget()
        self.layout = QGridLayout()
        self.layout.rowStretch(6)
        self.layout.columnStretch(6)
        self.layout.addWidget(open_widget, 0, 0, 1, 6)
        self.layout.addWidget(data_widget, 1, 0, 4, 6)
        self.layout.addWidget(navigation_button_widget, 5, 0, 1, 6)

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        # self.open_button.clicked.connect(self.read_data_from_file)
        self.next_button.clicked.connect(self.next_item)
        self.prev_button.clicked.connect(self.previous_item)
        self.open_button.clicked.connect(self.read_data_from_file)

    def read_data_from_file(self):
        self.filename = self.open_entry.text()
        if len(self.filename) == 0:
            self.open_file_dialog()
        elif not Path(self.filename).exists():
            self.filename = None
            self.display_error_msg()

        if self.filename:
            self.container = self.data_handler.read_from_file(self.filename)
            self.master_widget.items = self.container
            self.master_widget.set_current_row(0)

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(r'C:\Users\julia\PycharmProjects\ScriptLanguages\labs\ssh_logs_program\data')
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        dialog.setNameFilter("*.log")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            print(filenames)
            if filenames:
                self.filename = filenames[0]

    def display_error_msg(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText("Couldn't open a file")
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.exec()
        self.open_entry.clear()

    def next_item(self):
        is_next = self.master_widget.set_current_row(self.master_widget.get_current_row() + 1)
        if not is_next:
            self.next_button.setEnabled(False)
        elif not self.prev_button.isEnabled():
            self.prev_button.setEnabled(True)

    def previous_item(self):
        is_prev = self.master_widget.set_current_row(self.master_widget.get_current_row() - 1)
        if not is_prev:
            self.prev_button.setEnabled(False)
        elif not self.next_button.isEnabled():
            self.next_button.setEnabled(True)


class ErrorDialog(QDialog):

    def __init__(self, msg):
        super(ErrorDialog, self).__init__()
        self.setWindowTitle("Error")
        qbtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    reader = read_logs_from_file.SSHLogsHandler()

    window = MainWindow(reader)
    window.show()

    app.exec()


