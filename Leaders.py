import sqlite3

from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from leaders_ui import Ui_Form

DIFFICULTIES = {"easy": "лёгкий", "normal": "обычный", "hard": "сложный"}
COLUMNS_COUNT = 4


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setupUi(self)
        self.previous = args[0]
        self.difficulty = args[1]
        self.number = args[2]
        self.leaders()

    def leaders(self):
        self.leadersTable.setColumnCount(COLUMNS_COUNT)
        self.leadersTable.setRowCount(0)
        self.leadersTable.setHorizontalHeaderLabels(("Место", "Игрок", "Время",
                                                     "Количество затраченных попыток"))
        con = sqlite3.connect("sudoku.sqlite")
        cur = con.cursor()
        leaders = cur.execute("""SELECT id_player, time, attempts FROM results
            WHERE id_field = (SELECT id FROM fields WHERE id_difficulty = (
            SELECT id FROM difficulties WHERE title = ?) AND field = ?)
            ORDER BY attempts, time ASC""", (DIFFICULTIES[self.difficulty], self.difficulty + "/" +
                                             str(self.number) + ".csv")).fetchall()
        for i, row in enumerate(leaders):
            self.leadersTable.setRowCount(
                self.leadersTable.rowCount() + 1)
            player = cur.execute("""SELECT login FROM players WHERE id = ?""", (
                row[0],)).fetchone()
            self.leadersTable.setItem(i, 0, QTableWidgetItem(str(i + 1)))
            self.leadersTable.setItem(i, 1, QTableWidgetItem(player[0]))
            self.leadersTable.setItem(i, 2, QTableWidgetItem(str(row[1])[3:]))
            self.leadersTable.setItem(i, 3, QTableWidgetItem(str(row[2])))
        con.close()
        self.leadersTable.resizeColumnsToContents()
        self.leadersTable.setEnabled(False)

    def closeEvent(self, event):
        self.previous.close()
