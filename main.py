import sys
import sqlite3
from PyQt5.Qt import *
from PyQt5.uic import loadUi


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        self.connection = sqlite3.connect('coffee.sqlite')
        self.cur = self.connection.cursor()
        self.tableWidget.verticalHeader().setVisible(False)
        self.paste_data()

    def paste_data(self):
        for i in range(7):
            self.tableWidget.insertColumn(i)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах',
                                                    'описание вкуса', 'цена', 'объем упаковки'])

        results = self.cur.execute("""
        SELECT * FROM InfoAboutCoffee""").fetchall()
        rows = len(results)
        columns = len(results[0])
        self.tab(columns, rows, results)

    def tab(self, columns, rows, results):
        self.tableWidget.setRowCount(rows)
        self.tableWidget.setColumnCount(columns)

        for i in range(rows):
            for j in range(columns):
                item = QTableWidgetItem("{}".format(results[i][j]))
                item.setTextAlignment(Qt.AlignHCenter)
                self.tableWidget.setItem(i, j, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Coffee()
    w.show()
    sys.exit(app.exec_())
