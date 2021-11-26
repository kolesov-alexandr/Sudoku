import sqlite3

from PyQt5.QtWidgets import QWidget
from logging_in_ui import Ui_Form


class FormatError(Exception):
    pass


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.logInButton.clicked.connect(self.logging_in)

    def initUI(self, args):
        self.setupUi(self)
        self.previous = args[0]

    def logging_in(self):
        try:
            login = self.loginLineEdit.text()
            password = self.passwordLineEdit.text()
            if not (login and password):
                raise FormatError("Неверный формат данных")
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            player = cur.execute("""SELECT id from players
                WHERE login = ? AND password = ?""", (login, password)).fetchall()
            if not player:
                con.close()
                raise ValueError("Неверное сочетание логина и пароля")
            cur.execute("""UPDATE players SET is_active = 1
                WHERE login = ? AND password = ?""", (login, password))
            con.commit()
            self.close()
            self.previous.close()
            self.previous.previous.login = login
            self.previous.previous.password = password
            self.previous.previous.nameLabel.setText("Приветствую, " + login)
            active_game = cur.execute("""SELECT is_game FROM players
                WHERE is_active = 1""").fetchone()
            con.close()
            if active_game and active_game[0]:
                self.previous.previous.continueGameButton.setEnabled(True)
                self.previous.previous.continueGameButton.clicked.connect(
                    self.previous.previous.continue_game)
            else:
                self.previous.previous.continueGameButton.setEnabled(False)
        except Exception as error:
            self.errorLabel.setText("{}".format(error))
