import random
import csv
import sqlite3
import Sudoku

from PyQt5.QtWidgets import QWidget
from new_game_ui import Ui_Form

DIFFICULTIES = {"лёгкий": "easy", "обычный": "normal", "сложный": "hard"}


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.newGameButton.clicked.connect(self.new_game)

    def initUI(self, args):
        self.setupUi(self)
        self.previous = args[0]
        self.login = args[1]
        self.password = args[2]
        self.is_game = args[3]
        if self.is_game:
            self.time_ = args[4]
            self.attempts = args[5]

    def new_game(self):
        difficulty = DIFFICULTIES[self.difficultyButtonGroup.checkedButton().text()]
        number = random.randrange(1, 20 + 1)
        field_file = open(difficulty + "/" + str(number) + ".csv", encoding="utf-8")
        reader = csv.reader(field_file, delimiter=";", quotechar='"')
        field = [list(map(int, string)) for string in reader]
        self.close()
        self.sudoku_window = Sudoku.MyWidget(self, self.login, field, difficulty, number)
        self.sudoku_window.show()

    def closeEvent(self, event):
        if self.is_game:
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            id_field = cur.execute("""SELECT id_difficulty, field FROM fields
                WHERE id = (SELECT id_field FROM players WHERE is_active = 1)""").fetchone()
            difficulty = DIFFICULTIES[cur.execute("""SELECT title FROM difficulties WHERE id = (
                SELECT id_difficulty FROM fields WHERE id_difficulty = ?)""", (
                int(id_field[0]),),).fetchone()[0]]
            con.close()
            number = id_field[1].replace(difficulty + "/", "")
            number = int(number[:number.index(".")])
            field_file = open("saved_games/" + self.login + ".csv", encoding="utf-8")
            reader = csv.reader(field_file, delimiter=";", quotechar='"')
            field = [list(map(int, string)) for string in reader]
            self.sudoku_window = Sudoku.MyWidget(self, self.login, field, difficulty, number,
                                                 self.time_, self.attempts)
            self.sudoku_window.show()
