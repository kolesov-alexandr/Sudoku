import csv
import sqlite3
import Winner

from PyQt5.QtWidgets import QWidget, QInputDialog, QPushButton, QButtonGroup, QMessageBox
from PyQt5.QtCore import QTimer
from copy import deepcopy
from sudoku_ui import Ui_Form

DIFFICULTIES = {"easy": "лёгкий", "normal": "обычный", "hard": "сложный"}
SIDE = 9
MINUTE = 60
TIME_INTERVAL = 1000
ITEM_SIZE = 60
ITEM_SEP_SIZE = 7


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setupUi(self)
        self.previous = args[0]
        self.login = args[1]
        self.field = args[2]
        self.difficulty = args[3]
        self.number = args[4]
        con = sqlite3.connect("sudoku.sqlite")
        cur = con.cursor()
        cur.execute("""UPDATE players SET is_game = 1 WHERE
            is_active = 1""")
        con.commit()
        con.close()
        self.itemsButtonGroup = QButtonGroup(self)
        for i in range(SIDE ** 2):
            button = QPushButton("", self)
            button.setGeometry(10 + i % SIDE * ITEM_SIZE + i % SIDE * ITEM_SEP_SIZE,
                               120 + i // SIDE * ITEM_SIZE + i // SIDE * ITEM_SEP_SIZE,
                               ITEM_SIZE, ITEM_SIZE)
            button.clicked.connect(self.write_number)
            number = self.field[i // SIDE][i % SIDE]
            if number:
                button.setText(str(number))
                button.setEnabled(False)
            self.itemsButtonGroup.addButton(button, i)
        self.solved_field = solve(self.field)
        self.checkButton.clicked.connect(self.check)
        if len(args) == 5:
            self.attempts = 0
            self.attemptsDisplayLabel.setText(str(self.attempts))
            self.timer = QTimer(self)
            self.timer.setInterval(TIME_INTERVAL)
            self.count_seconds = 0
            self.timeDisplayLabel.setText("00:00")
            self.timer.start()
            self.timer.timeout.connect(self.show_time)
        else:
            self.attempts = args[6]
            self.attemptsDisplayLabel.setText(str(self.attempts))
            self.time_ = args[5]
            self.timer = QTimer(self)
            self.timer.setInterval(1000)
            minutes, seconds = map(int, self.time_.split(":")[1:])
            self.count_seconds = minutes * 60 + seconds
            self.timeDisplayLabel.setText(self.time_[3:])
            self.timer.start()
            self.timer.timeout.connect(self.show_time)

    def show_time(self):
        self.count_seconds += 1
        self.timeDisplayLabel.setText("{:02d}:{:02d}".format(self.count_seconds // MINUTE,
                                                             self.count_seconds % MINUTE))

    def check(self):
        self.timer.stop()
        self.attempts += 1
        self.attemptsDisplayLabel.setText(str(self.attempts))
        if self.field == self.solved_field:
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            time_ = "00:" + self.timeDisplayLabel.text()
            cur.execute("""INSERT INTO results(id_player, id_field, time, attempts) VALUES ((
                SELECT id FROM players WHERE login = ?), (
                SELECT id FROM fields WHERE id_difficulty = (SELECT id FROM difficulties
                WHERE title = ?) AND field = ?), ?, ?)""", (self.login,
                                                            DIFFICULTIES[self.difficulty],
                                                            self.difficulty +
                                                            "/" + str(self.number) + ".csv",
                                                            time_,
                                                            self.attempts))
            cur.execute("""UPDATE players SET is_game = 0, id_field = ?, time = ?, attempts = ?
                WHERE is_active = 1""", (None, None, None))
            self.previous.previous.continueGameButton.setEnabled(False)
            con.commit()
            con.close()
            self.winner_window = Winner.MyWidget(self, self.difficulty, self.number)
            self.winner_window.show()
        else:
            self.errorLabel.setText("Неверно! Попробуйте ещё")
            for i in range(SIDE ** 2):
                button = self.itemsButtonGroup.button(i)
                if button.isEnabled() and button.text():
                    number = int(button.text())
                    correct_number = self.solved_field[i // SIDE][i % SIDE]
                    if number == correct_number:
                        button.setEnabled(False)
            self.timer.start()

    def write_number(self):
        number, ok_pressed = QInputDialog.getInt(
            self, "", "Введите число:",
            1, 1, 9, 1)
        if ok_pressed:
            self.sender().setText(str(number))
            index = self.itemsButtonGroup.id(self.sender())
            self.field[index // SIDE][index % SIDE] = number

    def closeEvent(self, event):
        con = sqlite3.connect("sudoku.sqlite")
        cur = con.cursor()
        active_game = cur.execute("""SELECT is_game FROM players WHERE is_active = 1""").fetchone()
        con.close()
        if active_game[0]:
            valid = QMessageBox.question(self, "Сохранить игру",
                                         "Вы хотите сохранить результаты игры", QMessageBox.Yes |
                                         QMessageBox.No | QMessageBox.Cancel)
            if valid == QMessageBox.Yes:
                time_ = "00:" + self.timeDisplayLabel.text()
                con = sqlite3.connect("sudoku.sqlite")
                cur = con.cursor()
                cur.execute("""UPDATE players SET id_field = (
                    SELECT id FROM fields WHERE id_difficulty = (
                    SELECT id FROM difficulties WHERE title = ?) AND field = ?), time = ?,
                    attempts = ? WHERE is_active = 1""", (
                    DIFFICULTIES[self.difficulty], self.difficulty + "/" + str(self.number) +
                    ".csv", time_, self.attempts))
                con.commit()
                con.close()
                file = open("saved_games/" + self.login + ".csv", "w", encoding="utf-8",
                            newline="")
                writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for i in range(SIDE):
                    row = self.field[i]
                    writer.writerow(row)
                file.close()
                self.previous.previous.continueGameButton.setEnabled(True)
                self.previous.previous.continueGameButton.clicked.connect(
                    self.previous.previous.continue_game)
            elif valid == QMessageBox.No:
                con = sqlite3.connect("sudoku.sqlite")
                cur = con.cursor()
                cur.execute("""UPDATE players SET is_game = 0, id_field = ?, time = ?, attempts = ?
                    WHERE is_active = 1""", (None, None, None))
                con.commit()
                con.close()
                self.previous.previous.continueGameButton.setEnabled(False)
            else:
                event.ignore()
                self.timer.start()


def get_variants(sudoku):
    variants = []
    for i, row in enumerate(sudoku):
        for j, value in enumerate(row):
            if not value:
                row_values = set(row)
                column_values = set([sudoku[k][j] for k in range(SIDE)])
                sq_y = i // int(SIDE ** 0.5)
                sq_x = j // int(SIDE ** 0.5)
                square3x3_values = set([
                    sudoku[m][n]
                    for m in range(sq_y * int(SIDE ** 0.5), sq_y * (int(SIDE ** 0.5) + 1))
                    for n in range(sq_x * int(SIDE ** 0.5), sq_x * (int(SIDE ** 0.5) + 1))
                ])
                exists = row_values | column_values | square3x3_values
                values = set(range(1, SIDE + 1)) - exists
                variants.append((i, j, values))

    return variants


def solve(sudoku):
    if all([k for row in sudoku for k in row]):
        return sudoku
    variants = get_variants(sudoku)
    x, y, values = min(variants, key=lambda x: len(x[2]))
    for v in values:
        new_sudoku = deepcopy(sudoku)
        new_sudoku[x][y] = v
        s = solve(new_sudoku)
        if s:
            return s
    return None
