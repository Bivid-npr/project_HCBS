import sys
from PyQt6.QtWidgets import QApplication
from view.login_view import LoginView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginView()
    window.show()
    sys.exit(app.exec())