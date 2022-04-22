from Login.Main import LoginWindow as login
from MainMenu.Main import MainWindow as menu

import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = login()
    login.show()
    sys.exit(app.exec())