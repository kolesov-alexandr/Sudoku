import sys
import string
import sqlite3
import os
import Start_window
import New_game
import Change_password

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from main_window_ui import Ui_MainWindow
from Registration import *


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.newGameButton.clicked.connect(self.new_game)
        self.changePasswordAction.triggered.connect(self.change_password)
        self.quitAccountAction.triggered.connect(self.quit_account)
        self.deleteAccountAction.triggered.connect(self.delete_account)
        self.helpAction.triggered.connect(self.help)

    def initUI(self):
        self.setupUi(self)
        con = sqlite3.connect("sudoku.sqlite")
        cur = con.cursor()
        active_player = cur.execute("""SELECT login, password FROM players
            WHERE is_active = 1""").fetchall()
        con.close()
        if not active_player:
            self.start_window = Start_window.MyWidget(self, "")
            self.start_window.show()
        else:
            self.login, self.password = active_player[0]
            self.nameLabel.setText("Приветствую, " + self.login)
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            active_game = cur.execute("""SELECT is_game FROM players
                        WHERE is_active = 1""").fetchone()
            con.close()
            if active_game and active_game[0]:
                self.continueGameButton.setEnabled(True)
                self.continueGameButton.clicked.connect(self.continue_game)

    def new_game(self):
        con = sqlite3.connect("sudoku.sqlite")
        cur = con.cursor()
        active_game = cur.execute("""SELECT is_game FROM players
                            WHERE is_active = 1""").fetchone()
        if active_game[0]:
            valid = QMessageBox.warning(self, "Предупреждение",
                                        "Результаты прошлой игры будут " +
                                        "удалены. Вы уверены, что хотите продолжить?",
                                        QMessageBox.Yes | QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.continueGameButton.setEnabled(False)
                cur.execute("""UPDATE players SET is_game = 0, id_field = ?, time = ?, attempts = ?
                    WHERE is_active = 1""", (None, None, None))
                con.commit()
                con.close()
                self.new_game_window = New_game.MyWidget(self, self.login, self.password, False)
                self.new_game_window.show()
        else:
            con.close()
            self.new_game_window = New_game.MyWidget(self, self.login, self.password, False)
            self.new_game_window.show()

    def continue_game(self):
        con = sqlite3.connect("sudoku.sqlite")
        cur = con.cursor()
        time_, attempts = cur.execute("""SELECT time, attempts FROM players
            WHERE is_active = 1""").fetchone()
        con.close()
        self.new_game_window = New_game.MyWidget(self, self.login, self.password, True,
                                                 time_, attempts)
        self.new_game_window.show()
        self.new_game_window.close()

    def change_password(self):
        self.change_password_window = Change_password.MyWidget(self, self.login)
        self.change_password_window.show()

    def quit_account(self):
        valid = QMessageBox.question(
            self, "Подтвердите действие", "Выйти из аккаунта?",
            QMessageBox.Yes | QMessageBox.No)
        if valid == QMessageBox.Yes:
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            cur.execute("""UPDATE players SET is_active = 0
                WHERE is_active = 1""")
            con.commit()
            con.close()
            self.start_window = Start_window.MyWidget(self)
            self.start_window.show()

    def delete_account(self):
        valid = QMessageBox.question(
            self, "Подтвердите действие", "Удалить аккаунт?",
            QMessageBox.Yes | QMessageBox.No)
        if valid == QMessageBox.Yes:
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            cur.execute("""DELETE FROM players
                        WHERE is_active = 1""")
            con.commit()
            con.close()
            self.start_window = Start_window.MyWidget(self, "")
            self.start_window.show()

    def help(self):
        os.system("start help.docx")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MyWidget()
    main_window.show()
    sys.exit(app.exec_())
