import sys
import random
import time

from PySide6 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.n = 0

        self.hello = random.choices(['hola', 'cześć', 'hello'], k=600)
        self.button = QtWidgets.QPushButton("Click me!")
        # self.button.setCheckable(True)
        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItems(["Uno", "Dos", "Tres"])
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(600)


        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.progress_bar)

        self.button.clicked.connect(self.magic)
        self.button.clicked.connect(self.the_button_was_pushed)
        self.list_widget.itemClicked.connect(self.print_clicked_list_item)

        self.button.clicked.connect(self.read_list)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

    def read_list(self):
        for i in self.hello:
            self.n += 1
            # time.sleep(0.005)
            # self.progress_bar.setValue(self.n)
            self.list_widget.insertItem(self.list_widget.currentRow() + 1,
                                         i)

    def the_button_was_clicked(self, checked):
        print("Checked?", checked)

    def print_clicked_list_item(self, index):
        print("Clicked item:", self.list_widget.currentRow())

    def the_button_was_pushed(self):
        self.button.setText("You already clicked me.")
        self.button.setEnabled(False)

        self.setWindowTitle("Oneshot App")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())