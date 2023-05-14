from PySide6.QtWidgets import QWidget, QListWidget, QVBoxLayout


class DetailWidget(QWidget):

    def __init__(self):
        super(DetailWidget, self).__init__()

    def display_detailed_view(self, item):
        print(item)

    def clear(self):
        print("Clearing")

