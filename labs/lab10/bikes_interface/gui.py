import sys

from PySide6.QtWidgets import QMainWindow, QApplication, QGridLayout, QWidget, \
    QLineEdit, QPushButton, QHBoxLayout, QListWidget, QVBoxLayout, \
    QLabel, QComboBox, QTextEdit, QMessageBox, QHBoxLayout, QFileDialog
from PySide6.QtCore import Qt, QSize
from pathlib import Path
from labs.lab10.bikes_database.select_from_db import SQLSelector

QUERY_AVERAGE_RENTAL_TIME_STARTING_AT_STATION = "Compute average rental time starting at the station"
QUERY_AVERAGE_RENTAL_TIME_ENDING_AT_STATION = "Compute average rental time ending at the station"
QUERY_NUMBER_OF_BIKES_PARKED_AT_STATION = "Compute number of distinct bikes parked at the station"
QUERY_AVERAGE_TIME_BETWEEN_VISITING_STATION = "Compute average daily rentals initiated at the station"

CURRENT_DIRECTORY = Path(__file__).parents[1]

QUERY_MAPPINGS = {
    QUERY_AVERAGE_RENTAL_TIME_STARTING_AT_STATION: "compute_average_rental_time_starting_at_station",
    QUERY_AVERAGE_RENTAL_TIME_ENDING_AT_STATION: "compute_average_rental_time_ending_at_station",
    QUERY_NUMBER_OF_BIKES_PARKED_AT_STATION: "compute_number_of_bikes_parked",
    QUERY_AVERAGE_TIME_BETWEEN_VISITING_STATION: "compute_average_daily_rentals_from_station"
}


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        # There must be a text entry to enter database path

        self.sql_selector = None
        self.database_name = None

        self.setFixedSize((QSize(600, 500)))
        window_layout = QGridLayout()
        window_layout.rowStretch(6)
        window_layout.columnStretch(6)
        widget = QWidget()

        up_widget = QWidget()
        up_widget_layout = QHBoxLayout()
        # up_widget_layout = QGridLayout()
        # up_widget_layout.rowStretch(1)
        # up_widget_layout.columnStretch(6)
        self.open_database_button = QPushButton()
        self.open_database_button.setText("Open")

        up_widget_layout.addWidget(QLabel("Enter DB location: "), alignment=Qt.AlignmentFlag.AlignLeft)
        up_widget_layout.addWidget(self.open_database_button, alignment=Qt.AlignmentFlag.AlignCenter)
        up_widget.setLayout(up_widget_layout)

        '''
        up_widget_layout.addWidget(QLabel("Enter DB location: "), 0, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        up_widget_layout.addWidget(self.database_name, 0, 2, 1, 2, alignment=Qt.AlignmentFlag.AlignHCenter)
        up_widget_layout.addWidget(self.open_database_button, 0, 4, 1, 2, alignment=Qt.AlignmentFlag.AlignRight)
        up_widget.setLayout(up_widget_layout)'''

        middle_left_widget = QWidget()
        self.stations_list_widget = QListWidget()
        list_widget_layout = QGridLayout()
        list_widget_layout.rowStretch(3)
        list_widget_layout.columnStretch(3)
        list_widget_layout.addWidget(self.stations_list_widget, 1, 0, 3, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        middle_left_widget.setLayout(list_widget_layout)

        query_select_widget = QWidget()
        query_select_widget_layout = QVBoxLayout()
        query_select_widget_layout.addWidget(QLabel("Select Query"), alignment=Qt.AlignmentFlag.AlignTop)
        self.query_combo_box = QComboBox(query_select_widget)
        self.query_combo_box.addItem(QUERY_AVERAGE_RENTAL_TIME_STARTING_AT_STATION)
        self.query_combo_box.addItem(QUERY_AVERAGE_RENTAL_TIME_ENDING_AT_STATION)
        self.query_combo_box.addItem(QUERY_NUMBER_OF_BIKES_PARKED_AT_STATION)
        self.query_combo_box.addItem(QUERY_AVERAGE_TIME_BETWEEN_VISITING_STATION)
        self.result_text = QTextEdit(query_select_widget)
        self.result_text.setReadOnly(True)

        self.run_query_button = QPushButton("Run")

        query_select_widget_layout.addWidget(self.query_combo_box)
        query_select_widget_layout.addWidget(self.run_query_button, alignment=Qt.AlignmentFlag.AlignLeft)
        query_select_widget_layout.addWidget(self.result_text)

        query_select_widget.setLayout(query_select_widget_layout)
        down_widget = QWidget()

        window_layout.addWidget(up_widget, 0, 1, 1, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        window_layout.addWidget(middle_left_widget, 1, 0, 3, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        window_layout.addWidget(query_select_widget, 1, 3, 3, 3, alignment=Qt.AlignmentFlag.AlignHCenter)
        window_layout.addWidget(down_widget, 5, 0, 1, 6)

        widget.setLayout(window_layout)
        self.setCentralWidget(widget)

        self.open_database_button.clicked.connect(self.connect_to_db)
        self.run_query_button.clicked.connect(self.run_query)

    def connect_to_db(self):
        self.stations_list_widget.clear()
        if self.open_file_dialog():
            self.sql_selector = SQLSelector(str(self.database_name))
            self.stations_list_widget.addItems([s.station_name for s
                                            in self.sql_selector.select_all_stations()])

    def run_query(self):
        query_name = self.query_combo_box.currentText()
        if self.sql_selector:
            query_result = getattr(self.sql_selector, QUERY_MAPPINGS[query_name])\
                (self.stations_list_widget.currentItem().text())
            self.result_text.setText("Result = " + str(query_result))
        else:
            self.display_error_msg("The database is not present")

    def display_error_msg(self, msg=""):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Error")
        dlg.setText(msg)
        dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.exec()

    def open_file_dialog(self):
        dialog = QFileDialog(self)
        dialog.setDirectory(str(CURRENT_DIRECTORY))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        # dialog.setNameFilter("*.db")
        if dialog.exec():
            database_names = dialog.selectedFiles()
            if database_names:
                self.database_name = Path(database_names[0])
                return True
        return False


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec()





