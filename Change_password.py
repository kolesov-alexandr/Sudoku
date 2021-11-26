import sqlite3
import string
import Registration

from PyQt5.QtWidgets import QWidget, QMessageBox
from change_password_ui import Ui_Form


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.changePasswordButton.clicked.connect(self.change_password)

    def initUI(self, args):
        self.setupUi(self)
        self.previous = args[0]
        self.login = args[1]

    def change_password(self):
        try:
            password = self.passwordLineEdit.text()
            check_password = self.checkPasswordLineEdit.text()
            if not (password and check_password):
                raise Registration.FormatError("Неверный формат данных")
            if len(password) < 12:
                raise Registration.LengthError("Слишком короткий пароль")
            if not (set(password) & set(string.ascii_letters)):
                raise Registration.LettersError("В пароле отсутствуют буквы")
            if not (set(password) & set(string.ascii_uppercase)):
                raise Registration.BigLettersError("В пароле отсутствуют буквы верхнего регистра")
            if not (set(password) & set(string.ascii_lowercase)):
                raise Registration.SmallLettersError("В пароле отсутствуют буквы нижнего регистра")
            if not (set(password) & set(string.digits)):
                raise Registration.DigitsError("В пароле отсутствуют цифры")
            if not (set(password) & set(string.punctuation)):
                raise Registration.SpecialSymbolsError("В пароле отсутствуют специальные символы")
            if password != check_password:
                raise ValueError("Введены разные пароли")
            con = sqlite3.connect("sudoku.sqlite")
            cur = con.cursor()
            existing_password = cur.execute("""SELECT password from players
                WHERE login = ?""", (self.login,)).fetchone()
            if existing_password[0] == password:
                con.close()
                raise ValueError("Введён пароль, существоваший до этого")
            cur.execute("""UPDATE players SET password = ? WHERE login = ?""", (
                password, self.login))
            con.commit()
            con.close()
            self.close()
            self.previous.password = password
            QMessageBox.information(self, "Успешно", "Вы успешно сменили пароль", QMessageBox.Ok)
        except Exception as error:
            self.errorLabel.setText("{}".format(error))
