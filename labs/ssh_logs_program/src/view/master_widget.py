import datetime

from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QDateTimeEdit, QLabel, QGridLayout
from PySide6.QtCore import QSize, Qt, QDateTime
from labs.ssh_logs_program.src.view.utils import to_datetime, to_q_datetime


class MasterWidget(QWidget):

    def __init__(self, detail_widget):
        super().__init__()

        self._items = None
        self._currently_displayed = None

        self.detail_widget = detail_widget

        self.widget_list = QListWidget()

        self.datetime_widget_from = QDateTimeEdit()
        self.datetime_widget_from.setDateTime(QDateTime(2022, 12, 10, 8, 25, 0))
        self.datetime_widget_to = QDateTimeEdit()
        self.datetime_widget_to.setDateTime(QDateTime(2022, 12, 10, 9, 30, 0))

        datetime_from_widget = QWidget()
        datetime_from_layout = QHBoxLayout()
        datetime_from_layout.addWidget(QLabel("From"), alignment=Qt.AlignmentFlag.AlignLeft)
        datetime_from_layout.addWidget(self.datetime_widget_from, alignment=Qt.AlignmentFlag.AlignLeft)
        datetime_from_widget.setLayout(datetime_from_layout)

        datetime_to_widget = QWidget()
        datetime_to_layout = QHBoxLayout()
        datetime_to_layout.addWidget(QLabel("To"), alignment=Qt.AlignmentFlag.AlignRight)
        datetime_to_layout.addWidget(self.datetime_widget_to, alignment=Qt.AlignmentFlag.AlignRight)
        datetime_to_widget.setLayout(datetime_to_layout)

        datetimes_widget = QWidget()
        datetimes_layout = QGridLayout()
        datetimes_layout.rowStretch(1)
        datetimes_layout.columnStretch(6)
        datetimes_layout.addWidget(datetime_from_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        datetimes_layout.addWidget(datetime_to_widget, 0, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        datetimes_widget.setLayout(datetimes_layout)

        layout = QVBoxLayout()
        layout.addWidget(datetimes_widget)
        layout.addWidget(self.widget_list)

        self.widget_list.itemClicked.connect(self.dispatch_to_detail_view)
        self.widget_list.itemSelectionChanged.connect(self.dispatch_to_detail_view)
        self.datetime_widget_from.dateTimeChanged.connect(self._set_new_date_range)
        self.datetime_widget_to.dateTimeChanged.connect(self._set_new_date_range)

        self.setLayout(layout)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items
        self._currently_displayed = items
        self._set_new_date_range()
        # self.widget_list.addItems(journal)

    def update_view(self):
        self.widget_list.clear()
        for item in self._currently_displayed:
            self.widget_list.addItem(str(item)[:60] + "...")
        # self.widget_list.show()

    def dispatch_to_detail_view(self):
        self.detail_widget.display_detailed_view(self.items[self.widget_list.currentRow()])

    def set_current_row(self, row):
        can_be_changed = 0 <= row < self.widget_list.count()
        if can_be_changed:
            self.widget_list.setCurrentRow(row)
            self.dispatch_to_detail_view()
        return can_be_changed

    def get_current_row(self):
        return self.widget_list.currentRow()

    def _set_new_date_range(self):
        self._currently_displayed = self._items[self.datetime_widget_from.dateTime().toPython():self.datetime_widget_to.dateTime().toPython()]
        self.update_view()

    def clear(self):
        self.widget_list.clear()
