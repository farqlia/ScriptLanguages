import os
import sys
from pathlib import Path
from os import access, R_OK, EX_OK
import labs.ssh_logs_program.src.model.logging_configure as logging_configure

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QWidget, QGridLayout, QLineEdit, \
    QHBoxLayout, QFileDialog, QDialogButtonBox, QDialog, QLabel, QMessageBox
from labs.ssh_logs_program.src.view import master_widget, detail_widget
from labs.ssh_logs_program.src.model import ssh_log_journal, read_logs_from_file, log_factory

# Signals are usually send by widgets and triggered by users
# Events are user interactions with Qt App
# Slots are receivers of signals

DATA_DIR = str(Path(__file__).parents[2] / 'data')


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
        self.open_file_dialog_button = QPushButton(open_widget)
        self.open_file_dialog_button.setText("File Dialog")
        self.open_button = QPushButton(open_widget)
        self.open_button.setText("Open")
        open_widget_layout = QGridLayout()
        open_widget_layout.rowStretch(1)
        open_widget_layout.columnStretch(6)
        open_widget_layout.addWidget(self.open_entry, 0, 0)
        open_widget_layout.addWidget(self.open_button, 0, 3)
        open_widget_layout.addWidget(self.open_file_dialog_button, 0, 5)
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
        self.layout.rowStretch(7)
        self.layout.columnStretch(6)

        self.layout.addWidget(open_widget, 0, 0, 1, 6)
        self.layout.addWidget(data_widget, 2, 0, 4, 6)
        self.layout.addWidget(navigation_button_widget, 6, 0, 1, 6)

        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

        self.next_button.clicked.connect(self.next_item)
        self.prev_button.clicked.connect(self.previous_item)
        self.open_button.clicked.connect(self.read_data_from_given_path)
        self.open_file_dialog_button.clicked.connect(self.read_data_with_file_dialog)

        self.clear()

    def read_data_from_given_path(self):
        self.filename = Path(self.open_entry.text().strip())
        if self.check_file_correctness():
            self.update_data()

    def read_data_with_file_dialog(self):
        if self.open_file_dialog() and self.check_file_correctness():
            self.update_data()

    def update_data(self):
        try:
            self.container = self.data_handler.read_from_file(self.filename)
            self.master_widget.items = self.container
            self.master_widget.set_current_row(0)
            self.enable_buttons()
        except ValueError:
            self.display_error_msg(f"Couldn't parse file: {self.filename}")
        except Exception:
            self.display_error_msg(f"Unknown error occured")

    def check_file_correctness(self):
        if not self.data_handler.is_correct_extension(self.filename):
            if not self.display_yes_no_choice_dialog(f"File {self.filename} is not of correct type."
                                          f" Do you want to open it?"):
                return False

        if not self.data_handler.can_be_opened(self.filename):
            self.display_error_msg(f"Couldn't open: {self.filename}")
            return False

        return True

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(DATA_DIR)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        # dialog.setNameFilter("*.log")
        if dialog.exec():
            filenames = dialog.selectedFiles()
            print(filenames)
            if filenames:
                self.filename = Path(filenames[0])
                return True
        return False

    def display_error_msg(self, msg=""):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(msg)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.exec()
        self.open_entry.clear()

    def display_yes_no_choice_dialog(self, msg):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Question")
        dlg.setText(msg)
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        return dlg.exec() == QMessageBox.StandardButton.Yes

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

    def disable_buttons(self):
        self.next_button.setEnabled(False)
        self.prev_button.setEnabled(False)

    def enable_buttons(self):
        self.next_button.setEnabled(True)
        self.prev_button.setEnabled(True)

    def clear(self):
        self.detail_widget.clear()
        self.detail_widget.show()
        self.master_widget.clear()
        self.master_widget.items = None
        self.master_widget.currently_displayed = None
        self.disable_buttons()


if __name__ == "__main__":

    logging_configure.configure_logging()

    app = QApplication(sys.argv)

    reader = read_logs_from_file.SSHLogsHandler()

    window = MainWindow(reader)
    window.show()

    app.exec()


