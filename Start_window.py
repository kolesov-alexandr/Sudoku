import sqlite3
import Registration
import Logging_in

from PyQt5.QtWidgets import QWidget
from start_window_ui import Ui_Form


class MyWidget(QWidget, Ui_Form):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)
        self.logInButton.clicked.connect(self.logging_in)
        self.registrationButton.clicked.connect(self.registration)

    def initUI(self, args):
        self.setupUi(self)
        self.previous = args[0]

    def logging_in(self):
        self.log_window = Logging_in.MyWidget(self)
        self.log_window.show()

    def registration(self):
        self.reg_window = Registration.MyWidget(self)
        self.reg_window.show()

    def closeEvent(self, event):
        con = sqlite3.connect("sudoku.sqlite")
        cur = con.cursor()
        active_player = cur.execute("""SELECT login, password FROM players
            WHERE is_active = 1""").fetchall()
        con.close()
        if not active_player:
            self.previous.close()
        else:
            self.previous.login, self.previous.password = active_player[0]
            self.previous.newGameButton.clicked.connect(self.previous.new_game)
            self.previous.changePasswordAction.triggered.connect(self.previous.change_password)
            self.previous.quitAccountAction.triggered.connect(self.previous.quit_account)
            self.previous.deleteAccountAction.triggered.connect(self.previous.delete_account)
