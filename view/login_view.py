from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                              QLabel, QLineEdit, QPushButton,
                              QMessageBox, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from controller.auth_controller import AuthController
from models.user import BookingStaff, Admin, Manager


class LoginView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.auth_controller = AuthController()
        self.setWindowTitle("Horizon Cinemas - Login")
        self.setFixedSize(400, 340)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background-color: #202124;")

        layout = QVBoxLayout(central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)
        layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Horizon Cinemas")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #e8eaed;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel("Booking Management System")
        subtitle.setFont(QFont("Arial", 10))
        subtitle.setStyleSheet("color: #9aa0a6;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #292a2d;
                border-radius: 8px;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(10)
        frame_layout.setContentsMargins(24, 20, 24, 20)

        input_style = """
            QLineEdit {
                background-color: #303134;
                color: #e8eaed;
                border: 1px solid #5f6368;
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #8ab4f8;
            }
        """
        label_style = "color: #9aa0a6; font-size: 12px;"

        username_label = QLabel("Username")
        username_label.setStyleSheet(label_style)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedHeight(36)
        self.username_input.setStyleSheet(input_style)

        password_label = QLabel("Password")
        password_label.setStyleSheet(label_style)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(36)
        self.password_input.setStyleSheet(input_style)
        self.password_input.returnPressed.connect(self._handle_login)

        login_btn = QPushButton("Sign in")
        login_btn.setFixedHeight(38)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #8ab4f8;
                color: #202124;
                font-size: 13px;
                font-weight: bold;
                border-radius: 4px;
                border: none;
            }
            QPushButton:hover {
                background-color: #aecbfa;
            }
            QPushButton:pressed {
                background-color: #669df6;
            }
        """)
        login_btn.clicked.connect(self._handle_login)

        frame_layout.addWidget(username_label)
        frame_layout.addWidget(self.username_input)
        frame_layout.addWidget(password_label)
        frame_layout.addWidget(self.password_input)
        frame_layout.addSpacing(6)
        frame_layout.addWidget(login_btn)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(16)
        layout.addWidget(frame)

    def _handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Input Error",
                                "Please enter username and password.")
            return

        user = self.auth_controller.login(username, password)

        if not user:
            QMessageBox.critical(self, "Login Failed",
                                 "Invalid username or password.")
            return

        self._open_dashboard(user)

    def _open_dashboard(self, user):
        if isinstance(user, Manager):
            from view.manager_view import ManagerView
            self.dashboard = ManagerView(user)
        elif isinstance(user, Admin):
            from view.admin_view import AdminView
            self.dashboard = AdminView(user)
        elif isinstance(user, BookingStaff):
            from view.staff_view import StaffView
            self.dashboard = StaffView(user)
        self.dashboard.show()
        self.close()
