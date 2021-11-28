import sys
import sqlite3
from PyQt5.Qt import *
from mainUI import Ui_MainWindow
from addEditCoffeeFormUI import Ui_Form


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


class Coffee(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connection = sqlite3.connect('data/coffee.sqlite')
        self.cur = self.connection.cursor()
        self.form = addEditCoffeeForm(self.connection)
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.verticalHeader().setVisible(False)
        [self.tableWidget.setItemDelegateForColumn(i, ReadOnlyDelegate(self.tableWidget)) for i in range(7)]

        self.edit_or_add_coffee.triggered.connect(lambda x: self.form.show())
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


class addEditCoffeeForm(QWidget, Ui_Form):
    def __init__(self, connection):
        super().__init__()
        self.setupUi(self)

        self.titles = ['id', 'gradeOfCoffee', 'roastingDegree', 'coffeeType',
                       'tasteDescription', 'price', 'packageVolume']
        self.add_widgets = [self.gradeOfCoffee_textEdit, self.roastingDegree_textEdit,
                            self.coffeeType_textEdit, self.taste_DescriptiontextEdit,
                            self.price_textEdit, self.volume_textEdit]

        self.connection = connection
        self.cursor = self.connection.cursor()

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setItemDelegateForColumn(0, ReadOnlyDelegate(self.tableWidget))
        self.paste_data()

        self.update_radioButton.toggled.connect(
            lambda x: self.tableWidget.setEnabled(self.update_radioButton.isChecked()))
        self.add_radioButton.toggled.connect(
            lambda x: [widget.setEnabled(self.add_radioButton.isChecked()) for widget in
                       self.add_widgets] and self.add_button.setEnabled(self.add_radioButton.isChecked()))
        self.add_button.clicked.connect(self.add_row)
        self.tableWidget.itemChanged.connect(self.item_changed)

    def change_db(self, query, params=None):
        self.cursor.execute(query, (*params,)) if params else self.cursor.execute(query)
        self.connection.commit()

    def add_row(self):
        self.change_db("INSERT INTO InfoAboutCoffee VALUES (?, ?, ?, ?, ?, ?, ?)",
                       [self.tableWidget.rowCount() + 1] + [widget.toPlainText() for widget in self.add_widgets])
        [widget.clear() for widget in self.add_widgets]
        self.paste_data()

    def paste_data(self):
        for i in range(7):
            self.tableWidget.insertColumn(i)
        self.tableWidget.setHorizontalHeaderLabels(self.titles)

        results = self.cursor.execute("""SELECT * FROM InfoAboutCoffee""").fetchall()
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

    def item_changed(self, item):
        return f"UPDATE InfoAboutCoffee SET {self.titles[item.column()]}=" + \
               f"{item.text()} WHERE id={self.tableWidget.item(item.row(), 0).text()}"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Coffee()
    w.show()
    sys.exit(app.exec_())
