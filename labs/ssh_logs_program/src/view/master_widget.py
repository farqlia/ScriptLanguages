from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout, QHBoxLayout, QDateTimeEdit, QLabel, QGridLayout
from PySide6.QtCore import QSize, Qt, QDateTime
from labs.ssh_logs_program.src.view.utils import to_datetime, to_q_datetime


class MasterWidget(QWidget):

    def __init__(self, detail_widget):
        super().__init__()

        self._items = None
        self._currently_displayed = None

        self.detail_widget = detail_widget

        self.datetime_from = None
        self.datetime_to = None

        self.widget_list = QListWidget()

        self.datetime_widget_from = QDateTimeEdit()
        current_q_datetime = QDateTime.currentDateTime()
        self.datetime_widget_from.setDateTime(current_q_datetime.addYears(-2))
        self.datetime_widget_to = QDateTimeEdit()
        self.datetime_widget_to.setDateTime(current_q_datetime)

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
        datetimes_layout.addWidget(datetime_from_widget, 0, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        datetimes_layout.addWidget(datetime_to_widget, 0, 2, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)
        datetimes_widget.setLayout(datetimes_layout)

        layout = QVBoxLayout()
        layout.addWidget(datetimes_widget)
        layout.addWidget(self.widget_list)

        self.widget_list.itemClicked.connect(self.dispatch_to_detail_view)
        self.widget_list.itemSelectionChanged.connect(self.dispatch_to_detail_view)
        self.datetime_widget_from.dateTimeChanged.connect(self.filter_from)
        self.datetime_widget_to.dateTimeChanged.connect(self.filter_to)

        self.setLayout(layout)

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        self._items = items
        self._currently_displayed = items
        self.update_view()
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

    def filter_from(self, q_datetime: QDateTime):
        self.datetime_from = to_datetime(q_datetime)
        self._set_new_date_range()

    def filter_to(self, q_datetime: QDateTime):
        self.datetime_to = to_datetime(q_datetime)
        self._set_new_date_range()

    def _set_new_date_range(self):
        self._currently_displayed = self._items[self.datetime_from:self.datetime_to]
        self.update_view()
