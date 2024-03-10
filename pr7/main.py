import sys
from PyQt5 import QtWidgets, QtCore
import connect
import tables_list
import table
import create
import sqlite3


class ExampleApp(QtWidgets.QMainWindow, connect.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connectBtn.clicked.connect(self.connect)
        self.tables_list = TablesApp(self)
        self.tables_list.show()
        self.tables_list.setVisible(False)

    def connect(self):
        self.tables_list.conn = sqlite3.connect(f'{self.dbName.text()}.sqlite')
        self.tables_list.cur = self.tables_list.conn.cursor()
        self.tables_list.setVisible(True)
        self.tables_list.get_tables()
        self.setVisible(False)


class TablesApp(QtWidgets.QWidget, tables_list.Ui_Form):
    def __init__(self, main_window: ExampleApp):
        super().__init__()
        self.setupUi(self)
        self.conn: sqlite3.Connection = None
        self.cur: sqlite3.Cursor = None
        self.closeButton.clicked.connect(self.close_connect)
        self.execBtn.clicked.connect(self.execute_query)
        self.tablesList.clicked.connect(self.select_table)
        self.addBtn.clicked.connect(self.create_table)
        self.main_window = main_window
        self.table = OneTableApp(self)
        self.table.show()
        self.table.setVisible(False)
        self.create_window = CreateApp(self)
        self.create_window.show()
        self.create_window.setVisible(False)

    def close_connect(self):
        self.main_window.setVisible(True)
        self.setVisible(False)

    def get_tables(self):
        self.tablesList.clear()
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for t in self.cur.fetchall():
            table_name = t[0]
            if table_name != "sqlite_sequence":
                self.tablesList.addItem(table_name)

    def execute_query(self):
        try:
            self.cur.execute(self.query.toPlainText())
            self.query.setText("Ok") if "select" not in self.query.toPlainText().lower() else \
                self.query.setText("\n--------------------------------------\n".join([" | ".join([str(c) for c in r])
                                                                                     for r in self.cur.fetchall()]))
            self.conn.commit()
            self.get_tables()
        except Exception as e:
            self.query.setText(str(e))

    def select_table(self, item: QtCore.QModelIndex):
        self.table.conn, self.table.cur, self.table.table_name = self.conn, self.cur, item.data()
        self.table.setVisible(True)
        self.setVisible(False)
        self.table.get_data()

    def create_table(self):
        self.create_window.conn, self.create_window.cur = self.conn, self.cur
        self.create_window.setVisible(True)
        self.setVisible(False)


class OneTableApp(QtWidgets.QWidget, table.Ui_Form):
    def __init__(self, tables_list_window: TablesApp):
        super().__init__()
        self.setupUi(self)
        self.conn: sqlite3.Connection = None
        self.cur: sqlite3.Cursor = None
        self.table_name = None
        self.count = 0
        self.returnButton.clicked.connect(self.return_to_tables)
        self.dropBtn.clicked.connect(self.drop_table)
        self.deleteBtn.clicked.connect(self.delete_table)
        self.addBtn.clicked.connect(self.add_row)
        self.saveBtn.clicked.connect(self.save_table)
        self.tables_list_window = tables_list_window

    def get_data(self):
        self.tableWidget.clear()
        self.cur.execute(f'PRAGMA table_info("{self.table_name}")')
        column_names = [i[1] for i in self.cur.fetchall()]
        self.tableWidget.setColumnCount(len(column_names))
        self.tableWidget.setHorizontalHeaderLabels(column_names)
        self.cur.execute(f'select * from {self.table_name}')
        result = self.cur.fetchall()
        self.count = len(result)
        self.tableWidget.setRowCount(self.count)
        for i, row in enumerate(result):
            for j, cell in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(cell)))
        self.tableWidget.resizeColumnsToContents()

    def add_row(self):
        self.count += 1
        self.tableWidget.setRowCount(self.count)

    def return_to_tables(self):
        self.tables_list_window.setVisible(True)
        self.setVisible(False)

    def drop_table(self):
        self.cur.execute(f'drop table {self.table_name}')
        self.conn.commit()
        self.tables_list_window.get_tables()
        self.return_to_tables()

    def delete_table(self):
        self.cur.execute(f'delete from {self.table_name}')
        self.conn.commit()
        self.get_data()

    def save_table(self):
        self.cur.execute(f'delete from {self.table_name}')
        self.conn.commit()
        columns = self.tableWidget.columnCount()
        data = [[self.tableWidget.item(i, j).text() if self.tableWidget.item(i, j) is not None else None
                 for j in range(columns)] for i in range(self.count)]
        for row in data:
            query = f"""insert into {self.table_name} values
            ({', '.join([f"'{d}'" for d in row])})"""
            self.cur.execute(query)
        self.conn.commit()


class CreateApp(QtWidgets.QDialog, create.Ui_Dialog):
    def __init__(self, tables_list_window: TablesApp):
        super().__init__()
        self.setupUi(self)
        self.conn: sqlite3.Connection = None
        self.cur: sqlite3.Cursor = None
        self.cancelBtn.clicked.connect(self.cancel)
        self.addBtn.clicked.connect(lambda: self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1))
        self.acceptBtn.clicked.connect(self.save_table)
        self.tables_list_window = tables_list_window

    def cancel(self):
        self.tables_list_window.setVisible(True)
        self.setVisible(False)

    def save_table(self):
        rows = self.tableWidget.rowCount()
        columns = self.tableWidget.columnCount()
        print(rows, columns)
        text = lambda x: "" if x is None else x.text().upper()
        data = [[text(self.tableWidget.item(i, j)) if text(self.tableWidget.item(i, j)) != "PRIMARY KEY"
                 else "PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL"
                if j > 0 and text(self.tableWidget.item(i, j - 1)) == "INTEGER" else
                "PRIMARY KEY UNIQUE NOT NULL" for j in range(columns)] for i in range(rows)]
        query = f"""
            create table {self.tableName.text()} (
                {", ".join([" ".join([c for c in r]) for r in data])}
            )
        """
        self.cur.execute(query)
        self.conn.commit()
        self.tables_list_window.get_tables()
        self.cancel()


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
