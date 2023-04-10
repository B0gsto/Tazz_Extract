import PyQt6 as pyqt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QHeaderView
from PyQt6.QtGui import QIcon
from TazzExtract import *
from TazzCities import *
import sys


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        extract_and_save_tazz_cities()
        self.title = 'window'
        self.resize(640, 480)
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Label
        Label = pyqt.QtWidgets.QLabel(self)
        Label.setText("Select the city name:")
        layout.addWidget(Label)

        # QComboBox with cities
        self.combo = pyqt.QtWidgets.QComboBox()
        with open("tazz_cities.txt", 'r', encoding="UTF-8") as file:
            for line in file:
                self.combo.addItem(line.split(';')[0])
        layout.addWidget(self.combo)

        # buttons
        extract_button = pyqt.QtWidgets.QPushButton('Extract')
        extract_button.clicked.connect(self.extract_restaurants)

        show_button = pyqt.QtWidgets.QPushButton('Show second screen')
        show_button.clicked.connect(self.show_second_screen)

        layout.addWidget(extract_button)
        layout.addWidget(show_button)

        # create SecondScreen object
        self.second_screen = SecondScreen()
        self.second_screen.setStyleSheet(open("style/second_screen_style.css").read())
        self.second_screen.hide()

    # new function to extract restaurants
    def extract_restaurants(self):
        option = self.combo.currentText()
        extract_and_save_tazz_restaurants(option)
        self.second_screen.update_table()

    def show_second_screen(self):
        self.second_screen.show()


class SecondScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'window'
        self.left = 10
        self.top = 10
        self.resize(640, 480)
        layout = QVBoxLayout()
        self.setLayout(layout)
        # table
        self.table = pyqt.QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nume", "Livrare", "Stele"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

        # connect the header sectionClicked signal to the sort_table method
        header.sectionClicked.connect(self.sort_table)

        layout.addWidget(self.table)

    def update_table(self):
        self.table.setRowCount(0)  # clear previous data
        with open("tazz_restaurants.txt", 'r', encoding="UTF-8") as file:
            for line in file:
                row = line.split(':')
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount() - 1, 0, pyqt.QtWidgets.QTableWidgetItem(row[0]))
                self.table.setItem(self.table.rowCount() - 1, 1, pyqt.QtWidgets.QTableWidgetItem(row[1]))
                self.table.setItem(self.table.rowCount() - 1, 2, pyqt.QtWidgets.QTableWidgetItem(row[2]))

    def sort_table(self, logical_index):
        current_order = self.table.horizontalHeader().sortIndicatorOrder()
        self.table.sortItems(logical_index, current_order)
        if current_order == pyqt.QtCore.Qt.SortOrder.AscendingOrder:
            self.table.horizontalHeader().setSortIndicator(logical_index, pyqt.QtCore.Qt.SortOrder.DescendingOrder)
        else:
            self.table.horizontalHeader().setSortIndicator(logical_index, pyqt.QtCore.Qt.SortOrder.AscendingOrder)


def pyqt_application():
    application = pyqt.QtWidgets.QApplication(sys.argv)
    application.setApplicationName('Tazz Extractor')
    application.setWindowIcon(pyqt.QtGui.QIcon("style/app.ico"))
    app = MyApp()
    app.setStyleSheet(open("style/style.css").read())
    app.show()
    application.exec()

