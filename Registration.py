import string
import sqlite3

from PyQt5.QtWidgets import QWidget
from registration_ui import Ui_Form


class FormatError(Exception):
    pass


class LengthError(Exception):
    pass


class LettersError(Exception):
    pass


class BigLettersError(Exception):
    pass


class SmallLettersError(Exception):
    pass


class DigitsError(Exception):
    pass


class SpecialSymbolsError(Exception):
    pass


class LoginError(Exception):
    pass


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.registrationButton.clicked.connect(self.registration)

    def initUI(self, args):
        self.setupUi(self)
        self.previous = args[0]

    def registration(self):
        try:
            login = self.loginLineEdit.text()
            password = self.passwordLineEdit.text()
            if not (login and password):
                raise FormatError("Неверный формат данных")
            if len(password) < 12:
                raise LengthError("Слишком короткий пароль")
            if not (set(password) & set(string.ascii_letters)):
                raise LettersError("В пароле отсутствуют буквы")
            if not (set(password) & set(string.ascii_uppercase)):
                raise BigLettersError("В пароле отсутствуют буквы верхнего регистра")
            if not (set(password) & set(string.ascii_lowercase)):
                raise SmallLettersError("В пароле отсутствуют буквы нижнего регистра")
            if not (set(password) & set(string.digits)):
                raise DigitsError("В пароле отсутствуют цифры")
            if not (set(password) & set(string.punctuation)):
                raise SpecialSymbolsError("В пароле отсутствуют специальные символы")
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            existing_player = cur.execute("""SELECT id FROM players
                    WHERE login = ?""", (login,)).fetchall()
            if existing_player:
                con.close()
                raise LoginError("Аккаунт с этим логином уже существует")
            cur.execute("""INSERT INTO players(login, password, is_active) VALUES (?, ?, 1)""", (
                login, password))
            con.commit()
            self.close()
            self.previous.close()
            self.previous.previous.login = login
            self.previous.previous.password = password
            self.previous.previous.nameLabel.setText("Приветствую, " + login)
            con.close()
            self.previous.previous.continueGameButton.setEnabled(False)
        except Exception as error:
            self.errorLabel.setText("{}".format(error))
